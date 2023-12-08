# %pip install trulens

import torch
from transformers import (DistilBertForSequenceClassification,
                          DistilBertTokenizer)
from trulens.nn.attribution import Cut, IntegratedGradients, OutputCut
from trulens.nn.models import get_model_wrapper
from trulens.nn.quantities import ClassQoI
from trulens.utils.nlp import token_baseline
from trulens.utils.typing import ModelInputs
from trulens.visualizations import HTML, NLP, IPython, Output


class GradioHTML(Output):
    """Gradio Highligher visualization output format."""

    def __init__(self):
        super().__init__()

    def blank(self):
        return []

    def space(self):
        return ' '

    def escape(self, s):
        return s

    def linebreak(self):
        return '\n'

    def line(self, s):
        return s

    def clean(self, s):
        return s.replace(" ", "")
     
    def magnitude_colored(self, s, mag):
        return (self.clean(s), round(torch.Tensor.item(mag),3)*100)

    def append(self, *pieces) -> list:
        # firs case: label
        if len(pieces) == 3 and pieces[1] == ':' and pieces[2] == self.space():
            return [pieces[0]]
        
        # second case: append space
        elif len(pieces) == 2 and pieces[1] == self.space():
            return pieces[0]
        
        #third case: list = list + new tuple
        elif len(pieces) == 2:
            pieces[0].append(pieces[1])
            return pieces[0]
        
        # fourth case: add contents 
        elif len(pieces) == 4:
            # (first time : blank + new content + br + br )
            if pieces[0] == self.blank():
                return pieces[1]
            # (nth time : content + new content + br + br )
            else:
                return [pieces[0],pieces[1]]
            
        return pieces

    def render(self, s):
        
        return s


class CustomHTML(HTML):
    """Interactive python visualization output format."""

    def __init__(self):
        super().__init__()

    def clean(self, s):
        return s.replace(" ", "")
 
    def magnitude_colored(self, s, mag):
        red = 0.0
        green = 0.0
        if mag > 0:
            green = 1.0  # 0.5 + mag * 0.5
            red = 1.0 - mag * 0.5
        else:
            red = 1.0
            green = 1.0 + mag * 0.5
            #red = 0.5 - mag * 0.5

        blue = min(red, green)
        # blue = 1.0 - max(red, green)

        return f"<span title='{mag:0.3f}' style='margin: 1px; padding: 1px; border-radius: 4px; background: grey; color: rgb({red*255}, {green*255}, {blue*255});'>{self.clean(s)}</span>"



class CustomIPython(IPython):
    """Interactive python visualization output format."""

    def __init__(self):
        super().__init__()

    def clean(self, s):
        return s.replace(" ", "")
 
    def magnitude_colored(self, s, mag):
        red = 0.0
        green = 0.0
        if mag > 0:
            green = 1.0  # 0.5 + mag * 0.5
            red = 1.0 - mag * 0.5
        else:
            red = 1.0
            green = 1.0 + mag * 0.5
            #red = 0.5 - mag * 0.5

        blue = min(red, green)
        # blue = 1.0 - max(red, green)

        return f"<span title='{mag:0.3f}' style='margin: 1px; padding: 1px; border-radius: 4px; background: grey; color: rgb({red*255}, {green*255}, {blue*255});'>{self.clean(s)}</span>"



# Wrap all of the necessary components.
class SimpleEnglishClassifier:
    
    def __init__(self, model_path:str, resolution:int=20):
        self.model_path = model_path
        self.resolution = resolution
    
        self.model_name = model_path.split('/')[-1]

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") 

        self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_path, use_safetensors=True )
        self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})

        self.model = DistilBertForSequenceClassification.from_pretrained(self.model_path, use_safetensors=True).to(self.device)

        self.labels = ["simple", "complex"]

        self.SIMPLE = self.labels.index('simple')
        self.COMPLEX = self.labels.index('complex')

        self.wrapper = get_model_wrapper(self.model, device=self.device)

        # run integrated gradients
        self.integrated_gradients(res=self.resolution)

    def visualization(self, texts, output_type=None):
        V = NLP(
            wrapper=self.wrapper,
            labels=self.labels,
            output=output_type,
            decode=lambda x: self.tokenizer.decode(x),
            tokenize=lambda sentences: ModelInputs(kwargs=self.tokenizer(sentences, padding=True, return_tensors='pt')).map(lambda t: t.to(self.device)),
            input_accessor=lambda x: x.kwargs['input_ids'],
            output_accessor=lambda x: x['logits'],
            hidden_tokens=set([self.tokenizer.pad_token_id]),
            
        )
        return 'INFL COMPLEX (W/BASELINE)', V.token_attribution(texts, self.infl_complex_baseline)

    def integrated_gradients(self, res:int=20):
        # Parameters
        infl_max = IntegratedGradients(
            model = self.wrapper,
            doi_cut=Cut('distilbert_embeddings_word_embeddings'),
            qoi_cut=OutputCut(accessor=lambda o: o['logits'])
        )

        infl_complex = IntegratedGradients(
            model = self.wrapper,
            doi_cut=Cut('distilbert_embeddings_word_embeddings'),
            qoi=ClassQoI(self.COMPLEX),
            qoi_cut=OutputCut(accessor=lambda o: o['logits'])
        )

        inputs_baseline_ids, inputs_baseline_embeddings = token_baseline(
            keep_tokens=set([self.tokenizer.cls_token_id, self.tokenizer.sep_token_id]),
            replacement_token=self.tokenizer.pad_token_id,
            input_accessor=lambda x: x.kwargs['input_ids'],
            ids_to_embeddings=self.model.get_input_embeddings()
            )


        self.infl_complex_baseline = IntegratedGradients(
            model = self.wrapper,
            resolution=res,
            baseline = inputs_baseline_embeddings,
            doi_cut=Cut('distilbert_embeddings_word_embeddings'),
            qoi=ClassQoI(self.COMPLEX),
            qoi_cut=OutputCut(accessor=lambda o: o['logits'])
        )
        
        return



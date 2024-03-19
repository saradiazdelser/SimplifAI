import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
from trulens.nn.attribution import Cut, IntegratedGradients, OutputCut
from trulens.nn.models import get_model_wrapper
from trulens.nn.quantities import ClassQoI
from trulens.utils.nlp import token_baseline
from trulens.utils.typing import ModelInputs
from trulens.visualizations import NLP


# Wrap all of the necessary components.
class SimpleEnglishClassifier:

    def __init__(
        self,
        model_path: str = "saradiaz/distilbert-base-uncased-simpleEng-classifier",
        resolution: int = 20,
    ):
        self.model_path = model_path
        self.resolution = resolution

        self.model_name = model_path.split("/")[-1]

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.tokenizer = DistilBertTokenizer.from_pretrained(
            self.model_path, use_safetensors=True
        )
        self.tokenizer.add_special_tokens({"pad_token": "[PAD]"})

        self.model = DistilBertForSequenceClassification.from_pretrained(
            self.model_path, use_safetensors=True
        ).to(self.device)

        self.labels = ["simple", "complex"]

        self.SIMPLE = self.labels.index("simple")
        self.COMPLEX = self.labels.index("complex")

        self.wrapper = get_model_wrapper(self.model, device=self.device)

        # run integrated gradients
        self.integrated_gradients(res=self.resolution)

    def visualization(self, texts, output_type=None):
        V = NLP(
            wrapper=self.wrapper,
            labels=self.labels,
            output=output_type,
            decode=lambda x: self.tokenizer.decode(x),
            tokenize=lambda sentences: ModelInputs(
                kwargs=self.tokenizer(sentences, padding=True, return_tensors="pt")
            ).map(lambda t: t.to(self.device)),
            input_accessor=lambda x: x.kwargs["input_ids"],
            output_accessor=lambda x: x["logits"],
            hidden_tokens=set([self.tokenizer.pad_token_id]),
        )
        return "INFL COMPLEX (W/BASELINE)", V.token_attribution(
            texts, self.infl_complex_baseline
        )

    def integrated_gradients(self, res: int = 20):
        # Parameters
        infl_max = IntegratedGradients(
            model=self.wrapper,
            doi_cut=Cut("distilbert_embeddings_word_embeddings"),
            qoi_cut=OutputCut(accessor=lambda o: o["logits"]),
        )

        infl_complex = IntegratedGradients(
            model=self.wrapper,
            doi_cut=Cut("distilbert_embeddings_word_embeddings"),
            qoi=ClassQoI(self.COMPLEX),
            qoi_cut=OutputCut(accessor=lambda o: o["logits"]),
        )

        inputs_baseline_ids, inputs_baseline_embeddings = token_baseline(
            keep_tokens=set([self.tokenizer.cls_token_id, self.tokenizer.sep_token_id]),
            replacement_token=self.tokenizer.pad_token_id,
            input_accessor=lambda x: x.kwargs["input_ids"],
            ids_to_embeddings=self.model.get_input_embeddings(),
        )

        self.infl_complex_baseline = IntegratedGradients(
            model=self.wrapper,
            resolution=res,
            baseline=inputs_baseline_embeddings,
            doi_cut=Cut("distilbert_embeddings_word_embeddings"),
            qoi=ClassQoI(self.COMPLEX),
            qoi_cut=OutputCut(accessor=lambda o: o["logits"]),
        )

        return

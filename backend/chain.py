
from typing import List

from custom_feedback import (CustomMetrics, CustomNaturalLanguageFeedback,
                             CustomSpaCy)
from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub, VertexAI
from langchain.prompts import PromptTemplate
from prompts import SIMPLE_ENGLISH_PROMPT
from trulens_eval import Feedback, Huggingface


def define_feedback()->List[Feedback]:
    hugs = Huggingface()
    cspa = CustomSpaCy()
    cmetr = CustomMetrics()
    cnlf = CustomNaturalLanguageFeedback()
    
    langmatch = Feedback(hugs.language_match).on_input_output()
    piidetect = Feedback(hugs.pii_detection).on_input()
    nottoxic = Feedback(hugs.not_toxic).on_output()

    simplicity_in = Feedback(cspa.sentence_simplicity).on_input()
    simplicity_out = Feedback(cspa.sentence_simplicity).on_output()
    is_simpler = Feedback(cspa.is_simpler).on_input_output()
    ps_ratio_out = Feedback(custom.pron_subjects_ratio).on_output()

    bertscore = Feedback(cmetr.bert_score).on_input_output()
    bleuscore = Feedback(cmetr.bleu).on_input_output()
    rougescore = Feedback(cmetr.rouge).on_input_output()
    perplexityscore = Feedback(cmetr.perplexity).on_output()

    simpleenglish = Feedback(cnlf.simple_english).on_output()
    nometaphors = Feedback(cnlf.no_metaphors).on_output()

    # feedbacks = [langmatch, piidetect, nottoxic, simplicity_in, simplicity_out, is_simpler, bertscore, bleuscore, rougescore, perplexityscore]
    feedbacks = [simplicity_in, simplicity_out, is_simpler, ps_ratio_out, bertscore, bleuscore, perplexityscore, simpleenglish, nometaphors]
    return feedbacks



def simplifyapp(original_text:str, verbose:bool=False):
    prompt_template = PromptTemplate(
            template=SIMPLE_ENGLISH_PROMPT['prompt_text'],
            input_variables=SIMPLE_ENGLISH_PROMPT['variables'],
        )
    
    llm = VertexAI()
    chain = LLMChain(llm=llm, prompt=prompt_template, verbose=verbose)
    llm_response = chain({'text':original_text})
    return llm_response['text'].strip()
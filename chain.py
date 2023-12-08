
from typing import List

from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub, VertexAI, VertexAIModelGarden
from langchain.prompts import PromptTemplate
from trulens_eval import Feedback, Huggingface

from custom_feedback import custom


def define_feedback()->List[Feedback]:
    hugs = Huggingface()
    langmatch = Feedback(hugs.language_match).on_input_output()
    # nottoxic = Feedback(hugs.not_toxic).on_output() # not used because there's a bug
    is_simpler = Feedback(custom.is_simpler).on_input_output()
    ps_ratio_out = Feedback(custom.pron_subjects_ratio).on_output()

    bleuscore = Feedback(custom.bleu).on_input_output()
    perplexityscore = Feedback(custom.perplexity).on_output()

    feedbacks = [langmatch, is_simpler, ps_ratio_out, bleuscore, perplexityscore]
    return feedbacks



def simplifyapp(original_text:str, verbose:bool=False):
    prompt_template = PromptTemplate(
            template="Rewrite the following sentece using simple english: {text}",
            input_variables=["text"],
        )
    llm = VertexAI()
    chain = LLMChain(llm=llm, prompt=prompt_template, verbose=verbose)
    llm_response = chain({'text':original_text})
    return llm_response['text'].strip()

from typing import List

from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub, VertexAI
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


from prompts import SIMPLE_CONCEPT_PROMPT, SIMPLE_ENGLISH_PROMPT


def simplifyapp(original_text:str):
    
    if len(original_text) < 50:
        return "Please input a longer text."
    
    prompt_template = PromptTemplate(
            template=SIMPLE_ENGLISH_PROMPT['prompt_text'],
            input_variables=SIMPLE_ENGLISH_PROMPT['variables'],
        )
    llm = VertexAI()
    chain = LLMChain(llm=llm, prompt=prompt_template)
    llm_response = chain({'text':original_text})
    return llm_response['text'].strip()


def simplifyapp_2(answer_text:str, concept:str):
    prompt_template = PromptTemplate(
            template=SIMPLE_CONCEPT_PROMPT['prompt_text'],
            input_variables=SIMPLE_CONCEPT_PROMPT['variables'],
        )
    llm = VertexAI(model_name="text-bison-32k")
    chain = LLMChain(llm=llm, prompt=prompt_template)
    llm_response = chain({'answer_text':answer_text, 'concept':concept})
    return llm_response['text'].strip()

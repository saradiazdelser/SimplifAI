import os
import re
from typing import List

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceTextGenInference, VertexAI
from trulens_eval import Feedback, Huggingface

from custom_feedback import custom
from prompts import all_prompts

mixtral_config = {
    "inference_server_url":"http://10.10.78.11:8081/",
    "max_new_tokens":512,
    "top_k":10,
    "top_p":0.95,
    "typical_p":0.95,
    "temperature":0.01,
}


hugs = Huggingface()

def define_feedback() -> List[Feedback]:
    langmatch = Feedback(hugs.language_match).on_input_output()
    
    not_toxic = Feedback(hugs.not_toxic).on_output()

    is_simpler = Feedback(custom.is_simpler).on_input_output()

    ps_ratio_out = Feedback(custom.pron_subjects_ratio).on_output()

    bleuscore = Feedback(custom.bleu).on_input_output()

    perplexityscore = Feedback(custom.perplexity).on_output()

    feedbacks = [is_simpler, ps_ratio_out, bleuscore, perplexityscore]

    return feedbacks


def format_response(llm_response:str)->str:
    # it's a known issue that mixtral generates lists
    llm_response = llm_response.replace(". ", ".\n")
    llm_response = re.sub(r"^\d\.\n|\n\d\.\n", "\n", llm_response).strip()
    return llm_response

def execute_chain(task:str, input:dict, format:bool=False)-> str:
    """Executes a chain for a given task"""
    provider = os.environ["ModelType"]
    
    if provider == "VertexAI":
        llm = VertexAI()

    elif provider == "CTC_Madrid":
        llm = HuggingFaceTextGenInference(**mixtral_config)
        
    else:
        raise Exception('Missing `ModelType` configuration setting. Please set the enviornment variable `ModelType`.\n export ModelType=\'CTC_Madrid\'')

    # set prompt
    prompt = all_prompts[provider][task]
    prompt_template = PromptTemplate(
        template=prompt["prompt_text"],
        input_variables=prompt["variables"],
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    llm_response = chain(input)["text"].strip()
    if format:
        llm_response = format_response(llm_response)
    return llm_response


def evaluate_response(input_text:str, output_text:str)-> str:
    llm_response = execute_chain('evaluate',{"input_text": input_text, "ouput_text":output_text}, format=False)
    return llm_response


def simplify_text(original_text: str, evaluate:bool=False)-> str:
    if len(original_text) < 50:
        return "Please input a longer text. Minimun 50 characters."

    llm_response = execute_chain('simplify',{'text':original_text})
    
    if evaluate:
        eval_response = evaluate_response(original_text, llm_response)
        print("\nRESPONSE:\n", llm_response, "\nEVALUATION\n", eval_response)

    return llm_response

def explain_term(answer_text: str, concept: str)-> str:
    llm_response = execute_chain('explain',{"answer_text": answer_text, "concept": concept})
    return llm_response



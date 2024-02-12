from typing import List
import os
import re
from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceTextGenInference, VertexAI
from langchain.prompts import PromptTemplate
from trulens_eval import Feedback, Huggingface
from custom_feedback import custom
from prompts import SIMPLE_CONCEPT_PROMPT, SIMPLE_ENGLISH_PROMPT, SIMPLE_CONCEPT_PROMPT_MIXTRAL, SIMPLE_ENGLISH_PROMPT_MIXTRAL, EVAL_PROMPT_MIXTRAL
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
    

def simplify_text(original_text: str):
    if len(original_text) < 50:
        return "Please input a longer text. Minimun 50 characters."

    if os.environ["ModelType"] == "VertexAI":
        llm = VertexAI()
        prompt_template = PromptTemplate(
            template=SIMPLE_ENGLISH_PROMPT["prompt_text"],
            input_variables=SIMPLE_ENGLISH_PROMPT["variables"],
        )

    elif os.environ["ModelType"] == "CTC_Madrid":
        llm = HuggingFaceTextGenInference(
            inference_server_url="http://10.10.78.11:8081/",
            max_new_tokens=512,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.01,
            # repetition_penalty=1.03,
        )
        prompt_template = PromptTemplate(
            template=SIMPLE_ENGLISH_PROMPT_MIXTRAL["prompt_text"],
            input_variables=SIMPLE_ENGLISH_PROMPT_MIXTRAL["variables"],
        )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    llm_response = chain({"text": original_text})
    llm_response = format_response(llm_response)
    
    # eval_response = evaluate_response(llm=llm,input_text=original_text,output_text=llm_response)
    # print("PROMPT:\n",prompt_template.template, "\nRESPONSE:\n", llm_response, "\nEVALUATION\n", eval_response)
    
    return llm_response


def format_response(llm_response:str)->str:
    # it's a known issue that mixtral generates lists
    llm_response = llm_response["text"].strip().replace(". ", ".\n")
    llm_response = re.sub(r"^\d\.\n|\n\d\.\n", "\n", llm_response).strip()
    return llm_response


def evaluate_response(llm, input_text, output_text):
    prompt_template = PromptTemplate(
        template=EVAL_PROMPT_MIXTRAL["prompt_text"],
        input_variables=EVAL_PROMPT_MIXTRAL["variables"],
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    eval_response = chain({"input_text": input_text, "ouput_text":output_text})

    return eval_response["text"].strip()

def explain_term(answer_text: str, concept: str):
    prompt_template = PromptTemplate(
        template=SIMPLE_CONCEPT_PROMPT["prompt_text"],
        input_variables=SIMPLE_CONCEPT_PROMPT["variables"],
    )

    if os.environ["ModelType"] == "VertexAI":
        llm = VertexAI()
        prompt_template = PromptTemplate(
            template=SIMPLE_CONCEPT_PROMPT["prompt_text"],
            input_variables=SIMPLE_CONCEPT_PROMPT["variables"],
        )


    elif os.environ["ModelType"] == "CTC_Madrid":
        llm = HuggingFaceTextGenInference(
            inference_server_url="http://10.10.78.11:8081/",
            max_new_tokens=512,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.01,
            # repetition_penalty=1.03,
        )
        prompt_template = PromptTemplate(
            template=SIMPLE_CONCEPT_PROMPT_MIXTRAL["prompt_text"],
            input_variables=SIMPLE_CONCEPT_PROMPT_MIXTRAL["variables"],
        )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    llm_response = chain({"answer_text": answer_text, "concept": concept})
    llm_response = format_response(llm_response)

    return llm_response

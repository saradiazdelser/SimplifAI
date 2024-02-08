from typing import List
import os
from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceTextGenInference, VertexAI
from langchain.prompts import PromptTemplate
from trulens_eval import Feedback
from custom_feedback import custom
from prompts import SIMPLE_CONCEPT_PROMPT, SIMPLE_ENGLISH_PROMPT


def define_feedback() -> List[Feedback]:
    is_simpler = Feedback(custom.is_simpler).on_input_output()

    ps_ratio_out = Feedback(custom.pron_subjects_ratio).on_output()

    bleuscore = Feedback(custom.bleu).on_input_output()

    perplexityscore = Feedback(custom.perplexity).on_output()

    feedbacks = [is_simpler, ps_ratio_out, bleuscore, perplexityscore]

    return feedbacks


def simplify_text(original_text: str):
    if len(original_text) < 50:
        return "Please input a longer text. Minimun 50 characters."

    prompt_template = PromptTemplate(
        template=SIMPLE_ENGLISH_PROMPT["prompt_text"],
        input_variables=SIMPLE_ENGLISH_PROMPT["variables"],
    )

    if os.environ["ModelType"] == "VertexAI":
        llm = VertexAI()

    elif os.environ["ModelType"] == "CTC_Madrid":
        llm = HuggingFaceTextGenInference(
            inference_server_url="http://10.10.78.11:8081/",
            max_new_tokens=512,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.01,
            repetition_penalty=1.03,
        )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    llm_response = chain({"text": original_text})

    return llm_response["text"].strip()


def explain_term(answer_text: str, concept: str):
    prompt_template = PromptTemplate(
        template=SIMPLE_CONCEPT_PROMPT["prompt_text"],
        input_variables=SIMPLE_CONCEPT_PROMPT["variables"],
    )

    if os.environ["ModelType"] == "VertexAI":
        llm = VertexAI()

    elif os.environ["ModelType"] == "CTC_Madrid":
        llm = HuggingFaceTextGenInference(
            inference_server_url="http://10.10.78.11:8081/",
            max_new_tokens=512,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.01,
            repetition_penalty=1.03,
        )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    llm_response = chain({"answer_text": answer_text, "concept": concept})

    return llm_response["text"].strip()

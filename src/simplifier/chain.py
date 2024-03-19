import logging
import re
import time
from typing import List

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceTextGenInference, VertexAI
from trulens_eval import Feedback, Huggingface

from src.config import Configuration
from src.evaluation import custom
from src.simplifier.prompts import all_prompts

config = Configuration()

hugs = Huggingface()


def define_feedback() -> List[Feedback]:
    langmatch = Feedback(hugs.language_match).on_input_output()
    not_toxic = Feedback(hugs.not_toxic).on_output()
    is_simpler = Feedback(custom.is_simpler).on_input_output()
    ps_ratio_out = Feedback(custom.pron_subjects_ratio).on_output()
    bleuscore = Feedback(custom.bleu).on_input_output()
    perplexityscore = Feedback(custom.perplexity).on_output()

    requirement_1 = Feedback(custom.one_idea_sentence).on_output()
    requirement_2 = Feedback(custom.explicit_subject).on_output()
    requirement_3 = Feedback(custom.short_sentence).on_output()
    requirement_4 = Feedback(custom.no_negations).on_output()
    requirement_5 = Feedback(custom.no_many_numbers).on_output()
    requirement_8 = Feedback(custom.technical_terms).on_output()

    feedbacks = [
        is_simpler,
        ps_ratio_out,
        bleuscore,
        perplexityscore,
        requirement_1,
        requirement_2,
        requirement_3,
        requirement_4,
        requirement_5,
        requirement_8,
    ]

    return feedbacks


def format_response(llm_response: str) -> str:
    # it's a known issue that mixtral generates lists and/or numbered paragraphs, this removes them
    llm_response = llm_response.replace(". ", ".\n")
    llm_response = re.sub(
        r"^\d\.\n|\n\d\.\n|\n\d\d\.\n|\n *[-*] *\w", "\n", llm_response
    ).strip()
    return llm_response


def execute_chain(task: str, input: dict, format: bool = True) -> str:
    """Executes a chain for a given task"""
    llm = HuggingFaceTextGenInference(**config.LLM_CONFIG)
    # set prompt
    prompt = all_prompts[task]
    prompt_template = PromptTemplate(
        template=prompt["prompt_text"],
        input_variables=prompt["variables"],
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    llm_response = chain(input)["text"].strip()
    logging.info(
        f"PromptTemplate:\n{prompt_template.template}\nInput:\n{input}\nOutput:\n{llm_response}"
    )

    if format:
        llm_response = format_response(llm_response)
        logging.info(f"Formatted Response.\nOutput:\n{llm_response}")

    return llm_response


def output_parser(output_text: str) -> float:
    """Extracts numerical score from LLM response text"""
    m = re.search("\d+", output_text)
    if m:
        return float(m.group())
    return 0.0


def evaluate_response(input_text: str, output_text: str) -> str:
    eval_response = execute_chain(
        "evaluate", {"input_text": input_text, "ouput_text": output_text}, format=False
    )
    print("\nRESPONSE:\n", output_text, "\nEVALUATION\n", eval_response)


def simplify_text(original_text: str, evaluate: bool = False) -> str:
    if len(original_text) < 50:
        return "Please input a longer text. Minimun 50 characters."

    start_time = time.time()
    output_text = execute_chain("simplify", {"text": original_text})
    logging.info(
        f"LLM call finished. Task: simplify. Took {time.time() - start_time} s"
    )

    # Second Round
    # start_time = time.time()
    # eval_response = execute_chain('evaluate',{"input_text": original_text, "ouput_text":output_text}, format=False)
    # logging.info(f"LLM call finished. Task: evaluate. Took {time.time() - start_time} s")
    # score = output_parser(eval_response)
    # print(f'Score: {score}. Explanation: {eval_response}')

    # if score <7:
    #     logging.info(f'Second round. Score: {score}')
    #     start_time = time.time()
    #     output_text = execute_chain('simplify',{'text':output_text})
    #     logging.info(f"LLM call finished. Task: simplify. Took {time.time() - start_time} s")

    if evaluate:
        evaluate_response(original_text, output_text)

    return output_text


def explain_term(answer_text: str, concept: str) -> str:
    start_time = time.time()
    llm_response = execute_chain(
        "explain", {"answer_text": answer_text, "concept": concept}
    )
    logging.info(f"LLM call finished. Task: explain. Took {time.time() - start_time} s")

    # Split the response into lines
    response_lines = llm_response.split("\n")

    # Ensure the response has at most 10 lines
    if len(response_lines) > 10:
        llm_response = "\n".join(response_lines[:10])

    return llm_response

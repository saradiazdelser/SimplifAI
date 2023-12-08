
from typing import List

from custom_feedback import custom
from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub, VertexAIModelGarden
from langchain.prompts import PromptTemplate
from trulens_eval import Feedback, Huggingface


def define_feedback()->List[Feedback]:
    hugs = Huggingface()

    langmatch = Feedback(hugs.language_match).on_input_output()
    piidetect = Feedback(hugs.pii_detection).on_input()
    nottoxic = Feedback(hugs.not_toxic).on_output()

    simplicity_in = Feedback(custom.sentence_simplicity).on_input()
    simplicity_out = Feedback(custom.sentence_simplicity).on_output()
    is_simpler = Feedback(custom.is_simpler).on_input_output()

    bertscore = Feedback(custom.bert_score).on_input_output()
    bleuscore = Feedback(custom.bleu).on_input_output()
    rougescore = Feedback(custom.rouge).on_input_output()
    perplexityscore = Feedback(custom.perplexity).on_output()

    # feedbacks = [langmatch, piidetect, nottoxic, simplicity_in, simplicity_out, is_simpler, bertscore, bleuscore, rougescore, perplexityscore]
    feedbacks = [langmatch, nottoxic, simplicity_in, simplicity_out, is_simpler, bertscore, bleuscore, perplexityscore]
    return feedbacks



def simplifyapp(original_text:str, verbose:bool=False):
    prompt_template = PromptTemplate(
            template="Rewrite the following sentece using simple english: {text}",
            input_variables=["text"],
        )
    
    # llm = VertexAIModelGarden(
    #     project=VERTEXAI_PROJECT, 
    #     endpoint_id=VERTEXAI_ENDPOINT_ID, 
    #     allowed_model_args={
    #         "max_tokens": 50,
    #         "temperature": 1.0,
    #         "top_p": 1.0,
    #         "top_k": 10,        
    #     })
    
    llm = HuggingFaceHub(    
        repo_id="tiiuae/falcon-7b-instruct", model_kwargs={"temperature":0.9, "max_length": 128}
    )

    chain = LLMChain(llm=llm, prompt=prompt_template, verbose=verbose)
    llm_response = chain({'text':original_text})
    return llm_response['text'].strip()
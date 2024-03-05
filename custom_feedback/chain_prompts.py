import re

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceTextGenInference

mixtral_config = {
    "inference_server_url":"http://10.10.78.11:8081/",
    "max_new_tokens":10,
    "top_k":7,
    "top_p":0.95,
    "typical_p":0.95,
    "temperature": 0.1,
}

def output_parser(output_text:str) -> float:
    """Extracts numerical score from LLM response text"""
    m = re.search('\d+', output_text)
    if m:
        return float(m.group())
    return 0.0

def execute_chain(simplified_text:str, prompt:dict)-> float:
    """Executes a chain using the Mixtral model and the given input text (str) and prompt (dict)."""
    
    llm = HuggingFaceTextGenInference(**mixtral_config)
    
    # set prompt
    prompt_template = PromptTemplate(
        template=prompt['prompt_text'],
        input_variables=['variables'],
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    llm_response = chain({'text':simplified_text})
    llm_response = llm_response["text"].strip()
    
    score = output_parser(llm_response)

    return score


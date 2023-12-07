import os
import json
import tempfile
import gradio as gr
from google.cloud import aiplatform
from google.oauth2.service_account import Credentials
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import VertexAIModelGarden, HuggingFaceHub
from IPython.display import JSON
from trulens_eval import Feedback, Huggingface, Tru
from typing import List
from custom_feedback import custom
from trulens_eval import Huggingface
from trulens_eval.feedback.provider.hugs import Dummy

## Initalizing of Trulens
tru = Tru()
tru.reset_database()
CREDENTIAL_FILE_PATH = '' #! <--- CREDENTIALS HERE

#Use this to lines if you want to run it locally
from helper_functions.set_env_variables import load_env_variables
load_env_variables()

def define_feedback()->List[Feedback]:
    # hugs = Huggingface()
    hugs = Dummy()
    langmatch = Feedback(hugs.language_match).on_input_output()
    piidetect = Feedback(hugs.pii_detection).on_input()
    nottoxic = Feedback(hugs.not_toxic).on_output()

    simplicity_in = Feedback(custom.sentence_simplicity).on_input()
    simplicity_out = Feedback(custom.sentence_simplicity).on_output()
    is_simpler = Feedback(custom.is_simpler).on_input_output()
    ps_ratio_out = Feedback(custom.pron_subjects_ratio).on_output()

    bertscore = Feedback(custom.bert_score).on_input_output()
    bleuscore = Feedback(custom.bleu).on_input_output()
    rougescore = Feedback(custom.rouge).on_input_output()
    perplexityscore = Feedback(custom.perplexity).on_output()

    # feedbacks = [langmatch, piidetect, nottoxic, simplicity_in, simplicity_out, is_simpler, bertscore, bleuscore, rougescore, perplexityscore]
    feedbacks = [simplicity_in, simplicity_out, is_simpler, ps_ratio_out, bertscore, bleuscore, perplexityscore]
    return feedbacks

feedbacks = define_feedback()

print(os.environ['TestVariable'])
PROJECT_NUMBER = str(os.environ['PROJECT_NUMBER'])
ENDPOINT_ID = str(os.environ['ENDPOINT_ID'])
LOCATION = str(os.environ['LOCATION'])

# process of getting credentials
def get_credentials():
    creds_json_str = os.getenv("CREDENTIALS_JSON") # get json credentials stored as a string
    if creds_json_str is None:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_JSON not found in environment")

    # create a temporary file
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as temp:
        temp.write(creds_json_str) # write in json format
        temp_filename = temp.name 

    return temp_filename
    
# pass
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= get_credentials()



from langchain.llms import VertexAI
version = 2
def simplifyapp(original_text:str, verbose:bool=False):
    prompt_template = PromptTemplate(
            template="""Context:
                        Simple English Wikipedia is a version of the popular online encyclopedia, Wikipedia, that aims to present information in a language that is easy to understand for individuals with limited proficiency in English or those who are learning the language. Articles on Simple English Wikipedia are written with shorter sentences, simpler vocabulary, and a straightforward structure, making the content more accessible to a diverse audience. The primary goal is to provide clear and concise information on a wide range of topics, catering to readers who may find the regular English Wikipedia more challenging to comprehend. The simplicity of language in Simple English Wikipedia is intended to facilitate learning and understanding for a broad audience.
                        Instruction: Translate the input text to Simple English Wikipedia format. Make sure it complies with the following requirements:
                        - Express only one idea per sentence.
                        - One sentence per line.
                        - Make sure the subject of each sentence it is explicit. Do not use pronouns as subjects.
                        - Use short sentences and simple language
                        - Avoid negative sentences
                        - Avoid using too many numbers or mathematical denominations. If there is no choice but to insert a number, always use digits.
                        - Do not use confusing metaphors or comparisons.
                        - Use only one message per sentence.
                        - Be clear, concise and direct.
                        - Use simple and direct language.
                        - Avoid technical terms, abbreviations and initials.
                        - The content must follow a clear and coherent order.
                        - All unnecessary ideas, words, sentences or phrases should be avoided or deleted.
                        - Explain in a simple way by means of a vocabulary, if necessary, those words that are words that are considered somewhat difficult to understand.
                        Input text:
                        {text}
                        Output: """,
            input_variables=["text"],
        )
    llm = VertexAI()
    chain = LLMChain(llm=llm, prompt=prompt_template, verbose=verbose)
    llm_response = chain({'text':original_text})
    return llm_response['text'].strip()

def simplifyapp_2(answer_text:str, concept:str):
    #answer_text = original_text[0]
    #concept = original_text[1]
    
    prompt_template = PromptTemplate(
            template=    """Context:
                Simple English Wikipedia is a version of the popular online encyclopedia, Wikipedia, that aims to present information in a language that is easy to understand for individuals with limited proficiency in English or those who are learning the language. Articles on Simple English Wikipedia are written with shorter sentences, simpler vocabulary, and a straightforward structure, making the content more accessible to a diverse audience. The primary goal is to provide clear and concise information on a wide range of topics, catering to readers who may find the regular English Wikipedia more challenging to comprehend. The simplicity of language in Simple English Wikipedia is intended to facilitate learning and understanding for a broad audience.
                Instruction: Define the input concept with simple English Wikipedia format given the input context. Make sure it complies with the following requirements:
                - Express only one idea per sentence.
                - Make sure the subject of each sentence it is explicit. Do not use pronouns as subjects.
                - Use short sentences and simple language
                - Avoid negative sentences
                - Avoid using too many numbers or mathematical denominations. If there is no choice but to insert a number, always use digits.
                - Do not use confusing metaphors or comparisons.
                - Use only one message per sentence.
                - Be clear, concise and direct.
                - Use simple and direct language.
                - Avoid technical terms, abbreviations and initials.
                - The content must follow a clear and coherent order.
                - All unnecessary ideas, words, sentences or phrases should be avoided or deleted.
                - Explain in a simple way by means of a vocabulary, if necessary, those words that are words that are considered somewhat difficult to understand.
                Input context: {answer_text}
                Input concept: {concept}
                Output:""",
            input_variables=["answer_text", "concept"],
        )
    llm = VertexAI(model_name="text-bison-32k")
    chain = LLMChain(llm=llm, prompt=prompt_template)
    llm_response = chain({'answer_text':answer_text, 'concept':concept})
    return llm_response['text'].strip()



from trulens_eval import TruBasicApp
recorder = TruBasicApp(simplifyapp, app_id=f"simplify-app-v{version}", feedbacks=feedbacks)


def predict(text):
    with recorder as recording:
        rec = recorder.app(text)

    return rec

# ### Gradio Theme
# theme = gr.themes.Base(
#     primary_hue="violet",
#     font=[gr.themes.GoogleFont('San Serif'), 'ui-sans-serif', 'system-ui', 'sans-serif'],
#     # Different Fonts I tried: Archivo Black, Anton
# ).set(
#     button_secondary_border_color='*primary_800'
# )

def get_trulens_feedback():
    return tru.get_records_and_feedback(app_ids=[f'simplify-app-v{version}'])[0]
    
with gr.Blocks() as demo:

    gr.Image(value="backend/logo.png", width=60)
    gr.Markdown("# Simplif AI")
        

    with gr.Tab("Input"):

        gr.Markdown("### Let's go and simplif-AI")

        input_textbox = gr.Textbox(lines=5, placeholder="Put your complicated text here...")
        submit_butn = gr.Button("Submit")
        output_textbox = gr.Textbox()

        submit_butn.click(fn=predict, inputs=input_textbox, outputs=output_textbox)

        gr.Markdown("### Get a Definition for a concept")

        with gr.Row():
            wd_input_textbox = gr.Textbox(lines=1, placeholder="Put a concept that you don't understand here...")
            wd_submit_butn = gr.Button("Submit")
        wd_output_textbox = gr.Textbox()

        wd_submit_butn.click(fn=simplifyapp_2, inputs=[output_textbox, wd_input_textbox], outputs=wd_output_textbox)


    with gr.Tab("About the App"):
        gr.Markdown("This App converts any given text into 'plain language', a simplified form of writing designed to enhance understanding for people with diverse cognitive abilities.")
        gr.Markdown("## Introduction")
        gr.Markdown("Many individuals with learning or mental disabilities encounter difficulties in comprehending standard English text, limiting their access to information and hindering effective communication. To tackle this issue, we propose a user-friendly web application that effortlessly converts any given English text into 'Plain English,' a simplified form of writing designed to enhance understanding for people with diverse cognitive abilities. By doing so, we aim to ensure that information is not only accessible but also inclusive. The target audience for our web app is broad, encompassing individuals with learning or mental disabilities, caregivers, educators, and anyone aiming to communicate with a diverse audience. By catering to the needs of this demographic, our application fosters inclusivity and ensures that information is comprehensible to a wider spectrum of users. The unique benefit lies in the simplicity of our solution – a tool that makes information universally accessible, bridging the gap and promoting a more inclusive digital environment.")
        gr.Markdown("Visit our [GitHub](https://github.com/saradiazdelser/SimplifAI/)")

    with gr.Tab("Trulens Metrics"):

        tl_submit_butn = gr.Button("Get Trulens Metrics")
        tl_output_textbox = gr.Textbox()

        tl_submit_butn.click(fn=get_trulens_feedback, outputs=tl_output_textbox)

        

        


demo.launch()
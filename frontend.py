
import os

run_in_huggingface = False


##Use this lines if you want to run it on huggingface spaces
if run_in_huggingface == True:
    os.system("pip uninstall -y gradio")
    os.system("pip install gradio==3.36.0")
    os.system("pip uninstall -y pydantic")
    os.system("pip install pydantic==1.10.13")
    os.system("python -m spacy download en_core_web_sm")

##Use this to lines if you want to run it locally
else:
    from helper_functions.set_env_variables import load_env_variables
    load_env_variables()

# All needed imports
import json
import tempfile
from typing import List

import gradio as gr
from google.cloud import aiplatform
from google.oauth2.service_account import Credentials
from IPython.display import JSON
from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub, VertexAIModelGarden
from langchain.prompts import PromptTemplate
from trulens_eval import Feedback, Huggingface, Tru
from trulens_eval.feedback.provider.hugs import Dummy

from custom_feedback import custom

#Setting up the environment secrets
print(os.environ['TestVariable'])
PROJECT_NUMBER = str(os.environ['PROJECT_NUMBER'])
ENDPOINT_ID = str(os.environ['ENDPOINT_ID'])
LOCATION = str(os.environ['LOCATION'])

## process of getting credentials
def get_credentials():
    creds_json_str = os.getenv("CREDENTIALS_JSON") # get json credentials stored as a string
    if creds_json_str is None:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_JSON not found in environment")

    # create a temporary file
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as temp:
        temp.write(creds_json_str) # write in json format
        temp_filename = temp.name 

    return temp_filename
    
## pass
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= get_credentials()


# Trulens functions
## Initalizing of Trulens
tru = Tru()
# tru.reset_database()


# Feedback Functions
from chain import define_feedback

feedbacks = define_feedback() # import all feedback functions from chain module to avoid clutter


### Observability
from observability.observability import GradioHTML, SimpleEnglishClassifier


def classify(text):
    classifier_id = 'saradiaz/distilbert-base-uncased-simpleEng-classifier'
    task = SimpleEnglishClassifier(model_path=classifier_id, resolution=5)
    title, results = task.visualization(texts=[text], output_type=GradioHTML())
    attributions = results[1:]
    return attributions


# Communication with the model
version = 5
from trulens_eval import TruBasicApp

from chain import simplifyapp, simplifyapp_2

# from langchain.llms import VertexAI
# def simplifyapp(original_text:str):
#     prompt_template = PromptTemplate(
#             template="""Context:
#                         Simple English Wikipedia is a version of the popular online encyclopedia, Wikipedia, that aims to present information in a language that is easy to understand for individuals with limited proficiency in English or those who are learning the language. Articles on Simple English Wikipedia are written with shorter sentences, simpler vocabulary, and a straightforward structure, making the content more accessible to a diverse audience. The primary goal is to provide clear and concise information on a wide range of topics, catering to readers who may find the regular English Wikipedia more challenging to comprehend. The simplicity of language in Simple English Wikipedia is intended to facilitate learning and understanding for a broad audience.
#                         Instruction: Translate the input text to Simple English Wikipedia format. Make sure it complies with the following requirements:
#                         - Express only one idea per sentence.
#                         - One sentence per line.
#                         - Make sure the subject of each sentence it is explicit. Do not use pronouns as subjects.
#                         - Use short sentences and simple language
#                         - Avoid negative sentences
#                         - Avoid using too many numbers or mathematical denominations. If there is no choice but to insert a number, always use digits.
#                         - Do not use confusing metaphors or comparisons.
#                         - Use only one message per sentence.
#                         - Be clear, concise and direct.
#                         - Use simple and direct language.
#                         - Avoid technical terms, abbreviations and initials.
#                         - The content must follow a clear and coherent order.
#                         - All unnecessary ideas, words, sentences or phrases should be avoided or deleted.
#                         - Explain in a simple way by means of a vocabulary, if necessary, those words that are words that are considered somewhat difficult to understand.
#                         Input text:
#                         {text}
#                         Output: """,
#             input_variables=["text"],
#         )
#     llm = VertexAI()
#     chain = LLMChain(llm=llm, prompt=prompt_template)
#     llm_response = chain({'text':original_text})
#     return llm_response['text'].strip()

# def simplifyapp_2(answer_text:str, concept:str):
#     #answer_text = original_text[0]
#     #concept = original_text[1]
    
#     prompt_template = PromptTemplate(
#             template=    """Context:
#                 Simple English Wikipedia is a version of the popular online encyclopedia, Wikipedia, that aims to present information in a language that is easy to understand for individuals with limited proficiency in English or those who are learning the language. Articles on Simple English Wikipedia are written with shorter sentences, simpler vocabulary, and a straightforward structure, making the content more accessible to a diverse audience. The primary goal is to provide clear and concise information on a wide range of topics, catering to readers who may find the regular English Wikipedia more challenging to comprehend. The simplicity of language in Simple English Wikipedia is intended to facilitate learning and understanding for a broad audience.
#                 Instruction: Define the input concept with simple English Wikipedia format given the input context. Make sure it complies with the following requirements:
#                 - Express only one idea per sentence.
#                 - Make sure the subject of each sentence it is explicit. Do not use pronouns as subjects.
#                 - Use short sentences and simple language
#                 - Avoid negative sentences
#                 - Avoid using too many numbers or mathematical denominations. If there is no choice but to insert a number, always use digits.
#                 - Do not use confusing metaphors or comparisons.
#                 - Use only one message per sentence.
#                 - Be clear, concise and direct.
#                 - Use simple and direct language.
#                 - Avoid technical terms, abbreviations and initials.
#                 - The content must follow a clear and coherent order.
#                 - All unnecessary ideas, words, sentences or phrases should be avoided or deleted.
#                 - Explain in a simple way by means of a vocabulary, if necessary, those words that are words that are considered somewhat difficult to understand.
#                 Input context: {answer_text}
#                 Input concept: {concept}
#                 Output:""",
#             input_variables=["answer_text", "concept"],
#         )
#     llm = VertexAI(model_name="text-bison-32k")
#     chain = LLMChain(llm=llm, prompt=prompt_template)
#     llm_response = chain({'answer_text':answer_text, 'concept':concept})
#     return llm_response['text'].strip()



recorder = TruBasicApp(simplifyapp, app_id=f"simplifAI-app-v{version}", feedbacks=feedbacks)

def predict(text):
    with recorder as recording:
        rec = recorder.app(text)

    return rec


def get_trulens_feedback():
    df = tru.get_records_and_feedback(app_ids=[f'simplifAI-app-v{version}'])[0] # pass an empty list of app_ids to get all

    #column_names = df.columns.tolist()
    #print(column_names)

    try: sub_df = df.loc[: ,['sentence_simplicity',
        'pron_subjects_ratio',
        'is_simpler','bleu', 'perplexity']]
    except:
        sub_df = df.loc[: ,['sentence_simplicity',
        'pron_subjects_ratio',
        'is_simpler',]]

    return sub_df, df.loc[0, 'output']

# ### Gradio Theme
# theme = gr.themes.Base(
#     primary_hue="violet",
#     font=[gr.themes.GoogleFont('San Serif'), 'ui-sans-serif', 'system-ui', 'sans-serif'],
#     # Different Fonts I tried: Archivo Black, Anton
# ).set(
#     button_secondary_border_color='*primary_800'
# )

# Gradio UI for the fronted
with gr.Blocks() as demo:


    # with open("logo.html") as f:
    #     HTML_LOGO = f.read().strip()
 
    # gr.HTML(HTML_LOGO)

    gr.Image(value="logo.png", width=60)
    gr.Markdown("# Simplif AI 📝➡️✅")
        

    with gr.Tab("Input"):

        gr.Markdown("### Let's go and simplif-AI")

        input_textbox = gr.Textbox(lines=5, placeholder="Put your complicated text here...")
        submit_butn = gr.Button("Submit")
        output_textbox = gr.Textbox()

        submit_butn.click(fn=predict, inputs=input_textbox, outputs=output_textbox)

        gr.Markdown("### Get a definition for a concept")

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
        tl_output_textbox = gr.TextArea(label="Output:")
        tl_dataframe = gr.Dataframe()

        tl_submit_butn.click(fn=get_trulens_feedback, outputs=[tl_dataframe, tl_output_textbox])

    with gr.Tab("Observability"):

        gr.Markdown("Visualization of Attribution for Complexity by token. Generated using TruLen Explainability's implementation of Integrated Gradients.")
        input_textbox = gr.Textbox(lines=5, placeholder="Put your text here...")
        submit_butn2 = gr.Button("Submit")
        explain_output = gr.HighlightedText(
            label='COMPLEXITY ATTRIBUTION',
            interactive=True,
            combine_adjacent=True,
            show_legend=True)

        submit_butn2.click(fn=classify, inputs=input_textbox, outputs=explain_output)

demo.launch()
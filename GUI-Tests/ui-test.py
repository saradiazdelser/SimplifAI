import json
import os
import tempfile

import gradio as gr
from google.cloud import aiplatform
from google.oauth2.service_account import Credentials
#Use this to lines if you want to run it locally
from set_env_variables import load_env_variables

load_env_variables()

#import apiclient
#from google.oauth2 import service_account

# just a test function that simulates a prediction
#def predict(text):
#    return text + "this is the output of the model"

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



def classify(text):
    # calls the observability function
    return [('[CLS]', 0.0),
                 ('gothic', -4.6),
                 ('architecture', -6.2),
                 ('is', 1.7999999999999998),
                 ('an', 1.0),
                 ('architectural', -4.9),
                 ('style', -6.800000000000001),
                 ('that', -2.6),
                 ('was', -1.6),
                 ('prevalent', -8.7),
                 ('in', -2.6),
                 ('europe', 0.4),
                 (',', -1.6),
                 ('during', -2.9000000000000004),
                 ('the', -1.7000000000000002),
                 ('high', -2.6),
                 ('and', -1.7999999999999998),
                 ('of', -3.2),
                 ('classical', -5.4),
                 ('antiquity', -4.2)
           ]



def get_text_output_from_prediction(model_output):
    return model_output[0].split("Output:")[1]


def predict(text):
    instances = [
        {
            "prompt": text ,
            "max_tokens": 150,
            "temperature": 1.0,
            "top_p": 1.0,
            "top_k": 10,
        },
    ]
    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}",
        )
    response = endpoint.predict(instances=instances)
    return get_text_output_from_prediction(response.predictions)

### Gradio Theme
theme = gr.themes.Base(
    primary_hue="violet",
    font=[gr.themes.GoogleFont('San Serif'), 'ui-sans-serif', 'system-ui', 'sans-serif'],
    # Different Fonts I tried: Archivo Black, Anton
).set(
    button_secondary_border_color='*primary_800'
)

    
with gr.Blocks(theme=theme) as demo:

    gr.Markdown("## Simplif AI")

    with gr.Tab("Input"):

        gr.Markdown("### Let's go and simplif-AI")

        input_textbox = gr.Textbox(lines=5, placeholder="Put your complicated text here...")
        submit_butn = gr.Button("Submit")
        output_textbox = gr.Textbox()

        submit_butn.click(fn=predict, inputs=input_textbox, outputs=output_textbox)



    with gr.Tab("About the App"):
        gr.Markdown("This App converts any given text into 'plain language', a simplified form of writing designed to enhance understanding for people with diverse cognitive abilities.")
        gr.Markdown("## Introduction")
        gr.Markdown("Many individuals with learning or mental disabilities encounter difficulties in comprehending standard English text, limiting their access to information and hindering effective communication. To tackle this issue, we propose a user-friendly web application that effortlessly converts any given English text into 'Plain English,' a simplified form of writing designed to enhance understanding for people with diverse cognitive abilities. By doing so, we aim to ensure that information is not only accessible but also inclusive. The target audience for our web app is broad, encompassing individuals with learning or mental disabilities, caregivers, educators, and anyone aiming to communicate with a diverse audience. By catering to the needs of this demographic, our application fosters inclusivity and ensures that information is comprehensible to a wider spectrum of users. The unique benefit lies in the simplicity of our solution – a tool that makes information universally accessible, bridging the gap and promoting a more inclusive digital environment.")
        gr.Markdown("Visit our [GitHub](https://github.com/saradiazdelser/SimplifAI/)")


    with gr.Tab("Observability"):

        gr.Markdown("Visualization of Attribution for Complexity by token. Generated using TruLen Evaluation's implementation of Integrated Gradients.")
        input_textbox = gr.Textbox(lines=5, placeholder="Put your text here...")
        submit_butn2 = gr.Button("Submit")
        explain_output = gr.HighlightedText(
            label='COMPLEXITY ATTRIBUTION',
            interactive=True,
            combine_adjacent=True,
            show_legend=True)

        submit_butn2.click(fn=classify, inputs=input_textbox, outputs=explain_output)


demo.launch()
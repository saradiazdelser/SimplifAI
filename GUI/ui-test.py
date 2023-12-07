import os
import json
import tempfile
import gradio as gr
from google.cloud import aiplatform
from google.oauth2.service_account import Credentials
#import apiclient
#from google.oauth2 import service_account

# just a test function that simulates a prediction
#def predict(text):
#    return text + "this is the output of the model"

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

        gr.Interface(
                    fn=predict, 
                    inputs=gr.Textbox(lines=5, placeholder="Put your complicated text here..."),
                    outputs="text",
        )

    with gr.Tab("About the App"):

        gr.Markdown("This App converts any given text into 'plain language', a simplified form of writing designed to enhance understanding for people with diverse cognitive abilities.")

        gr.Markdown("## Introduction")

        gr.Markdown("Many individuals with learning or mental disabilities encounter difficulties in comprehending standard English text, limiting their access to information and hindering effective communication. To tackle this issue, we propose a user-friendly web application that effortlessly converts any given English text into 'Plain English,' a simplified form of writing designed to enhance understanding for people with diverse cognitive abilities. By doing so, we aim to ensure that information is not only accessible but also inclusive. The target audience for our web app is broad, encompassing individuals with learning or mental disabilities, caregivers, educators, and anyone aiming to communicate with a diverse audience. By catering to the needs of this demographic, our application fosters inclusivity and ensures that information is comprehensible to a wider spectrum of users. The unique benefit lies in the simplicity of our solution – a tool that makes information universally accessible, bridging the gap and promoting a more inclusive digital environment.")

        gr.Markdown("Visit our [GitHub](https://github.com/saradiazdelser/SimplifAI/)")



demo.launch()
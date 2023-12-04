import gradio as gr
from google.cloud import aiplatform

model_id = "your-model-id"
endpoint_id = "your-endpoint-id"

# just a test function that simulates a prediction
def predict(text):
    return text + "this is the output of the model"

"""
def predict(text):
    endpoint = aiplatform.Endpoint(endpoint_id)
    response = endpoint.predict(instances=[text])
    return response.predictions[0]
"""


iface = gr.Interface(fn=predict, inputs="text", outputs="text")
iface.launch()
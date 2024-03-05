import logging
import os
import tempfile

import gradio as gr
import pandas as pd
from trulens_eval import Tru, TruBasicApp

from chain import define_feedback, explain_term, simplify_text
from helper_functions.set_env_variables import load_env_variables
from observability.observability import GradioHTML, SimpleEnglishClassifier

logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s')

# uncomment these lines if running on HuggingFace
# os.system("pip uninstall -y gradio")
# os.system("pip install gradio==3.36.0")
# os.system("pip uninstall -y pydantic")
# os.system("pip install pydantic==1.10.13")
# os.system("python -m spacy download en_core_web_sm")


load_env_variables()

# Setting up the environment secrets
PROJECT_NUMBER = str(os.environ["PROJECT_NUMBER"])
ENDPOINT_ID = str(os.environ["ENDPOINT_ID"])
LOCATION = str(os.environ["LOCATION"])


# process of getting credentials
def get_credentials():
    creds_json_str = os.getenv("CREDENTIALS_JSON")

    if creds_json_str is None:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_JSON not found in environment")

    # create a temporary file
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as temp:
        temp.write(creds_json_str)
        temp_filename = temp.name

    return temp_filename


def classify(text):
    classifier_id = "saradiaz/distilbert-base-uncased-simpleEng-classifier"
    task = SimpleEnglishClassifier(model_path=classifier_id, resolution=5)
    _, results = task.visualization(texts=[text], output_type=GradioHTML())
    attributions = results[1:]
    return attributions


def predict(text):
    with recorder as recording:
        rec = recorder.app(text)
    return rec


def get_trulens_feedback():
    # pass an empty list of app_ids to get all
    df = tru.get_records_and_feedback(app_ids=[f"simplifAI-app-v{version}"])[0]

    interesting_metrcs = ["language_match","pron_subjects_ratio","is_simpler","bleu","perplexity",
                          "one_idea_sentence", "explicit_subject","short_sentence","no_negations",
                        "no_many_numbers","technical_terms"]
    
    sub_df = pd.DataFrame()
    for metric in interesting_metrcs:
        try: 
            sub_df[metric] = df[metric]
        except:
            print(f"Didn't found {metric} in TruLens result")

    return sub_df.iloc[-1:], df.loc[len(df.index) - 1]["output"]


# load google credentials
if os.environ["ModelType"] == "VertexAI":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_credentials()

# Trulens functions
tru = Tru()

# load the feedback functions
feedbacks = define_feedback()

# Communication with the model
version = 5

recorder = TruBasicApp(
    simplify_text, app_id=f"simplifAI-app-v{version}", feedbacks=feedbacks
)


# Gradio Theme
theme = gr.themes.Default(
    primary_hue=gr.themes.colors.emerald,
    secondary_hue=gr.themes.colors.green,
)


title = """
<picture>
  <img alt="Logo" src="https://raw.githubusercontent.com/saradiazdelser/SimplifAI/main/logo.png" style="width: 14%; margin-bottom: 10px;" />
</picture>

# Let's go and simplif-AI
Our application can be used to simplify texts to make them more accessible
"""

# Gradio UI for the fronted
with gr.Blocks(theme=theme) as demo:
    gr.Markdown(title)

    with gr.Tab("Input"):

        input_textbox = gr.Textbox(
            lines=5, placeholder="Put your complicated text here..."
        )
        submit_butn = gr.Button("Submit")
        output_textbox = gr.Textbox()

        submit_butn.click(fn=predict, inputs=input_textbox, outputs=output_textbox)

        gr.Markdown("### Get a definition for a concept")

        with gr.Row():
            wd_input_textbox = gr.Textbox(
                lines=1, placeholder="Put a concept that you don't understand here..."
            )
            wd_submit_butn = gr.Button("Submit")
        wd_output_textbox = gr.Textbox()

        wd_submit_butn.click(
            fn=explain_term,
            inputs=[output_textbox, wd_input_textbox],
            outputs=wd_output_textbox,
        )

    with gr.Tab("About the App"):
        gr.Markdown(open('README.md', 'r').read())
        gr.Markdown("Visit our [GitHub](https://github.com/saradiazdelser/SimplifAI/)")

    with gr.Tab("Trulens Metrics"):

        tl_submit_butn = gr.Button("Get Trulens Metrics")
        with gr.Row():
            tl_output_textbox = gr.TextArea(label="Output:")
            tl_explanation =  gr.Markdown(
                                            """<picture>
                                            <img alt="Metrics Explained" src="https://raw.githubusercontent.com/saradiazdelser/SimplifAI/main/metrics_explained.png" style="width: 100%; margin-bottom: 10px;" />
                                            </picture>"""
                                        )
        tl_dataframe = gr.Dataframe()

        tl_submit_butn.click(
            fn=get_trulens_feedback, outputs=[tl_dataframe, tl_output_textbox]
        )

    with gr.Tab("Observability"):

        gr.Markdown(
            "Visualization of Attribution for Complexity by token. Generated using TruLen Explainability's implementation of Integrated Gradients."
        )
        input_textbox = gr.Textbox(lines=5, placeholder="Put your text here...")
        submit_butn2 = gr.Button("Submit")
        explain_output = gr.HighlightedText(
            label="SIMPLICITY ATTRIBUTION",
            interactive=True,
            combine_adjacent=True,
            show_legend=True,
        )

        submit_butn2.click(fn=classify, inputs=input_textbox, outputs=explain_output)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0")
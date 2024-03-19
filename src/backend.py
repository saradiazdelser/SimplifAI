import pandas as pd
from trulens_eval.tru import Tru
from trulens_eval.tru_basic_app import TruBasicApp

from src.observability.classifier import SimpleEnglishClassifier
from src.observability.output import GradioHTML
from src.simplifier.chain import define_feedback, explain_term, simplify_text

# Trulens
tru = Tru()  # initialize TruLens app
version = 6  # define app version
feedbacks = define_feedback()  # load the feedback functions

# Initialize recorder for trulens to perform evaluations on each call
recorder = TruBasicApp(
    simplify_text, app_id=f"simplifAI-app-v{version}", feedbacks=feedbacks
)


def classify(text: str):
    """Classify function wrapper for gradio frontend.

    Args:
        text (str): Input text

    Returns:
        attributions: Attributions array for visualization (custom GradioHTML format)
    """
    classifier_id = "saradiaz/distilbert-base-uncased-simpleEng-classifier"
    task = SimpleEnglishClassifier(model_path=classifier_id, resolution=5)
    _, results = task.visualization(texts=[text], output_type=GradioHTML())
    attributions = results[1:]  # remove class label
    return attributions


def predict(text):
    """Simplify function wrapper for gradio frontend.
    Wraps trulens recorder so the trulens evaluation is triggered in every call.

    Args:
        text (str): Input text

    Returns:
        rec (str): Output text
    """
    with recorder as recording:
        rec = recorder.app(text)
    return rec


def explain(answer_text, concept):
    """Explain Term function wrapper for gradio frontend
    Args:
        answer_text (str): Simplified text for context
        concept (str) : termn that requires explaining
    Returns:
        rec (str): Output text
    """
    return explain_term(answer_text, concept)


def get_trulens_feedback() -> tuple:
    """
    Retrieve original input text and trulens evaluation results and output the latter as a dataframe.

    Returns:
        dataframe (pd.Dataframe) : trulens evaluation results dataframe
        output_textbox (str): original input text
    """
    # pass an empty list of app_ids to get all
    df = tru.get_records_and_feedback(app_ids=[f"simplifAI-app-v{version}"])[0]

    interesting_metrics = [
        "language_match",
        "pron_subjects_ratio",
        "is_simpler",
        "bleu",
        "perplexity",
        "one_idea_sentence",
        "explicit_subject",
        "short_sentence",
        "no_negations",
        "no_many_numbers",
        "technical_terms",
    ]

    sub_df = pd.DataFrame()
    for metric in interesting_metrics:
        try:
            sub_df[metric] = df[metric]
        except:
            print(f"Couldn't find metric {metric} in TruLens results")

    return sub_df.iloc[-1:], df.loc[len(df.index) - 1]["output"]

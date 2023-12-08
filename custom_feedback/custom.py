import functools

import evaluate as eval
import spacy
from bert_score import BERTScorer

# TODO: add requirements

# load spaCy model
nlp = spacy.load("en_core_web_sm")

def is_simpler(input_text: str, output_text:str) -> float:
    simplicity_in = sentence_simplicity(input_text)
    simplicity_out = sentence_simplicity(output_text)
    score = 1.0 if (simplicity_out > simplicity_in) else 0.0
    return float(score)

def pron_subjects_ratio(input_text: str) -> float:
    """
    Pronoun/Subject Ratio feedback function implementation.`pron_subjects_ratio` is a plain python method that accepts one piece
    of text (string), and produces a float representing the rate of pronouns used as subjects ( 0.0 --none-- and 1.0 --all pronouns are subjects--) .
    """
    # Process the sentence with spaCy
    doc = nlp(input_text)

    subjects = [token for token in doc if token.dep_ == "nsubj"]
    n_pron = [token for token in doc if token.pos_ == "PRON"]
    
    if len(subjects) > 0:
        score = len(n_pron)/len(subjects)
        # because the smaller the ratio the better
        return float(1-score)
    return 0.0


def sentence_simplicity(sentence: str) -> float:
    """
    Simplicity feedback function implementation.`Sentence_simplicity` is a plain python method that accepts one piece
    of text (string), and produces a float (assumed to be between 0.0 --complex-- and 1.0 --simple--) .
    """
    # Process the sentence with spaCy
    doc = nlp(sentence)

    # Calculate sentence length
    sentence_length = len(list(doc))
        
    noun_chucks =[chunk.text for chunk in doc.noun_chunks]
    n_root = sum([1 for token in doc if token.dep_=='ROOT'])
    if n_root:
        
        # Calculate average child num per root
        total_children = [len(list(token.children)) for token in doc ] #if token.dep_=='ROOT']
        average_children =  sum(total_children) / n_root

        # Calculate average noun phrases per root
        average_noun_chucks = len(noun_chucks) / n_root

        # Combine features into a single score
        score = (0.5*average_children + 0.5*average_noun_chucks) / sentence_length
        return float(1-score)
    
    return 0.0


def bert_score(input_text:str, output_text:str) -> float:
    """
    Uses BERT Score. A function that that measures
    similarity to ground truth using bert embeddings. ,
    Args:
        input_text (str): The input text. 
        output_text (str): The text generated by the model as response.

    Returns:
        float: A value between 0 and 1. 0 being "not in agreement" and 1
               being "in agreement".

    """

    bert = eval.load('bert')
    bert_score = bert.compute(
        predictions=[output_text], references=[input_text]
    )
    score = bert_score['precision'] if bert_score['precision'] else 0.0
    return float(score)

def bleu(input_text:str, output_text:str) -> float:
    """
    Uses BLEU Score. A function that that measures
    similarity to ground truth using token overlap.
    Args:
        input_text (str): The input text. 
        output_text (str): The text generated by the model as response.

    Returns:
        float: A value between 0 and 1. 0 being "not in agreement" and 1
               being "in agreement".

    """

    bleu = eval.load('bleu')
    bleu_score = bleu.compute(
        predictions=[output_text], references=[input_text]
    )
    score = 1-bleu_score['bleu'] if bleu_score['bleu'] else 0.0
    return float(score)

def rouge(input_text:str, output_text:str) -> float:
    """
    Uses ROUGE Score. Compares an automatically produced summary 
    or translation against a reference.
    Args:
        input_text (str): The input text. 
        output_text (str): The text generated by the model as response.

    Returns:
        float: A value between 0 and 1. 0 being "not in agreement" and 1
               being "in agreement".

    """

    rouge = eval.load('rouge')
    rouge_score = rouge.compute(
        predictions=[output_text], references=[input_text]
    )
    score = rouge_score['rouge1'] if rouge_score['rouge1'] else 0.0
    return float(score)


def perplexity(text:str) -> float:
    perplexity = eval.load("perplexity", module_type="metric")
    perplexity_score = perplexity.compute(predictions=[text], model_id='gpt2')
    score = perplexity_score['mean_perplexity'] if perplexity_score['mean_perplexity'] else 0.0
    return float(score)

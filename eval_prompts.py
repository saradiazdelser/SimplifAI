EVAL_PROMPT_MIXTRAL = {
    "prompt_text": """[INST] Assign a score (0-10 points) to the translation of the following text from English to Simple English.
Simple English is a version of the English language that aims to present information in a way that is easy to understand for individuals with limited proficiency in English or those who are learning the language. 
Texts in Simple English must follow these 10 requirements. Assing 1 point per requirement met.
1. Each sentence expresses only one idea.
2. The subject of each sentence must be explicit. Do not use pronouns as subjects.
3. Use short sentences and simple vocabulary. Use simple and direct language.
4. Do not use negations.
5. Do not use too many numbers or mathematical denominations. If there is no choice but to insert a number, always use digits.
6. Do not use confusing metaphors or complex comparisons.
7. Be clear, concise and direct.
8. Do not use technical terms, abbreviations and initials.
9. Text should be clear and coherent.
10. Avoid unnecessary ideas, words, sentences or phrases.
Original text (English):
{input_text}
Rewritten text (Simple English):
{ouput_text}
Score: [/INST] """,
    "variables": ["input_text", "output_text"],
}

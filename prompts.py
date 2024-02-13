SIMPLE_ENGLISH_PROMPT_MIXTRAL = {
    "prompt_text": """[INST] Re-write the input text into a Simple English text.
Simple English is a version of the English language that aims to present information in a way that is easy to understand for individuals with learning disabilities. 
Texts in Simple English must follow these requirements:
- Each sentence expresses only one idea. 
- Do not enumerate sentences or paragraphs.
- The subject of each sentence must be explicit. Do not use pronouns as subjects.
- Use short sentences and simple vocabulary. Be repetitive if necessary.
- Do not use negations.
- Do not use too many numbers or mathematical denominations. If there is no choice but to insert a number, always use digits.
- Do not use confusing metaphors or complex comparisons.
- Be clear, concise, direct and coherent.
- Do not use technical terms, abbreviations and initials.
- Avoid unnecessary ideas, words, sentences or phrases.
Input text:
{text}
Rewritten text: [/INST] """,
    "variables": ["text"],
}

EVAL_PROMPT_MIXTRAL = {
    "prompt_text": """[INST] Assign a score (0-10 points) to the translation of the following text from English to Simple English.
Simple English is a version of the English language that aims to present information in a way that is easy to understand for individuals with limited proficiency in English or those who are learning the language. 
Texts in Simple English must follow these 10 requirements. Assing 1 point per requirement met.
1. Each sentences expresses only one idea.
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

SIMPLE_CONCEPT_PROMPT_MIXTRAL = {
    "prompt_text": """[INST] Explain the following concept in Simple English within the given context. 
Simple English is a version of the English language that aims to present information in a way that is easy to understand for individuals with learning disabilities. 
Texts in Simple English must follow these requirements:
- Each sentence expresses only one idea. 
- Do not enumerate sentences or paragraphs.
- The subject of each sentence must be explicit. Do not use pronouns as subjects.
- Use short sentences and simple vocabulary. Be repetitive if necessary.
- Do not use negations.
- Do not use too many numbers or mathematical denominations. If there is no choice but to insert a number, always use digits.
- Do not use confusing metaphors or complex comparisons.
- Be clear, concise, direct and coherent.
- Do not use technical terms, abbreviations and initials.
- Avoid unnecessary ideas, words, sentences or phrases.
Context: {answer_text}
Concept to explain: {concept}
Explanation: [/INST] """,
    "variables": ["answer_text", "concept"],
}

SIMPLE_ENGLISH_PROMPT = {
    "prompt_text": """Simple English is a version of the English language that aims to present information in a way that is easy to understand for individuals with limited proficiency in English or those who are learning the language. Text in on Simple English are written with shorter sentences, simpler vocabulary, and a straightforward structure, making the content more accessible to a diverse audience. The primary goal is to provide clear and concise information on a wide range of topics, catering to readers who may find the regular English more challenging to comprehend. The simplicity of language in Simple English is intended to facilitate learning and understanding for a broad audience.
Instruction: Translate the input text to Simple English. Make sure it complies with the following requirements:
- Express only one idea per sentence.
- Each sentence should not start with a list number.
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
If the input text is already in Simple English, say "The input text is already in Simple English." and nothing else.
Input text:
{text}
Output text: """,
    "variables": ["text"],
}

SIMPLE_CONCEPT_PROMPT = {
    "prompt_text": """Simple English is a version of the English language that aims to present information in a way that is easy to understand for individuals with limited proficiency in English or those who are learning the language. Text in on Simple English are written with shorter sentences, simpler vocabulary, and a straightforward structure, making the content more accessible to a diverse audience. The primary goal is to provide clear and concise information on a wide range of topics, catering to readers who may find the regular English more challenging to comprehend. The simplicity of language in Simple English is intended to facilitate learning and understanding for a broad audience.
Instruction: Define the input concept in Simple English within the given input context. Make sure it complies with the following requirements:
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
    "variables": ["answer_text", "concept"],
}


all_prompts = {
    'VertexAI': {
        'simplify': SIMPLE_ENGLISH_PROMPT, 
        'explain': SIMPLE_CONCEPT_PROMPT,
        'evaluate': EVAL_PROMPT_MIXTRAL
        },
    'CTC_Madrid': {
        'simplify': SIMPLE_ENGLISH_PROMPT_MIXTRAL,
        'explain': SIMPLE_CONCEPT_PROMPT_MIXTRAL,
        'evaluate': EVAL_PROMPT_MIXTRAL
        }
}

SIMPLE_ENGLISH_PROMPT = {
    'prompt_text' : 
"""Context:
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
    'variables' = ['text']
}

SIMPLE_CONCEPT_PROMPT = {
     'prompt_text' : """Context:
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
    'variables' = ['answer_text', 'concept']
}


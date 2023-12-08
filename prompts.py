SIMPLE_ENGLISH_PROMPT = {
    'prompt_text' : 
"""Context: Simple English Wikipedia is a version of the popular online encyclopedia, Wikipedia, that aims to present information in a language that is easy to understand for individuals with limited proficiency in English or those who are learning the language. Articles on Simple English Wikipedia are written with shorter sentences, simpler vocabulary, and a straightforward structure, making the content more accessible to a diverse audience. The primary goal is to provide clear and concise information on a wide range of topics, catering to readers who may find the regular English Wikipedia more challenging to comprehend. The simplicity of language in Simple English Wikipedia is intended to facilitate learning and understanding for a broad audience.
Instruction: Translate the input text to Simple English Wikipedia format. Make sure it complies with the following requirements:
- Express only one idea per sentence.
- One sentence per line.
- Make sure the subject of each sentence is explicit. Do not use pronouns as subjects.
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
{input_text}
Output:""",
    'variables' = ['input_text']
}

SIMPLE_SENTECES_EVAL_PROMPT = {
    'prompt_text' : 
"""Context: Simple English Wikipedia is a version of the popular online encyclopedia, Wikipedia, that aims to present information in a language that is easy to understand for individuals with limited proficiency in English or those who are learning the language. Articles on Simple English Wikipedia are written with shorter sentences, simpler vocabulary, and a straightforward structure, making the content more accessible to a diverse audience. The primary goal is to provide clear and concise information on a wide range of topics, catering to readers who may find the regular English Wikipedia more challenging to comprehend. The simplicity of language in Simple English Wikipedia is intended to facilitate learning and understanding for a broad audience.
Instruction: Evaluate whether or not the following text expresses only one idea per sentence. Respond with an evaluation score from 0 (more than one idea per sentence) to 1 (only one idea per sentence).
Text: Star Wars is an American epic space opera media franchise created by George Lucas, which began with the eponymous 1977 film and quickly became a worldwide pop culture phenomenon. Score: 0
Text: Star Wars is an American science-fiction media franchise. It was created by George Lucas.  Score: 1
Text: {input_text} Score:""",
    'variables' = ['input_text']
}

COHERENCE_EVAL_PROMPT = {
    'prompt_text' : 
"""Context: Simple English Wikipedia is a version of the popular online encyclopedia, Wikipedia, that aims to present information in a language that is easy to understand for individuals with limited proficiency in English or those who are learning the language. Articles on Simple English Wikipedia are written with shorter sentences, simpler vocabulary, and a straightforward structure, making the content more accessible to a diverse audience. The primary goal is to provide clear and concise information on a wide range of topics, catering to readers who may find the regular English Wikipedia more challenging to comprehend. The simplicity of language in Simple English Wikipedia is intended to facilitate learning and understanding for a broad audience.
Instruction: Evaluate whether or not the following text follows a clear and coherent order. Respond with an evaluation score from 0 (not clear and not coherent) to 1 (clear and coherent).
Text: The sun set behind the mountains, casting a warm orange glow across the serene lake. The tranquility of the scene made it a perfect evening for a leisurely stroll along the water's edge. Score: 1
Text: The purple elephant danced with joyous laughter as the toaster sang the national anthem of Antarctica. Tomorrow, the clouds will taste like strawberry jam in the land of flying penguins and paperclip symphonies. Score: 0
Text: {input_text} Score:""",
    'variables' = ['input_text']
}

METAPHOR_EVAL_PROMPT = {
    'prompt_text' : 
"""Context: Simple English Wikipedia is a version of the popular online encyclopedia, Wikipedia, that aims to present information in a language that is easy to understand for individuals with limited proficiency in English or those who are learning the language. Articles on Simple English Wikipedia are written with shorter sentences, simpler vocabulary, and a straightforward structure, making the content more accessible to a diverse audience. The primary goal is to provide clear and concise information on a wide range of topics, catering to readers who may find the regular English Wikipedia more challenging to comprehend. The simplicity of language in Simple English Wikipedia is intended to facilitate learning and understanding for a broad audience.
Instruction: Evaluate whether or not the following text contains any metaphor or confusing comparisons. Respond with an evaluation score from 0 (no metaphors or comparisons) to 1 (methaphors present).
Text: Her smile was a beacon of sunshine on a cloudy day, brightening the gloom that had settled in his heart. Score: 1
Text: The cat sat lazily on the windowsill, watching the world go by with half-closed eyes. Score: 0
Text: {input_text} Score:""",
    'variables' = ['input_text']
}




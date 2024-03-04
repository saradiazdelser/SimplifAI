REQUIREMENT_4 = {
    "prompt_text": """"<s>[INST] Assign a score to the given text. The output must be a number 0, 5, 10.
    The output will be '10' if it meets the requirement of ''Do not use negations'' in every sentence, and will be '0' if it does not meet it in any sentence. If some sentences meet the requirement, but other not meet it, set a score of '5'.

    Text 1: "The capybara is a big rodent.\nThe capybara lives in South America.\nThe capybara is the biggest rodent alive.\n It lives in South America.\nCapybaras are part of the Hydrochoerus family.\n The capybara lives in savannas and rainforests.\nThe capybara lives near places with water.\n" 
    The assigned score to Text 1 is (0-10): 10 points

    Text 2: "The capybara is not a big rodent.\nThe capybara does not live in South America.\nThe capybara is not the biggest rodent alive.\n It does not live in South America.\nCapybaras are not part of the Hydrochoerus family.\n The capybara does not live in savannas and rainforests.\nThe capybara does not live near places with water.\n" 
    The assigned score to Text 2 is (0-10): 0 points

    Text 3: "The capybara is not a big rodent.\nThe capybara does live in South America.\nThe capybara is the biggest rodent alive.\n It does not live in South America.\nCapybaras are not part of the Hydrochoerus family.\n The capybara does not live in savannas and rainforests.\n" 
    The assigned score to Text 3 is (0-10): 5 points
    [/INST]</s> 

    [INST] 
    Text 4: "{text}"
    The assigned score to Text 4 is (0-10): 

    The output must be a number without explanations. [/INST]
""",
    "variables": ["text"],
}


REQUIREMENT_2 = {
    "prompt_text": """<s>[INST] Assign a score to the given text. The requirement of each sentence is 'The subject of each sentence must be explicit'.

    The output will be '10' if it meets the requirement in every sentence, will be '0' if it does not meet it in any sentence or will be '5' if some sentences meet the requirement, but other not meet it.

    Text 1: "The capybara is a big rodent.\nThe capybara lives in South America.\nThe capybara is the biggest rodent alive.\n Capybaras are part of the Hydrochoerus family.\n The capybara lives in savannas and rainforests.\nThe capybara lives near places with water.\n" 
    The assigned score to Text 1 is (0-10): 10 points
    
    Text 2: "It is a big rodent.\nIt lives in South America.\nIt is the biggest rodent alive.\n They are part of the Hydrochoerus family.\n It lives in savannas and rainforests.\nIt lives near places with water.\n" 
    The assigned score to Text 2 is (0-10): 0 points
    
    Text 3: "The capybara is a big rodent.\nIt lives in South America.\nThe capybara is the biggest rodent alive.\n They are part of the Hydrochoerus family.\n It lives in savannas and rainforests.\nThe capybara lives near places with water.\n" 
    The assigned score to Text 3 is (0-10): 5 points
    [/INST]</s> 

    [INST] 
    Text 4: "{text}"
    The assigned score to Text 4 is (0-10): 

    The output must be a number without explanations. [/INST]
""",
    "variables": ["text"],
}


REQUIREMENT_5 = {
    "prompt_text": """<s>[INST] Assign a score to the given text. The requirement of each sentence is 'Do not use too many numbers'.

    The output will be '10' if it meets the requirement in every sentence, will be '0' if it does not meet it in any sentence or will be '5' if some sentences meet the requirement, but other not meet it.

    Text 1: "The capybara is a big rodent.\nThe capybara lives in South America.\nThe capybara is the biggest rodent alive.\n Capybaras are part of the Hydrochoerus family.\n The capybara lives in savannas and rainforests.\nThe capybara lives near places with water.\n" 
    The assigned score to Text 1 is (0-10): 10 points
    
    Text 2: "There are 1,200,000 capybaras in Brazil.\nThe capybara measure from 3 to 4 feet in length and 1 to 2 feet at shoulder height.\n An adult capybara weighs 60 to 174 pounds, depending on the sex.\n" 
    The assigned score to Text 2 is (0-10): 0 points
    
    Text 3: "The capybara is a big rodent.\nAn adult capybara weighs 60 to 174 pounds, depending on the sex.\n" 
    The assigned score to Text 3 is (0-10): 5 points
    [/INST]</s> 

    [INST] 
    Text 4: "{text}"
    The assigned score to Text 4 is (0-10): 

    The output must be a number without explanations. [/INST] 
""",
    "variables": ["text"],
}


REQUIREMENT_8 = {
    "prompt_text": """<s>[INST] Assign a score to the text according to the following requirement: 'Does not contain technical terms, abbreviations or initials'.
    The output must be a number without explanations.
    The score will be a number from 0 to 10. A score of '10' means every sentence in the text meets the requirement, and a score of '0' means none of the sentences in the text meet the requirement.
    
    Text 1: "The capybara or greater capybara (Hydrochoerus hydrochaeris) is a giant cavy rodent native to South America (SA).\nIt is the largest living rodent and a member of the genus Hydrochoerus.\nThe only other extant member is the lesser capybara (Hydrochoerus isthmius).\nIts phylogenetic relatives encompass guinea pigs and rock cavies, while more distant relations include the agouti, chinchilla, and nutria.\n
    Score (0-10): 0 points
    
    Text 2: "The capybara is a big rodent that comes from South America.\nIt's the biggest rodent around today.\nIt's related to guinea pigs and rock cavies, and also has more distant connections to the agouti, chinchilla, and nutria.\n"
    Score (0-10): 10 points
    
    Text 3: "The capybara or greater capybara (Hydrochoerus hydrochaeris) is a giant cavy rodent native to South America.\nIt is the largest living rodent in the world.\nThe only other extant member is the lesser capybara (Hydrochoerus isthmius).\nIt's related to guinea pigs and rock cavies, and also has more distant connections to the agouti, chinchilla, and nutria.\n
    Score (0-10): 5 points
    [/INST]</s> 

    [INST] Assign a score to the text according to the following requirement: 'Does not contain technical terms, abbreviations or initials'.
    The output must be a number without explanations.
    The score will be a number from 0 to 10. A score of '10' means every sentence in the text meets the requirement, and a score of '0' means none of the sentences in the text meet the requirement.
    
    Text 4: "{text}"
    Score (0-10): [/INST] 
""",
    "variables": ["text"],
}

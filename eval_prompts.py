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

simplified_text = "The Savanna is a type of ecosystem.\nThe Savanna is found in tropical regions.\nSavannas typically have warm temperatures.\nSavannas have both wet and dry seasons.\nLots of animals live in the Savannas."
simplified_text_2= "The Savanna has from 800 to 3300 trees per hectare.\nSavannas typically have temperatures of 50 degrees.\nSavanna covers approximately 20 percentage of the Earth's land area."
simplified_text_3 = "The Savanna is a type of ecosystem.\nThe Savanna is found in tropical regions.\nThe Savanna has from 800 to 3300 trees per hectare.\nSavannas typically have temperatures of 50 degrees."

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

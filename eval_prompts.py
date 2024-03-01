REQUIREMENT_4 = {
    "prompt_text": """"[INST] Assign a score (0-10 points) to the translation of the following text from English to Simple English.
    One requirement of the Simple English is to ''Do not use negations''.
    Below, there are some examples of Simple English text and the output will be 10 if it meets the requirement of ''Do not use negations'' in every sentence, and will be 0 if it does not meet it in any sentence. 
    Text 1: "The capybara is a big rodent.\nThe capybara lives in South America.\nThe capybara is the biggest rodent alive.\nCapybaras are part of the Hydrochoerus family.\n The capybara lives in savannas and rainforests.\nThe capybara lives near places with water.\n" 
    The assigned score to Text 1 is (0-10): 10 points
    Text 2: "The capybara is not a big rodent.\nThe capybara does not live in South America.\nThe capybara is not the biggest rodent alive.\n It does not live in South America.\nCapybaras are not part of the Hydrochoerus family.\n The capybara does not live in savannas and rainforests.\nThe capybara does not live near places with water.\n" 
    The assigned score to Text 2 is (0-10): 0 points
    Text 3: "The capybara is a big rodent.\nThe capybara does live in South America.\nThe capybara is the biggest rodent alive.\n It does not live in South America.\nCapybaras are not part of the Hydrochoerus family.\n The capybara does not live in savannas and rainforests.\n" 
    The assigned score to Text 3 is (0-10): 5 points
    Text 4: "{text}"
    The assigned score to Text 4 is (0-10): [/INST] 
""",
    "variables": ["text"],
}


REQUIREMENT_2 = {
    "prompt_text": """[INST] Assign a score (0-10 points) to the input text.
    One requirement of the Simple English is to ''The subject of each sentence must be explicit''.

    Below, there are some examples of Simple English text and the output will be 10 if it meets the requirement of ''The subject of each sentence must be explicit'' in every sentence, and will be 0 if it does not meet it in any sentence. 
    Text 1: "The capybara is a big rodent.\nThe capybara lives in South America.\nThe capybara is the biggest rodent alive.\n Capybaras are part of the Hydrochoerus family.\n The capybara lives in savannas and rainforests.\nThe capybara lives near places with water.\n" 
    The assigned score to Text 1 is (0-10): 10 points
    Text 2: "The capybara is not a big rodent.\nIt does not live in South America.\nIt is not the biggest rodent alive.\n It does not live in South America.\nThey are not part of the Hydrochoerus family.\n It does not live in savannas and rainforests.\nIt does not live near places with water.\n" 
    The assigned score to Text 2 is (0-10): 0 points
    Text 3: "The capybara is a big rodent.\nIt does live in South America.\nIt is the biggest rodent alive.\n It does not live in South America.\nCapybaras are not part of the Hydrochoerus family.\n The capybara does not live in savannas and rainforests.\n" 
    The assigned score to Text 3 is (0-10): 5 points
    
	Text 4: "{text}"
    The assigned score to Text 4 is (0-10): [/INST] 
""",
    "variables": ["text"],
}


REQUIREMENT_5 = {
    "prompt_text": """[INST] Assign a score (0-10 points) to the input text.
    One requirement of the Simple English is to ''Do not use too many numbers''.

    Below, there are some examples of Simple English text and the output will be 10 if it meets the requirement of ''Do not use too many numbers'' in every sentence, and will be 0 if it does not meet it in any sentence. 

    Text 1: "The capybara is a big rodent.\nThe capybara lives in South America.\nThe capybara is the biggest rodent alive.\n Capybaras are part of the Hydrochoerus family.\n The capybara lives in savannas and rainforests.\nThe capybara lives near places with water.\n" 
    The assigned score to Text 1 is (0-10): 10 points
    Text 2: "There are 1,200,000 capybaras in Brazil.\nThe capybara measure three to four feet in length and one to two feet at shoulder height.\n An adult capybara weighs 60 to 174 pounds, depending on the sex.\n" 
    The assigned score to Text 2 is (0-10): 0 points
    
	Text 3: "{text}"
    The assigned score to Text 3 is (0-10): [/INST] 
""",
    "variables": ["text"],
}
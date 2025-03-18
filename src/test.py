from fuzzywuzzy import process

def find_closest_match(input_sentence, sentence_list):
    # Find the closest match from the list without extracting anything
    best_match, score = process.extractOne(input_sentence, sentence_list)
    
    return best_match

# Example usage
input_sentence = "polar bear: thick smoothie"
sentence_list = [
    "spooky stew",
    "scorpion salad",
    "strawberry skewers",
    "thick smoothie"
]

closest_match = find_closest_match(input_sentence, sentence_list)
print("Closest Match:", closest_match)

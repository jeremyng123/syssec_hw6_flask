import json

with open('words_dictionary.json', 'r') as f:
    words = json.load(f).keys()
    f.close()

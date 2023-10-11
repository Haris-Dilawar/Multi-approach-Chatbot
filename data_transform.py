import json

### using this module to convert the data into question answer format.(Q/A dataset will be available in code folder)
with open("intents.json") as file:
    data = json.load(file)


output = []

for intent in data['intents']:
    patterns = intent['patterns']
    responses = intent['responses']
    for p, r in zip(patterns, responses):
        output.append(p)
        output.append(r)


file_path = "q_a.txt"
with open(file_path, "w") as file:
    for line in output:
        file.write(line + "\n")
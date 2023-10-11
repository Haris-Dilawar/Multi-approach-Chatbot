
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import os


# chatbot = ChatBot('Assistant')
chatbot = ChatBot(
    'Assistant',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',  # This is the default
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, I do not understand. Can you rephrase?',
            'maximum_similarity_threshold': 0.90
        }
    ]
)



# Use the ChatterBotCorpusTrainer trainer class
trainer = ChatterBotCorpusTrainer(chatbot)


# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")

# Additionally, use the ListTrainer to train from the provided data
list_trainer = ListTrainer(chatbot)


# Assuming your provided data is in the form of alternating questions and answers
with open("q_a.txt", "r") as file:
    lines = file.readlines()
    conversations = [line.strip() for line in lines]


list_trainer.train(conversations)

def get_Response(prompt):
    return chatbot.get_response(prompt)

# print(get_Response("what time do you open"))

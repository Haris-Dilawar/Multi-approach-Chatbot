import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tensorflow as tf
import random
import json 
import pickle

nltk.download("punkt")
with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    #LOADING AND PRE-PROCESSING JSON FILE  

    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    #TRAINING AND TESTING
    #1) BAG OF WORDS IS USED THAT COUNTS OCCURENCE OF WORDS

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

    #MODEL

# Create Model using Keras API
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(len(training[0]),)),    #INPUT DATA (LENGTH OF INPUT DATA)
    tf.keras.layers.Dense(8, activation='relu'),   #TWO HIDDEN LAYERS
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(len(output[0]), activation='softmax')    #OUTPUT LAYER
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Load model if exists check
try:
    model.load_weights("model.tflearn")
except:
    model.fit(training, output, epochs=1000, batch_size=8)
    model.save_weights("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return np.array(bag)

def chat(msg):
    print("Start talking with the bot (type quit to stop)!")
    
    while True:
        inp = msg
        
        if inp.lower() == "quit":
            exit(0)
        
        results = model.predict(np.array([bag_of_words(inp, words)]))
        results_index = np.argmax(results)
    
        tag = labels[results_index]
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        
        return(random.choice(responses))
# chat("hello")
# if __name__ == "__main__":
#     chat()

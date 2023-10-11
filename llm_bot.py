from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import os 
import pinecone 
import json
import os


with open("config.json", "r") as f:
    credentials = json.load(f)


### use this code chunk for dataset creation for llm

# with open("intents.json") as file:
#     data = json.load(file)

# output = []

# for intent in data['intents']:
#     patterns = intent['patterns']
#     responses = intent['responses']
#     for p, r in zip(patterns, responses):
#         output.append("question: " + p)
#         output.append("answer: "+r)

# file_path = "llm.txt"
# with open(file_path, "w") as file:
#     for line in output:
#         file.write(line + "\n")




##loading the dataset
loader = TextLoader("llm.txt")  
docs = loader.load()


os.environ["OPENAI_API_KEY"] = credentials["OPENAI_API_KEY"]


# initialize pinecone
pinecone.init(
    api_key=credentials["PINECONE"]["API_KEY"],
    environment=credentials["PINECONE"]["ENVIRONMENT"]
)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1200,
    chunk_overlap  = 200,
    length_function = len,
)

docs_chunks = text_splitter.split_documents(docs)



embeddings = OpenAIEmbeddings()




index_name = "myindex"

# #create a new index
docsearch = Pinecone.from_documents(docs_chunks, embeddings, index_name=index_name)


from langchain.prompts import PromptTemplate
prompt_template = """You are an Car Rental AI English assitant for a Car rental Service in Pakistan. Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer in English:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


chain_type_kwargs = {"prompt": PROMPT}
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever(), chain_type_kwargs=chain_type_kwargs)

def get_answers(prompt):
    return qa.run(prompt)



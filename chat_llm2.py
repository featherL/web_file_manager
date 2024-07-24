from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from bs4 import BeautifulSoup

model_local = ChatOllama(model="codellama")
# 1 split data into chunks
urls = [
    "https://ollama.com/",
    "https://ollama.com/blog/windows-preview",
    "https://ollama.com/blog/openai-compatibility",
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [ item for sublist in docs for item in sublist]
#text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500,chunk_overlap=100)
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
docs_splits = text_splitter.split_documents(docs_list)

# 2 convert documents to Embeddings and store them
vectorstore = Chroma.from_documents(
    documents=docs_splits,
    collection_name="rag-chroma",
    #embedding=embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text'),
    embedding=OllamaEmbeddings(model='nomic-embed-text'),

    
)

retriever =vectorstore.as_retriever()

# 3 before RAG 
print("Before RAG\n")
before_rag_template ="What is {topic}"
before_rag_prompt = ChatPromptTemplate.from_template(before_rag_template)
before_rag_chain = before_rag_prompt | model_local | StrOutputParser()
print(before_rag_chain.invoke({"topic":"Ollama"}))

# 4 after RAG
print("\n######\nAfter RAG\n")
after_rag_template ="""Answer the question based only the following context:
{context}
Question:{question}
"""
after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
after_rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | after_rag_prompt
    | model_local
    | StrOutputParser()
)
print(after_rag_chain.invoke("What is Ollama?"))
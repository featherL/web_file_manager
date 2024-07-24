
import os,time
from langchain_community.document_loaders import DirectoryLoader,TextLoader
from langchain.llms.ollama import Ollama
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import chroma
from langchain_community.embeddings import OllamaEmbeddings
#from langchain_community import embeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import gradio as gr

# 加载embedding
embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec": "/home/guoyuh/Github/shibing624/text2vec-bge-large-chinese/",
    "text2vec2": "uer/sbert-base-chinese-nli",
    "text2vec3": "shibing624/text2vec-base-chinese",
    "m3e-base":"moka-ai/m3e-base",
    "nomic-embed-text":"nomic-embed-text"
}


def load_documents(directory="documents"):
    """
    加载books下的文件，进行拆分
    :param directory:
    :return:
    """
    text_loader_kwargs={'autodetect_encoding': True}
    #loader = DirectoryLoader(directory,glob="*.txt")
    loader = DirectoryLoader(directory,glob="*.txt",loader_cls=TextLoader,loader_kwargs=text_loader_kwargs,silent_errors =True)
    #print("=============loader",loader)
    documents = loader.load()
    #print("=============documents",documents[0])
    text_spliter = CharacterTextSplitter(chunk_size=128, chunk_overlap=0)
    split_docs = text_spliter.split_documents(documents)
    return split_docs

def load_embedding_model(model="ernie-tiny"):
    """
    加载embedding模型
    :param model_name:
    :return:
    """
    return OllamaEmbeddings(
        model=embedding_model_dict[model]
    )

def store_chroma(docs, embeddings, persist_directory="VectorStore"):
    """
    讲文档向量化，存入向量数据库
    :param docs:
    :param embeddings:
    :param persist_directory:
    :return:
    """
    db = chroma.Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    db.persist()
    return db



# 加载embedding模型
#embeddings = load_embedding_model('text2vec')
embeddings = load_embedding_model(model='nomic-embed-text')

# 加载数据库
if not os.path.exists('VectorStore'):
    documents = load_documents(directory="books/")
    db = store_chroma(documents, embeddings)
else:
    db = chroma.Chroma(persist_directory='VectorStore', embedding_function=embeddings)


retriever = db.as_retriever()

# 创建llm
codellama_llm = Ollama(model="mistral")

# before_rag_template = ",请用中午回答下述问题,问题：{question}"
# before_rag_prompt  = ChatPromptTemplate.from_template(before_rag_template)
# before_rag_chain = (
#     before_rag_prompt
#     | codellama_llm
#     | StrOutputParser()
# )
# query ="你知道芮小丹是谁吗"
# print("before_rag_prompt:\n",before_rag_chain.invoke({"question":query}))


after_rag_template = """根据下面的上下文（context）内容用中文回答问题。
如果你不知道答案，就回答不知道，不要试图编造答案。
答案最多3句话，保持答案简介。
总是在答案结束时说“谢谢你的提问！”
{context}
问题：{question}
"""
after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
after_rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | after_rag_prompt
    | codellama_llm
    | StrOutputParser()
)
# query ="你知道芮小丹是谁吗"
# print("after_rag_chain:\n",after_rag_chain.invoke(query))
# # print(after_rag_chain.invoke("请介绍一下自己"))



def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.update(value="", interactive=False)


def add_file(history, file):
    """
    上传文件后的回调函数，将上传的文件向量化存入数据库
    :param history:
    :param file:
    :return:
    """
    global after_rag_chain
    directory = os.path.dirname(file.name)
    documents = load_documents(directory)
    db = store_chroma(documents, embeddings)
    retriever = db.as_retriever()
    after_rag_chain.retriever = retriever
    history = history + [((file.name,), None)]
    return history


def bot(history):
    """
    聊天调用的函数
    :param history:
    :return:
    """
    message = history[-1][0]
    if isinstance(message, tuple):
        response = "文件上传成功！！"
    else:
        #response = after_rag_chain({"query": message})['result']
        response = after_rag_chain.invoke(message)
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        btn = gr.UploadButton("📁", file_types=['txt'])
    with gr.Column(scale=1):
        emptyBtn = gr.Button("Clear History")
        max_length = gr.Slider(0, 4096, value=2048, step=1.0, label="Maximum length", interactive=True)
        top_p = gr.Slider(0, 1, value=0.7, step=0.01, label="Top P", interactive=True)
        temperature = gr.Slider(0, 1, value=0.95, step=0.01, label="Temperature", interactive=True)

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )

demo.queue()
if __name__ == "__main__":
    demo.launch(share=True)
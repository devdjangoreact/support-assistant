import os
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

import pickle

load_dotenv()
API_KEY = os.environ.get("OPENAI_API_KEY")


class IndexesLLM:
    def __init__(self) -> None:
        pass

    def loaders_from_file(self, input: str):
        loader = DirectoryLoader(
            "/home/ai/projects/support-assistant/backend/components/llm/FAQ",
            glob="**/*.txt",
            loader_cls=TextLoader,
            show_progress=True,
        )
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
        )

        documents = text_splitter.split_documents(docs)
        documents[0]

        embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
        vectorstore = FAISS.from_documents(documents, embeddings)

        with open("vectorstore.pkl", "wb") as f:
            pickle.dump(vectorstore, f)

        with open("vectorstore.pkl", "rb") as f:
            vectorstore = pickle.load(f)
            prompt_template = """You are a helpful assistant for our restaurant.

            {context}

            Question: {question}
            Answer here:"""
            PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
            chain_type_kwargs = {"prompt": PROMPT}

            llm = OpenAI(openai_api_key=API_KEY)
            qa = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vectorstore.as_retriever(),
                chain_type_kwargs=chain_type_kwargs,
            )

            query = "When does the restaurant open?"
            qa.run(query)
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")
            qa = ConversationalRetrievalChain.from_llm(
                llm=OpenAI(model_name="text-davinci-003", temperature=0.7, openai_api_key=API_KEY),
                memory=memory,
                retriever=vectorstore.as_retriever(),
                combine_docs_chain_kwargs={"prompt": PROMPT},
            )

            query = "Do you offer vegan food?"
            qa({"question": query})
            return qa({"question": "How much does it cost?"})

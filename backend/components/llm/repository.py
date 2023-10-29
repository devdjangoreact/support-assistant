import os
import openai

from dotenv import load_dotenv, find_dotenv

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain.document_loaders import JSONLoader
from components.llm import schemas as llm_schemas

load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]


class LLMService:
    def __init__(self) -> None:
        pass

    def get_answer_from_llm(self, input: str) -> llm_schemas.FAQItem:
        loader = JSONLoader(file_path="backend/datasource/FAQ.json", jq_schema=".[]", text_content=False)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()

        url = "http://localhost:6333"
        qdrant = Qdrant.from_documents(
            docs,
            embeddings,
            url=url,
            prefer_grpc=True,
            collection_name="my_documents",
        )
        found_docs = qdrant.similarity_search(input)
        return llm_schemas.FAQItem(**eval(found_docs[0].page_content))

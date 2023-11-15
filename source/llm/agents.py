import os
import pickle
from dotenv import load_dotenv


from langchain.agents import load_tools
from langchain.llms import OpenAI
from langchain.agents import Tool
from langchain.agents import initialize_agent

from typing import Optional
from langchain.tools import BaseTool
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain.agents import AgentType

load_dotenv()
API_KEY = os.environ.get("OPENAI_API_KEY")

with open("vectorstore.pkl", "rb") as f:
    vectorstore = pickle.load(f)


class CustomSearchTool(BaseTool):
    name = "restaurant search"
    description = "useful for when you need to answer questions about our restaurant"

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        store = vectorstore.as_retriever()
        docs = store.get_relevant_documents(query)
        text_list = [doc.page_content for doc in docs]
        return "\n".join(text_list)

    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")


class AgentsLLM:
    def __init__(self) -> None:
        self.llm = OpenAI(model_name="text-davinci-003", temperature=0.7, openai_api_key=API_KEY)

    def defualt_tools(self, input: str):
        llm = self.llm

        tool_names = ["llm-math"]
        tools = load_tools(tool_names, llm=llm)
        tool_list = [Tool(name="Math Tool", func=tools[0].run, description="Tool to calculate, nothing else")]

        agent = initialize_agent(tool_list, llm, agent="zero-shot-react-description", verbose=True)
        answer1 = agent.run("How are you?")
        answer2 = agent.run("What is 100 divided by 25?")

        return [answer1, answer2]

    def custom_tools(self, input: str):
        llm = self.llm
        tools = [CustomSearchTool()]
        agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
        return agent.run("When does the restaurant open?")

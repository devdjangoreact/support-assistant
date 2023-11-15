import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain.llms import OpenAI
from langchain.memory import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory

load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]


class MemoryLLM:
    def __init__(self) -> None:
        pass

    def get_memory_answer(self, input: str):
        history = ChatMessageHistory()

        history.add_user_message("hi!")
        history.add_ai_message("hello my friend!")
        history.messages
        memory = ConversationBufferMemory()
        memory.chat_memory.add_user_message("hi!")
        memory.chat_memory.add_ai_message("hello my friend!")
        memory.load_memory_variables({})
        llm = OpenAI(temperature=0)
        conversation = ConversationChain(llm=llm, verbose=True, memory=ConversationBufferMemory())
        conversation.predict(input="Hi")
        answer1 = conversation.predict(input="I need to know the capital of france")

        review = "I ordered Pizza Salami for 9.99$ and it was awesome! \
        The pizza was delivered on time and was still hot when I received it. \
        The crust was thin and crispy, and the toppings were fresh and flavorful. \
        The Salami was well-cooked and complemented the cheese perfectly. \
        The price was reasonable and I believe I got my money's worth. \
        Overall, I am very satisfied with my order and I would recommend this pizza place to others."

        memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)
        memory.save_context(
            {"input": "Hello, how can I help you today?"},
            {"output": "Could you analyze a review for me?"},
        )
        memory.save_context(
            {"input": "Sure, I'd be happy to. Could you provide the review?"},
            {"output": f"{review}"},
        )
        conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
        conversation.predict(input="Thank you very much!")
        answer2 = memory.load_memory_variables({})
        return [answer1, answer2]

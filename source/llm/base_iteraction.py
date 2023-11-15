import os
import openai
from dotenv import load_dotenv, find_dotenv

from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate as PromptTemplatePrompts
from langchain.chains import LLMChain

# prompt
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.chat_models import ChatOpenAI

# chain
from langchain import PromptTemplate
from langchain.chains import SimpleSequentialChain
from langchain.chains import SequentialChain


from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE

load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]


class ModalBasic:
    def __init__(self) -> None:
        pass

    def chat(self, input: str) -> str:
        messages = [{"role": "user", "content": input}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message.content


class PromptParsers:
    def __init__(self) -> None:
        pass

    def chat_template(self, input: str):
        llm = OpenAI(model_name="text-ada-001")
        llm("Tell me a joke")

        template = """
        Interprete the text and evaluate the text.
        sentiment: is the text in a positive, neutral or negative sentiment?
        subject: What subject is the text about? Use exactly one word.

        Format the output as JSON with the following keys:
        sentiment
        subject

        text: {input}
        """
        prompt_template = ChatPromptTemplate.from_template(template=template)
        chain = LLMChain(llm=llm, prompt=prompt_template)
        answer = chain.predict(input="I ordered Pizza Salami and it was awesome!")

        return answer

    def chat_parser(self, input: str):
        sentiment_schema = ResponseSchema(
            name="sentiment",
            description="Is the text positive, neutral or negative? Only provide these words",
        )
        subject_schema = ResponseSchema(
            name="subject", description="What subject is the text about? Use exactly one word."
        )
        price_schema = ResponseSchema(
            name="price",
            description="How expensive was the product? Use None if no price was provided in the text",
        )

        response_schemas = [sentiment_schema, subject_schema, price_schema]

        parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = parser.get_format_instructions()

        template = """
        Interprete the text and evaluate the text.
        sentiment: is the text in a positive, neutral or negative sentiment?
        subject: What subject is the text about? Use exactly one word.

        Just return the JSON, do not add ANYTHING, NO INTERPRETATION!

        text: {input}

        {format_instructions}

        """

        prompt = ChatPromptTemplate.from_template(template=template)

        format_instructions = parser.get_format_instructions()

        messages = prompt.format_messages(
            # input="I ordered Pizza Salami for 9.99$ and it was awesome!",
            input=input,
            format_instructions=format_instructions,
        )

        chat = ChatOpenAI(temperature=0.0)
        response = chat(messages)

        output_dict = parser.parse(response.content)
        return output_dict


class Chains:
    def __init__(self) -> None:
        self.llm = OpenAI(temperature=0)

    def base_chain(self, input: str):
        llm = self.llm
        template = """
        Interprete the text and evaluate the text.
        sentiment: is the text in a positive, neutral or negative sentiment?
        subject: What subject is the text about? Use exactly one word.

        Format the output as JSON with the following keys:
        sentiment
        subject

        text: {input}
        """

        prompt_template = PromptTemplate.from_template(template=template)
        chain = LLMChain(llm=llm, prompt=prompt_template)
        answer1 = chain.predict(input="I ordered Pizza Salami and it was awesome!")

        # sequentials_chain
        response_template = """
        You are a helpful bot that creates a 'thank you' reponse text.
        If customers are unsatisfied, offer them a real world assitant to talk to.
        You will get a sentiment and subject as into and evaluate.

        text: {input}
        """
        review_template = PromptTemplate(input_variables=["input"], template=response_template)
        review_chain = LLMChain(llm=llm, prompt=review_template)
        overall_chain = SimpleSequentialChain(chains=[chain, review_chain], verbose=True)

        answer2 = overall_chain.run(input="I ordered Pizza Salami and was aweful!")

        return [answer1, answer2]

    def chain_multi_arguments(self, input: str):
        llm = self.llm
        # This is an LLMChain to write a review given a dish name and the experience.
        prompt_review = PromptTemplate.from_template(
            template="You ordered {dish_name} and your experience was {experience}. Write a review: "
        )
        chain_review = LLMChain(llm=llm, prompt=prompt_review, output_key="review")

        # This is an LLMChain to write a follow-up comment given the restaurant review.
        prompt_comment = PromptTemplate.from_template(
            template="Given the restaurant review: {review}, write a follow-up comment: "
        )
        chain_comment = LLMChain(llm=llm, prompt=prompt_comment, output_key="comment")

        # This is an LLMChain to summarize a review.
        prompt_summary = PromptTemplate.from_template(
            template="Summarise the review in one short sentence: \n\n {review}"
        )
        chain_summary = LLMChain(llm=llm, prompt=prompt_summary, output_key="summary")

        # This is an LLMChain to translate a summary into German.
        prompt_translation = PromptTemplate.from_template(template="Translate the summary to german: \n\n {summary}")
        chain_translation = LLMChain(llm=llm, prompt=prompt_translation, output_key="german_translation")

        overall_chain = SequentialChain(
            chains=[chain_review, chain_comment, chain_summary, chain_translation],
            input_variables=["dish_name", "experience"],
            output_variables=["review", "comment", "summary", "german_translation"],
        )

        return overall_chain({"dish_name": "Pizza Salami", "experience": "It was awful!"})

    def chain_multi_prompt(self, input: str):
        llm = self.llm

        positive_template = """You are an AI that focuses on the positive side of things. \
        Whenever you analyze a text, you look for the positive aspects and highlight them. \
        Here is the text:
        {input}"""

        neutral_template = """You are an AI that has a neutral perspective. \
        You just provide a balanced analysis of the text, \
        not favoring any positive or negative aspects. Here is the text:
        {input}"""

        negative_template = """You are an AI that is designed to find the negative aspects in a text. \
        You analyze a text and show the potential downsides. Here is the text:
        {input}"""

        prompt_infos = [
            {
                "name": "positive",
                "description": "Good for analyzing positive sentiments",
                "prompt_template": positive_template,
            },
            {
                "name": "neutral",
                "description": "Good for analyzing neutral sentiments",
                "prompt_template": neutral_template,
            },
            {
                "name": "negative",
                "description": "Good for analyzing negative sentiments",
                "prompt_template": negative_template,
            },
        ]
        destination_chains = {}
        for p_info in prompt_infos:
            name = p_info["name"]
            prompt_template = p_info["prompt_template"]
            prompt = PromptTemplatePrompts(template=prompt_template, input_variables=["input"])
            chain = LLMChain(llm=llm, prompt=prompt)
            destination_chains[name] = chain
        destination_chains
        destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
        destinations_str = "\n".join(destinations)
        router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)
        router_prompt = PromptTemplatePrompts(
            template=router_template,
            input_variables=["input"],
            output_parser=RouterOutputParser(),
        )

        router_chain = LLMRouterChain.from_llm(llm, router_prompt)

        chain = MultiPromptChain(
            router_chain=router_chain,
            destination_chains=destination_chains,
            default_chain=destination_chains["neutral"],
            verbose=True,
        )

        return chain.run("I ordered Pizza Salami for 9.99$ and it was awesome!")

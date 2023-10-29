from components.llm import schemas as llm_schemas
from components.llm import repository as llm_repository


class LLMService:
    def __init__(self, llm_repository: llm_repository.LLMService = llm_repository.LLMService()) -> None:
        self.llm_repository = llm_repository

    def get_answer_from_llm(self, input: str):
        answer: llm_schemas.FAQItem = self.llm_repository.get_answer_from_llm(input)
        return answer

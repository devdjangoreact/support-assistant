from components.llm import service as llm_service
from components.message import repository as message_repository


class Messages:
    def __init__(
        self,
        llm_service=llm_service.LLMService(),
        message_repository: message_repository.MessageRepository = message_repository.MessageRepository(),
    ) -> None:
        self.llm_service = llm_service
        self.message_repository = message_repository

    def get_answer_brom_chatgpt(self, input: str, chat: str) -> str:
        return self.llm_service.get_answer_from_llm(input=input)

    def get_messages_by_room(self, room: str):
        return self.message_repository.get_message_by_room(room=room)

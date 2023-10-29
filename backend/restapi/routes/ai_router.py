from fastapi import APIRouter
from typing import List
from components.message import service as message_service
from components.chat import service as chat_service
from restapi.schemas import Question
from components.llm import schemas as llm_schemas
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/chat-rooms")
def read_roots() -> List[str]:
    return chat_service.Rooms().get_chats()


@router.get("/chat-room/{selectedChatRoom}/messages")
def read_root(selectedChatRoom: str) -> List[str]:
    object_message = message_service.Messages()
    return object_message.get_messages_by_room(room=selectedChatRoom)


@router.post("/chat-room/{selectedChatRoom}/send-message")
def get_answer(body: Question, selectedChatRoom: str) -> JSONResponse:
    question_text = body.message
    object_message = message_service.Messages()
    answer: llm_schemas.FAQItem = object_message.get_answer_brom_chatgpt(input=question_text, chat=selectedChatRoom)
    answer_dict = answer.dict()
    return JSONResponse(content=answer_dict)

from fastapi import APIRouter
from typing import Dict, List

from restapi.schemas import Question

router = APIRouter(prefix="/ai", tags=["ai"])


FAQ = [...]  # Copy the FAQ JSON data here


@router.get("/chat-rooms")
def read_root() -> List[str]:
    return ["General", "Support", "Feedback", "Random"]


@router.get("/chat-rooms/{selectedChatRoom}/messages")
def read_root(selectedChatRoom: str) -> List[str]:
    return [selectedChatRoom + " - answer"]


@router.post("/chat-room/{selectedChatRoom}/send-message")
def get_answer(body: Question, selectedChatRoom: str) -> List[str]:
    question_text = body.message
    # Here, we should incorporate logic to match the question with the FAQ
    # and retrieve the answer, possibly using the ChatGPT API.
    # This is a basic example that just returns the first answer.
    return [selectedChatRoom + " - answer - " + question_text]
    # return {"answer": FAQ[0]["Answer_plain_text"]}

from pydantic import BaseModel, Field
from typing import List


class FAQItem(BaseModel):
    question_id: str = Field(..., alias="Question ID")
    question_short: str = Field(..., alias="Question_short")
    question_original: str = Field(..., alias="Question_original")
    keywords: List[str] = Field(..., alias="Keywords")
    answer_plain_text: str = Field(..., alias="Answer_plain_text")
    answer_original: str = Field(..., alias="Answer_original")
    question_original_alternatives: List[str] = Field(..., alias="Question_original_alternatives")
    question_short_alternatives: List[str] = Field(..., alias="Question_short_alternatives")
    notes: str = Field(..., alias="Notes")
    source_type: str = Field(..., alias="Source_type")
    date: str = Field(..., alias="date")

from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str

class StartAttempt(BaseModel):
    user_id: int
    quiz_mode: str = "single"  # default to single mode

class FinishAttempt(BaseModel):
    attempt_id: int

class AnswerSubmission(BaseModel):
    user_id: int
    attempt_id: int
    question_id: int
    selected_option: str

class BatchSubmission(BaseModel):
    user_id: int
    attempt_id: int
    answers : List[AnswerSubmission]
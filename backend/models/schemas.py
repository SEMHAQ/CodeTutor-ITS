from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    message: str
    session_id: str
    mode: str = "tutor"  # "tutor", "hint", "exercise"
    programming_language: str = "python"
    hint_level: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    hint_level: Optional[int] = None
    knowledge_points: List[str] = []


class ExerciseRequest(BaseModel):
    topic: str
    difficulty: str = "medium"  # "easy", "medium", "hard"
    programming_language: str = "python"
    count: int = 1


class Exercise(BaseModel):
    title: str
    description: str
    input_example: str
    output_example: str
    test_cases: List[dict]
    knowledge_points: List[str]
    difficulty: str


class HintRequest(BaseModel):
    code: str
    error_description: Optional[str] = None
    current_hint_level: int = 1
    programming_language: str = "python"


class HintResponse(BaseModel):
    hint: str
    hint_level: int
    next_hint_available: bool


class StudentProgress(BaseModel):
    session_id: str
    knowledge_point: str
    mastery_level: float  # 0.0 to 1.0
    attempts: int
    last_updated: datetime


class ProgressReport(BaseModel):
    session_id: str
    total_questions: int
    knowledge_points_summary: dict
    weak_points: List[str]
    recommendations: List[str]

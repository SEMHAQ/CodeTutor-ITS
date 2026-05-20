from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json

from backend.models.schemas import (
    ChatRequest,
    ChatResponse,
    ExerciseRequest,
    Exercise,
    HintRequest,
    HintResponse,
    ProgressReport,
)
from backend.database.db import get_db, ChatHistory, StudentKnowledge, ExerciseRecord
from llm.client import llm_client
from llm.prompts import (
    build_tutor_prompt,
    build_hint_prompt,
    build_exercise_prompt,
    build_knowledge_analysis_prompt,
)

router = APIRouter(prefix="/api/tutor", tags=["tutor"])


@router.post("/chat", response_model=ChatResponse)
async def chat_with_tutor(request: ChatRequest, db: Session = Depends(get_db)):
    """Main chat endpoint for tutoring."""
    # Save user message
    user_msg = ChatHistory(
        session_id=request.session_id,
        role="user",
        content=request.message,
        mode=request.mode,
        timestamp=datetime.utcnow(),
    )
    db.add(user_msg)
    db.commit()

    # Get chat history
    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.session_id == request.session_id)
        .order_by(ChatHistory.timestamp)
        .limit(20)
        .all()
    )
    chat_history = [{"role": h.role, "content": h.content} for h in history]

    # Get knowledge context
    knowledge = (
        db.query(StudentKnowledge)
        .filter(StudentKnowledge.session_id == request.session_id)
        .all()
    )
    knowledge_context = ""
    if knowledge:
        weak = [k.knowledge_point for k in knowledge if k.mastery_level < 0.5]
        if weak:
            knowledge_context = f"Student's weak knowledge points: {', '.join(weak)}"

    # Build prompt based on mode
    if request.mode == "tutor":
        messages = build_tutor_prompt(
            request.message, chat_history, request.programming_language, knowledge_context
        )
    elif request.mode == "hint":
        messages = build_hint_prompt(
            request.message,
            "",
            request.hint_level or 1,
            request.programming_language,
            chat_history,
        )
    else:
        messages = build_tutor_prompt(
            request.message, chat_history, request.programming_language, knowledge_context
        )

    # Get LLM response
    try:
        response_text = await llm_client.chat(messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

    # Save assistant response
    assistant_msg = ChatHistory(
        session_id=request.session_id,
        role="assistant",
        content=response_text,
        mode=request.mode,
        timestamp=datetime.utcnow(),
    )
    db.add(assistant_msg)
    db.commit()

    return ChatResponse(response=response_text, knowledge_points=[])


@router.post("/hint", response_model=HintResponse)
async def get_hint(request: HintRequest, db: Session = Depends(get_db)):
    """Get a hint for code."""
    messages = build_hint_prompt(
        request.code,
        request.error_description or "",
        request.current_hint_level,
        request.programming_language,
    )

    try:
        hint_text = await llm_client.chat(messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

    return HintResponse(
        hint=hint_text,
        hint_level=request.current_hint_level,
        next_hint_available=request.current_hint_level < 4,
    )


@router.post("/exercise", response_model=Exercise)
async def generate_exercise(request: ExerciseRequest, db: Session = Depends(get_db)):
    """Generate a programming exercise."""
    # Get knowledge context
    knowledge = (
        db.query(StudentKnowledge)
        .filter(StudentKnowledge.session_id == "default")
        .all()
    )
    knowledge_context = ""
    if knowledge:
        weak = [k.knowledge_point for k in knowledge if k.mastery_level < 0.5]
        if weak:
            knowledge_context = f"Student's weak knowledge points: {', '.join(weak)}"

    messages = build_exercise_prompt(
        request.topic, request.difficulty, request.programming_language, knowledge_context
    )

    try:
        response_text = await llm_client.chat(messages, temperature=0.8)
        # Try to parse JSON from response
        exercise_data = json.loads(response_text.strip().strip("```json").strip("```"))
        return Exercise(**exercise_data)
    except json.JSONDecodeError:
        # If JSON parsing fails, return a basic exercise
        return Exercise(
            title=request.topic,
            description=response_text,
            input_example="",
            output_example="",
            test_cases=[],
            knowledge_points=[request.topic],
            difficulty=request.difficulty,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/progress/{session_id}", response_model=ProgressReport)
async def get_progress(session_id: str, db: Session = Depends(get_db)):
    """Get student progress report."""
    knowledge = (
        db.query(StudentKnowledge)
        .filter(StudentKnowledge.session_id == session_id)
        .all()
    )

    total_questions = (
        db.query(ExerciseRecord).filter(ExerciseRecord.session_id == session_id).count()
    )

    knowledge_summary = {}
    weak_points = []
    for k in knowledge:
        knowledge_summary[k.knowledge_point] = {
            "mastery": k.mastery_level,
            "attempts": k.attempts,
        }
        if k.mastery_level < 0.5:
            weak_points.append(k.knowledge_point)

    recommendations = []
    if weak_points:
        recommendations.append(f"Recommended review: {', '.join(weak_points[:3])}")
    if total_questions < 10:
        recommendations.append("Practice more exercises to consolidate knowledge")

    return ProgressReport(
        session_id=session_id,
        total_questions=total_questions,
        knowledge_points_summary=knowledge_summary,
        weak_points=weak_points,
        recommendations=recommendations,
    )

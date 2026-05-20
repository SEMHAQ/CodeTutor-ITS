"""
Knowledge Tracking Module for CodeTutor-ITS
Tracks student mastery of programming knowledge points.
"""

from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from backend.database.db import StudentKnowledge, ChatHistory, ExerciseRecord
from llm.client import llm_client
from llm.prompts import build_knowledge_analysis_prompt
import config


class KnowledgeTracker:
    """Tracks and updates student knowledge mastery levels."""

    def __init__(self, db: Session, session_id: str):
        self.db = db
        self.session_id = session_id

    def get_knowledge_state(self) -> Dict[str, Dict]:
        """Get current knowledge state for the student."""
        records = (
            self.db.query(StudentKnowledge)
            .filter(StudentKnowledge.session_id == self.session_id)
            .all()
        )
        return {
            r.knowledge_point: {
                "mastery": r.mastery_level,
                "attempts": r.attempts,
                "correct": r.correct_attempts,
                "last_updated": r.last_updated,
            }
            for r in records
        }

    def update_knowledge(self, knowledge_point: str, is_correct: bool):
        """Update mastery level for a specific knowledge point."""
        record = (
            self.db.query(StudentKnowledge)
            .filter(
                StudentKnowledge.session_id == self.session_id,
                StudentKnowledge.knowledge_point == knowledge_point,
            )
            .first()
        )

        if not record:
            record = StudentKnowledge(
                session_id=self.session_id,
                knowledge_point=knowledge_point,
                mastery_level=0.0,
                attempts=0,
                correct_attempts=0,
            )
            self.db.add(record)

        record.attempts += 1
        if is_correct:
            record.correct_attempts += 1

        # Bayesian-inspired mastery update
        # mastery = correct / attempts, smoothed with prior
        prior_weight = 2  # equivalent to 2 prior attempts at 50%
        prior_correct = 1
        record.mastery_level = (record.correct_attempts + prior_correct) / (
            record.attempts + prior_weight
        )

        record.last_updated = datetime.utcnow()
        self.db.commit()

        return record.mastery_level

    async def analyze_from_chat_history(self) -> Dict:
        """Analyze knowledge levels from chat history using LLM."""
        history = (
            self.db.query(ChatHistory)
            .filter(ChatHistory.session_id == self.session_id)
            .order_by(ChatHistory.timestamp)
            .limit(30)
            .all()
        )

        if not history:
            return {"knowledge_levels": {}, "weak_points": [], "recommendations": []}

        chat_data = [{"role": h.role, "content": h.content} for h in history]
        messages = build_knowledge_analysis_prompt(chat_data, "python")

        try:
            response = await llm_client.chat(messages, temperature=0.3)
            import json

            result = json.loads(response.strip().strip("```json").strip("```"))

            # Update database with analyzed knowledge levels
            for kp, data in result.get("knowledge_levels", {}).items():
                self._update_analyzed_knowledge(kp, data.get("mastery", 0.5))

            return result
        except Exception:
            return {"knowledge_levels": {}, "weak_points": [], "recommendations": []}

    def _update_analyzed_knowledge(self, knowledge_point: str, mastery: float):
        """Update knowledge from LLM analysis."""
        record = (
            self.db.query(StudentKnowledge)
            .filter(
                StudentKnowledge.session_id == self.session_id,
                StudentKnowledge.knowledge_point == knowledge_point,
            )
            .first()
        )

        if not record:
            record = StudentKnowledge(
                session_id=self.session_id,
                knowledge_point=knowledge_point,
                mastery_level=mastery,
                attempts=0,
                correct_attempts=0,
            )
            self.db.add(record)
        else:
            # Weighted average with existing data
            if record.attempts > 0:
                record.mastery_level = 0.7 * record.mastery_level + 0.3 * mastery
            else:
                record.mastery_level = mastery

        record.last_updated = datetime.utcnow()
        self.db.commit()

    def get_weak_points(self, threshold: float = 0.5) -> List[str]:
        """Get knowledge points below mastery threshold."""
        records = (
            self.db.query(StudentKnowledge)
            .filter(
                StudentKnowledge.session_id == self.session_id,
                StudentKnowledge.mastery_level < threshold,
            )
            .all()
        )
        return [r.knowledge_point for r in records]

    def get_recommendations(self) -> List[str]:
        """Generate learning recommendations based on knowledge state."""
        weak_points = self.get_weak_points()
        if not weak_points:
            return ["你对当前知识点掌握良好！可以尝试更高难度的练习。"]

        recommendations = []
        for point in weak_points[:3]:
            recommendations.append(f"建议复习'{point}'，尝试相关练习题巩固。")

        return recommendations

    def get_progress_summary(self) -> Dict:
        """Get a summary of student progress."""
        records = (
            self.db.query(StudentKnowledge)
            .filter(StudentKnowledge.session_id == self.session_id)
            .all()
        )

        if not records:
            return {
                "total_points": 0,
                "mastered": 0,
                "learning": 0,
                "weak": 0,
                "average_mastery": 0.0,
            }

        mastered = sum(1 for r in records if r.mastery_level >= 0.8)
        learning = sum(1 for r in records if 0.5 <= r.mastery_level < 0.8)
        weak = sum(1 for r in records if r.mastery_level < 0.5)
        avg = sum(r.mastery_level for r in records) / len(records)

        return {
            "total_points": len(records),
            "mastered": mastered,
            "learning": learning,
            "weak": weak,
            "average_mastery": round(avg, 2),
        }

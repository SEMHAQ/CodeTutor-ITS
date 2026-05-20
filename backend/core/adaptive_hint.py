"""
Adaptive Hint System for CodeTutor-ITS
Manages multi-level hint generation based on student interaction history.
"""

from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from backend.database.db import ChatHistory, StudentKnowledge
from llm.client import llm_client
from llm.prompts import build_hint_prompt


class AdaptiveHintManager:
    """Manages adaptive hint levels based on student progress."""

    HINT_LEVELS = {
        1: {
            "name": "方向提示",
            "description": "指出错误类型和大致方向，不透露具体位置",
            "prompt_addon": "只给出一个简短的方向性提示，比如'检查循环条件'或'注意变量作用域'。",
        },
        2: {
            "name": "位置提示",
            "description": "指出错误所在的具体位置和原因",
            "prompt_addon": "指出错误的大致位置和原因，比如'第5行的for循环条件有误，会导致死循环'。",
        },
        3: {
            "name": "思路提示",
            "description": "给出修复思路，但不给出完整代码",
            "prompt_addon": "给出修复的思路和步骤，比如'将while True改为while len(queue) > 0'。",
        },
        4: {
            "name": "完整解答",
            "description": "给出完整的修复代码和详细解释",
            "prompt_addon": "给出完整的修复代码，并详细解释为什么这样修改。",
        },
    }

    def __init__(self, db: Session, session_id: str):
        self.db = db
        self.session_id = session_id

    def determine_hint_level(self, current_level: int, student_attempts: int) -> int:
        """Determine appropriate hint level based on student history."""
        # Auto-escalate after multiple failed attempts
        if student_attempts >= 3 and current_level < 4:
            return min(current_level + 1, 4)
        return current_level

    async def generate_hint(
        self,
        code: str,
        error_description: Optional[str] = None,
        hint_level: int = 1,
        programming_language: str = "python",
    ) -> Dict:
        """Generate a hint at the specified level."""
        level_info = self.HINT_LEVELS.get(hint_level, self.HINT_LEVELS[1])

        messages = build_hint_prompt(
            code=code,
            error_description=error_description or "",
            hint_level=hint_level,
            programming_language=programming_language,
        )

        # Add specific guidance for this hint level
        messages.append(
            {
                "role": "user",
                "content": level_info["prompt_addon"],
            }
        )

        try:
            hint_text = await llm_client.chat(messages)
        except Exception as e:
            hint_text = f"生成提示时出错：{str(e)}"

        # Save hint interaction to history
        self._save_interaction(code, hint_text, hint_level)

        return {
            "hint": hint_text,
            "hint_level": hint_level,
            "level_name": level_info["name"],
            "next_hint_available": hint_level < 4,
            "next_level_description": (
                self.HINT_LEVELS[hint_level + 1]["description"] if hint_level < 4 else None
            ),
        }

    def _save_interaction(self, code: str, hint: str, hint_level: int):
        """Save hint interaction to chat history."""
        user_msg = ChatHistory(
            session_id=self.session_id,
            role="user",
            content=f"[代码提交 - 提示级别{hint_level}]\n{code}",
            mode="hint",
            timestamp=datetime.utcnow(),
        )
        assistant_msg = ChatHistory(
            session_id=self.session_id,
            role="assistant",
            content=f"[提示级别{hint_level}] {hint}",
            mode="hint",
            timestamp=datetime.utcnow(),
        )
        self.db.add(user_msg)
        self.db.add(assistant_msg)
        self.db.commit()

    def get_hint_history(self) -> List[Dict]:
        """Get hint interaction history for this session."""
        history = (
            self.db.query(ChatHistory)
            .filter(
                ChatHistory.session_id == self.session_id,
                ChatHistory.mode == "hint",
            )
            .order_by(ChatHistory.timestamp)
            .all()
        )
        return [
            {"role": h.role, "content": h.content, "timestamp": h.timestamp}
            for h in history
        ]

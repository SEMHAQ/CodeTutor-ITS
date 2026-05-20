import config


def build_tutor_prompt(
    user_message: str,
    chat_history: list,
    programming_language: str = "python",
    knowledge_context: str = "",
) -> list:
    """Build prompt for tutoring mode."""
    messages = [{"role": "system", "content": config.SYSTEM_PROMPTS["tutor"]}]

    if knowledge_context:
        messages.append(
            {
                "role": "system",
                "content": f"学生当前知识状态：{knowledge_context}",
            }
        )

    # Add chat history (last 10 messages)
    for msg in chat_history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})
    return messages


def build_hint_prompt(
    code: str,
    error_description: str,
    hint_level: int,
    programming_language: str = "python",
    chat_history: list = None,
) -> list:
    """Build prompt for hint system."""
    messages = [{"role": "system", "content": config.SYSTEM_PROMPTS["hint_system"]}]

    hint_guidance = {
        1: "给出一个非常简短的提示，只指出错误类型，不要透露具体位置。",
        2: "给出中等程度的提示，指出大致的错误区域和原因。",
        3: "给出较详细的提示，说明如何修复，但不给出完整代码。",
        4: "给出完整的解答和详细解释。",
    }

    prompt = f"""学生提交了以下{programming_language}代码：

```{programming_language}
{code}
```

"""
    if error_description:
        prompt += f"学生描述的问题：{error_description}\n\n"

    prompt += f"当前提示级别：{hint_level}\n"
    prompt += f"指导：{hint_guidance.get(hint_level, hint_guidance[1])}"

    messages.append({"role": "user", "content": prompt})

    if chat_history:
        for msg in chat_history[-6:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

    return messages


def build_exercise_prompt(
    topic: str,
    difficulty: str,
    programming_language: str,
    knowledge_context: str = "",
) -> list:
    """Build prompt for exercise generation."""
    messages = [{"role": "system", "content": config.SYSTEM_PROMPTS["exercise_generator"]}]

    prompt = f"""请生成一道编程练习题：

主题：{topic}
难度：{difficulty}
编程语言：{programming_language}

"""
    if knowledge_context:
        prompt += f"学生当前知识水平：{knowledge_context}\n\n"

    prompt += """请按以下JSON格式输出（只输出JSON，不要其他内容）：
{
    "title": "题目标题",
    "description": "题目描述（详细说明要求）",
    "input_example": "输入示例",
    "output_example": "输出示例",
    "test_cases": [
        {"input": "测试输入1", "expected_output": "期望输出1"},
        {"input": "测试输入2", "expected_output": "期望输出2"}
    ],
    "knowledge_points": ["涉及的知识点1", "涉及的知识点2"],
    "difficulty": "easy/medium/hard"
}"""

    messages.append({"role": "user", "content": prompt})
    return messages


def build_knowledge_analysis_prompt(
    chat_history: list, programming_language: str
) -> list:
    """Build prompt to analyze student's knowledge from chat history."""
    messages = [
        {
            "role": "system",
            "content": "你是一个教育分析专家。根据学生的对话历史，分析他们对各个编程知识点的掌握程度。",
        }
    ]

    history_text = "\n".join(
        [f"{msg['role']}: {msg['content'][:200]}" for msg in chat_history[-20:]]
    )

    prompt = f"""请分析以下学生对话历史，评估学生对各知识点的掌握程度：

{history_text}

请按以下JSON格式输出（只输出JSON）：
{{
    "knowledge_levels": {{
        "知识点1": {{"mastery": 0.0-1.0, "evidence": "判断依据"}},
        "知识点2": {{"mastery": 0.0-1.0, "evidence": "判断依据"}}
    }},
    "weak_points": ["薄弱知识点列表"],
    "recommendations": ["学习建议列表"]
}}"""

    messages.append({"role": "user", "content": prompt})
    return messages

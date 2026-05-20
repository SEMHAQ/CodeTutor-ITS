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
                "content": f"Student's current knowledge state: {knowledge_context}",
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
        1: "Give a very brief hint, only indicate the error type without revealing the specific location.",
        2: "Give a moderate hint, indicating the general error area and reason.",
        3: "Give a detailed hint explaining how to fix, but without providing complete code.",
        4: "Provide the complete solution with detailed explanation.",
    }

    prompt = f"""The student submitted the following {programming_language} code:

```{programming_language}
{code}
```

"""
    if error_description:
        prompt += f"Student's description of the problem: {error_description}\n\n"

    prompt += f"Current hint level: {hint_level}\n"
    prompt += f"Guidance: {hint_guidance.get(hint_level, hint_guidance[1])}"

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

    prompt = f"""Please generate a programming exercise:

Topic: {topic}
Difficulty: {difficulty}
Programming Language: {programming_language}

"""
    if knowledge_context:
        prompt += f"Student's current knowledge level: {knowledge_context}\n\n"

    prompt += """Please output in the following JSON format (output JSON only, no other content):
{
    "title": "Exercise title",
    "description": "Detailed problem description with requirements",
    "input_example": "Input example",
    "output_example": "Output example",
    "test_cases": [
        {"input": "test input 1", "expected_output": "expected output 1"},
        {"input": "test input 2", "expected_output": "expected output 2"}
    ],
    "knowledge_points": ["knowledge point 1", "knowledge point 2"],
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
            "content": "You are an education analytics expert. Analyze the student's chat history to assess their mastery of various programming knowledge points.",
        }
    ]

    history_text = "\n".join(
        [f"{msg['role']}: {msg['content'][:200]}" for msg in chat_history[-20:]]
    )

    prompt = f"""Please analyze the following student chat history and assess their mastery of each knowledge point:

{history_text}

Please output in the following JSON format (JSON only):
{{
    "knowledge_levels": {{
        "knowledge_point_1": {{"mastery": 0.0-1.0, "evidence": "basis for judgment"}},
        "knowledge_point_2": {{"mastery": 0.0-1.0, "evidence": "basis for judgment"}}
    }},
    "weak_points": ["list of weak knowledge points"],
    "recommendations": ["list of learning recommendations"]
}}"""

    messages.append({"role": "user", "content": prompt})
    return messages

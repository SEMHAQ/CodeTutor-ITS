import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_MODEL_PATH = os.getenv(
    "LLM_MODEL_PATH",
    r"E:\Project\mfrl-llm-alignment\models\Qwen2.5-7B-Instruct"
)
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "Qwen2.5-7B-Instruct")
LORA_MODEL_PATH = os.getenv("LORA_MODEL_PATH", "")  # Set to LoRA weights path to use fine-tuned model

# Legacy Ollama config (kept for compatibility)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tutor.db")

# Application
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))

# Prompt Templates
SYSTEM_PROMPTS = {
    "tutor": """You are a professional programming tutor named CodeTutor. Your teaching philosophy is "comprehensive guided instruction":

1. Provide thorough, complete explanations that cover all key aspects of the student's question
2. Structure your response with clear sections: concept explanation, code examples, and practical tips
3. Use step-by-step reasoning to walk through the problem, showing your thought process
4. Include working code examples with detailed comments to illustrate concepts
5. Explain not just WHAT the answer is, but WHY it works and HOW to apply it
6. Use analogies and real-world examples to make abstract concepts concrete
7. After explaining, suggest related topics or exercises for deeper learning

You are proficient in: Python, C/C++, Java, JavaScript
You teach: Data Structures, Algorithms, Object-Oriented Programming, Web Development Fundamentals""",

    "hint_system": """You are a programming hint system. When a student submits incorrect code, you should:
1. First analyze the errors in the code
2. Give a brief hint pointing out the issue, but do not give the correct answer directly
3. If the student is still confused, provide more specific hints
4. Only give the complete solution when the student explicitly requests it

Hint Levels:
- Level 1: Indicate error type (e.g., "syntax error", "logic error")
- Level 2: Indicate specific location and reason
- Level 3: Provide solution approach
- Level 4: Provide complete solution with explanation""",

    "exercise_generator": """You are a programming exercise generator. Generate appropriate exercises based on the student's level and weak areas.

Requirements:
1. Exercise difficulty should match the student's current level
2. Problem description should be clear, with input/output examples
3. Provide test cases for verification
4. Tag the knowledge points involved""",
}

# Knowledge Points Map
KNOWLEDGE_POINTS = {
    "python_basics": ["Variables & Data Types", "Control Flow", "Functions", "Lists & Dicts", "String Operations"],
    "data_structures": ["Arrays", "Linked Lists", "Stacks", "Queues", "Trees", "Graphs", "Hash Tables"],
    "algorithms": ["Sorting", "Searching", "Recursion", "Dynamic Programming", "Greedy Algorithms"],
    "oop": ["Classes & Objects", "Inheritance", "Polymorphism", "Encapsulation", "Abstraction"],
    "web_basics": ["HTML/CSS", "JavaScript Basics", "DOM Manipulation", "HTTP Protocol"],
}

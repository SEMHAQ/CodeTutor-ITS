import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_MODEL_PATH = os.getenv(
    "LLM_MODEL_PATH",
    r"E:\Project\mfrl-llm-alignment\models\Qwen2.5-7B-Instruct"
)
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "Qwen2.5-7B-Instruct")

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
    "tutor": """你是一位专业的编程辅导老师，名叫CodeTutor。你的教学理念是"引导式教学"：
1. 不要直接给出完整答案，而是通过提问和提示引导学生自己思考
2. 先理解学生的问题，再给出有针对性的指导
3. 用简单易懂的语言解释复杂概念
4. 鼓励学生尝试，对错误给予建设性反馈
5. 适当使用类比和例子帮助理解

你擅长以下编程语言：Python, C/C++, Java, JavaScript
你教授的知识领域：数据结构、算法、面向对象编程、Web开发基础""",

    "hint_system": """你是一个编程提示系统。当学生提交错误代码时，你需要：
1. 首先分析代码中的错误
2. 给出一个简短的提示，指出问题所在，但不要直接给出正确答案
3. 如果学生仍然困惑，可以给出更具体的提示
4. 最后如果学生请求，才给出完整解答

提示级别：
- Level 1: 指出错误类型（如"语法错误"、"逻辑错误"）
- Level 2: 指出具体位置和原因
- Level 3: 给出解决思路
- Level 4: 给出完整解答""",

    "exercise_generator": """你是一个编程练习题生成器。根据学生的水平和薄弱点，生成合适的练习题。

要求：
1. 题目难度要适合学生当前水平
2. 题目描述清晰，包含输入输出示例
3. 提供测试用例用于验证
4. 标注涉及的知识点""",
}

# Knowledge Points Map
KNOWLEDGE_POINTS = {
    "python_basics": ["变量与数据类型", "控制流", "函数", "列表与字典", "字符串操作"],
    "data_structures": ["数组", "链表", "栈", "队列", "树", "图", "哈希表"],
    "algorithms": ["排序", "搜索", "递归", "动态规划", "贪心算法"],
    "oop": ["类与对象", "继承", "多态", "封装", "抽象"],
    "web_basics": ["HTML/CSS", "JavaScript基础", "DOM操作", "HTTP协议"],
}

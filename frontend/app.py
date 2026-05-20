import streamlit as st
import httpx
import json
import uuid
from datetime import datetime

# Config
API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="CodeTutor - 智能编程辅导系统",
    page_icon="💻",
    layout="wide",
)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "tutor"
if "language" not in st.session_state:
    st.session_state.language = "python"


def send_message(message: str, mode: str = "tutor", hint_level: int = None):
    """Send message to backend API."""
    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                f"{API_BASE_URL}/api/tutor/chat",
                json={
                    "message": message,
                    "session_id": st.session_state.session_id,
                    "mode": mode,
                    "programming_language": st.session_state.language,
                    "hint_level": hint_level,
                },
            )
            response.raise_for_status()
            return response.json()
    except httpx.ConnectError:
        return {"response": "无法连接到后端服务，请确保FastAPI服务已启动。"}
    except Exception as e:
        return {"response": f"错误：{str(e)}"}


def generate_exercise(topic: str, difficulty: str):
    """Generate an exercise from backend."""
    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                f"{API_BASE_URL}/api/tutor/exercise",
                json={
                    "topic": topic,
                    "difficulty": difficulty,
                    "programming_language": st.session_state.language,
                    "session_id": st.session_state.session_id,
                },
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"title": "错误", "description": str(e)}


def get_progress():
    """Get student progress."""
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"{API_BASE_URL}/api/tutor/progress/{st.session_state.session_id}"
            )
            response.raise_for_status()
            return response.json()
    except Exception:
        return None


# Sidebar
with st.sidebar:
    st.title("CodeTutor")
    st.caption("智能编程辅导系统")

    st.divider()

    # Mode selection
    st.subheader("辅导模式")
    mode = st.radio(
        "选择模式",
        ["tutor", "hint", "exercise"],
        format_func=lambda x: {
            "tutor": "对话辅导",
            "hint": "代码提示",
            "exercise": "练习生成",
        }[x],
        index=0,
    )
    st.session_state.mode = mode

    st.divider()

    # Language selection
    st.subheader("编程语言")
    language = st.selectbox(
        "选择语言",
        ["python", "c", "cpp", "java", "javascript"],
        format_func=lambda x: {
            "python": "Python",
            "c": "C",
            "cpp": "C++",
            "java": "Java",
            "javascript": "JavaScript",
        }[x],
    )
    st.session_state.language = language

    st.divider()

    # Session info
    st.subheader("会话信息")
    st.text(f"ID: {st.session_state.session_id[:8]}...")
    st.text(f"消息数: {len(st.session_state.messages)}")

    if st.button("清除对话"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # Progress button
    if st.button("查看学习进度"):
        progress = get_progress()
        if progress:
            st.json(progress)

# Main area
st.title("CodeTutor - 智能编程辅导系统")
st.caption("基于开源大语言模型的编程教育智能辅导系统")

# Display mode description
mode_descriptions = {
    "tutor": "在对话辅导模式下，我可以回答你的编程问题，解释概念，帮你理解代码。我不会直接给答案，而是引导你思考。",
    "hint": "在代码提示模式下，你可以提交有错误的代码，我会逐步给出提示帮你找到问题。",
    "exercise": "在练习生成模式下，告诉我你想练习什么主题，我会为你生成合适的练习题。",
}
st.info(mode_descriptions[mode])

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("输入你的编程问题..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            if mode == "exercise":
                result = generate_exercise(prompt, "medium")
                response = f"### {result.get('title', '练习题')}\n\n"
                response += result.get("description", "")
                if result.get("input_example"):
                    response += f"\n\n**输入示例：** `{result['input_example']}`"
                if result.get("output_example"):
                    response += f"\n**输出示例：** `{result['output_example']}`"
            else:
                result = send_message(prompt, mode)
                response = result.get("response", "抱歉，出现了错误。")

        st.markdown(response)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

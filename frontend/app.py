import streamlit as st
import httpx
import json
import uuid
from datetime import datetime

# Config
API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="CodeTutor - Intelligent Programming Tutoring System",
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
        return {"response": "Cannot connect to backend service. Please ensure FastAPI is running."}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}


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
        return {"title": "Error", "description": str(e)}


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
    st.caption("Intelligent Programming Tutor")

    st.divider()

    # Mode selection
    st.subheader("Tutoring Mode")
    mode = st.radio(
        "Select Mode",
        ["tutor", "hint", "exercise"],
        format_func=lambda x: {
            "tutor": "Dialogue Tutor",
            "hint": "Code Hints",
            "exercise": "Exercise Generator",
        }[x],
        index=0,
    )
    st.session_state.mode = mode

    st.divider()

    # Language selection
    st.subheader("Programming Language")
    language = st.selectbox(
        "Select Language",
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
    st.subheader("Session Info")
    st.text(f"ID: {st.session_state.session_id[:8]}...")
    st.text(f"Messages: {len(st.session_state.messages)}")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # Progress button
    if st.button("View Learning Progress"):
        progress = get_progress()
        if progress:
            st.json(progress)

# Main area
st.title("CodeTutor - Intelligent Programming Tutoring System")
st.caption("An LLM-powered intelligent tutoring system for programming education")

# Display mode description
mode_descriptions = {
    "tutor": "In Dialogue Tutor mode, I can answer your programming questions, explain concepts, and help you understand code. I won't give direct answers but guide you to think.",
    "hint": "In Code Hints mode, you can submit code with errors, and I'll provide progressive hints to help you find the issues.",
    "exercise": "In Exercise Generator mode, tell me what topic you want to practice, and I'll generate appropriate exercises for you.",
}
st.info(mode_descriptions[mode])

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Enter your programming question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if mode == "exercise":
                result = generate_exercise(prompt, "medium")
                response = f"### {result.get('title', 'Exercise')}\n\n"
                response += result.get("description", "")
                if result.get("input_example"):
                    response += f"\n\n**Input Example:** `{result['input_example']}`"
                if result.get("output_example"):
                    response += f"\n**Output Example:** `{result['output_example']}`"
            else:
                result = send_message(prompt, mode)
                response = result.get("response", "Sorry, an error occurred.")

        st.markdown(response)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

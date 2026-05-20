#!/bin/bash
# CodeTutor-ITS Startup Script

echo "Starting CodeTutor-ITS..."
echo "================================"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "WARNING: Ollama is not running!"
    echo "Please start Ollama first: ollama serve"
    echo "And pull the model: ollama pull qwen2.5:7b"
    echo ""
fi

# Start FastAPI backend
echo "Starting FastAPI backend on port 8000..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start Streamlit frontend
echo "Starting Streamlit frontend on port 8501..."
streamlit run frontend/app.py --server.port 8501 &
FRONTEND_PID=$!

echo "================================"
echo "CodeTutor-ITS is running!"
echo "Backend API: http://localhost:8000"
echo "Frontend UI: http://localhost:8501"
echo "API Docs: http://localhost:8000/docs"
echo "================================"
echo "Press Ctrl+C to stop"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM
wait

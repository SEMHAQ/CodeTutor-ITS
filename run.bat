@echo off
REM CodeTutor-ITS Startup Script for Windows

echo Starting CodeTutor-ITS...
echo ================================

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo WARNING: Ollama is not running!
    echo Please start Ollama first: ollama serve
    echo And pull the model: ollama pull qwen2.5:7b
    echo.
)

REM Start FastAPI backend
echo Starting FastAPI backend on port 8000...
start "CodeTutor-Backend" cmd /c "uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start Streamlit frontend
echo Starting Streamlit frontend on port 8501...
start "CodeTutor-Frontend" cmd /c "streamlit run frontend/app.py --server.port 8501"

echo ================================
echo CodeTutor-ITS is running!
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:8501
echo API Docs: http://localhost:8000/docs
echo ================================
echo Close this window to stop services.
pause

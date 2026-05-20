# CodeTutor-ITS Startup Script for PowerShell

Write-Host "Starting CodeTutor-ITS..." -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check if Ollama is running
try {
    $null = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -ErrorAction Stop
    Write-Host "[OK] Ollama is running" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Ollama is not running!" -ForegroundColor Yellow
    Write-Host "Please start Ollama first: ollama serve" -ForegroundColor Yellow
    Write-Host "And pull the model: ollama pull qwen2.5:7b" -ForegroundColor Yellow
    Write-Host ""
}

# Start FastAPI backend
Write-Host "Starting FastAPI backend on port 8000..." -ForegroundColor Cyan
$backend = Start-Process -FilePath "uvicorn" -ArgumentList "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" -PassThru -NoNewWindow

# Wait for backend to start
Start-Sleep -Seconds 3

# Start Streamlit frontend
Write-Host "Starting Streamlit frontend on port 8501..." -ForegroundColor Cyan
$frontend = Start-Process -FilePath "streamlit" -ArgumentList "run", "frontend/app.py", "--server.port", "8501" -PassThru -NoNewWindow

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "CodeTutor-ITS is running!" -ForegroundColor Green
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Green
Write-Host "Frontend UI: http://localhost:8501" -ForegroundColor Green
Write-Host "API Docs:    http://localhost:8000/docs" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow

# Handle cleanup on exit
try {
    $backend.WaitForExit()
} finally {
    Stop-Process -Id $backend.Id -ErrorAction SilentlyContinue
    Stop-Process -Id $frontend.Id -ErrorAction SilentlyContinue
    Write-Host "Services stopped." -ForegroundColor Red
}

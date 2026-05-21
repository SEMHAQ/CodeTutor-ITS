# LoRA Fine-tune Pipeline - PowerShell Script
# Usage: .\experiments\scripts\run_lora_pipeline.ps1

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $projectRoot

# === Config ===
# Set OPENROUTER_API_KEY before running:
#   $env:OPENROUTER_API_KEY = "sk-or-v1-..."
if (-not $env:OPENROUTER_API_KEY) {
    Write-Host "ERROR: Set OPENROUTER_API_KEY first: `$env:OPENROUTER_API_KEY = 'your-key'" -ForegroundColor Red
    exit 1
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " LoRA Fine-tune Pipeline" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# === Step 1: Start backend ===
Write-Host "`n[1/5] Starting backend server..." -ForegroundColor Yellow
$backend = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000" -PassThru -NoNewWindow

# Wait for backend to be ready
Write-Host "Waiting for backend to start..." -ForegroundColor Gray
$maxWait = 120
$waited = 0
while ($waited -lt $maxWait) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Host "Backend ready!" -ForegroundColor Green
            break
        }
    } catch {}
    Start-Sleep -Seconds 2
    $waited += 2
    Write-Host "." -NoNewline -ForegroundColor Gray
}
if ($waited -ge $maxWait) {
    Write-Host "`nERROR: Backend failed to start within ${maxWait}s" -ForegroundColor Red
    Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue
    exit 1
}

# === Step 2: Generate training data ===
Write-Host "`n[2/5] Generating training data..." -ForegroundColor Yellow
python experiments/scripts/generate_training_data.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Training data generation failed" -ForegroundColor Red
    Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue
    exit 1
}

# === Step 3: Stop backend (no longer needed) ===
Write-Host "`nStopping backend server..." -ForegroundColor Gray
Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# === Step 4: LoRA fine-tune ===
Write-Host "`n[3/5] Running LoRA fine-tune..." -ForegroundColor Yellow
python experiments/scripts/lora_finetune.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: LoRA fine-tune failed" -ForegroundColor Red
    exit 1
}

# === Step 5: Evaluate (OpenRouter judge) ===
Write-Host "`n[4/5] Evaluating with OpenRouter judge..." -ForegroundColor Yellow
python experiments/scripts/finetune_evaluation.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Evaluation failed" -ForegroundColor Red
    exit 1
}

# === Step 6: Generate charts ===
Write-Host "`n[5/5] Generating charts..." -ForegroundColor Yellow
python experiments/scripts/generate_charts.py
Copy-Item "experiments/charts/finetune_comparison.pdf" "docs/figures/" -Force

Write-Host "`n========================================" -ForegroundColor Green
Write-Host " Pipeline complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  git add experiments/results/ experiments/data/training_data.jsonl docs/figures/finetune_comparison.pdf"
Write-Host '  git commit -m "exp: rerun LoRA with optimized pipeline"'
Write-Host "  git push"

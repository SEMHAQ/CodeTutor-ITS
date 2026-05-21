# LoRA Fine-tune Pipeline
# Prerequisites: backend must be running on localhost:8000
# Usage:
#   Terminal 1: python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
#   Terminal 2: $env:OPENROUTER_API_KEY = "sk-or-v1-..."; .\experiments\scripts\run_lora_pipeline.ps1

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))

if (-not $env:OPENROUTER_API_KEY) {
    Write-Host "ERROR: Set OPENROUTER_API_KEY first" -ForegroundColor Red
    exit 1
}

Write-Host "[1/4] Generating training data (backend must be running)..." -ForegroundColor Yellow
python experiments/scripts/generate_training_data.py
if ($LASTEXITCODE -ne 0) { Write-Host "FAILED" -ForegroundColor Red; exit 1 }

Write-Host "`n[2/4] LoRA fine-tune..." -ForegroundColor Yellow
python experiments/scripts/lora_finetune.py
if ($LASTEXITCODE -ne 0) { Write-Host "FAILED" -ForegroundColor Red; exit 1 }

Write-Host "`n[3/4] Evaluating (OpenRouter judge)..." -ForegroundColor Yellow
python experiments/scripts/finetune_evaluation.py
if ($LASTEXITCODE -ne 0) { Write-Host "FAILED" -ForegroundColor Red; exit 1 }

Write-Host "`n[4/4] Generating charts..." -ForegroundColor Yellow
python experiments/scripts/generate_charts.py
Copy-Item "experiments/charts/finetune_comparison.pdf" "docs/figures/" -Force

Write-Host "`nDone! Now commit and push." -ForegroundColor Green

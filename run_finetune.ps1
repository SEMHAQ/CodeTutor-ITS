$ErrorActionPreference = "Continue"

Write-Host "=== LoRA Fine-tuning Pipeline ==="
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""

# Step 1: Generate training data (needs backend running)
Write-Host "[1/5] Generating training data (250 examples, ~1h)..."
python -u experiments/scripts/generate_training_data.py --count 250
Write-Host "[1/5] Done. Exit code: $LASTEXITCODE"
Write-Host ""

# Step 2: Install training dependencies
Write-Host "[2/5] Installing training dependencies..."
pip install peft datasets accelerate bitsandbytes 2>&1 | Out-Null
Write-Host "[2/5] Done."
Write-Host ""

# Step 3: LoRA fine-tuning (3-5 hours on 3090)
Write-Host "[3/5] LoRA fine-tuning Qwen2.5-7B (3-5 hours)..."
python -u experiments/scripts/lora_finetune.py --epochs 3 --batch-size 4 --lr 2e-4
Write-Host "[3/5] Done. Exit code: $LASTEXITCODE"
Write-Host ""

# Step 4: Evaluate fine-tuned vs base model
Write-Host "[4/5] Evaluating fine-tuned vs base model..."
python -u experiments/scripts/finetune_evaluation.py --sample 50
Write-Host "[4/5] Done. Exit code: $LASTEXITCODE"
Write-Host ""

# Step 5: Generate charts
Write-Host "[5/5] Generating charts..."
python experiments/scripts/generate_charts.py
Write-Host "[5/5] Done."
Write-Host ""

# Push results
Write-Host "Pushing results..."
git add experiments/results/ experiments/charts/ experiments/models/
git commit -m "exp: LoRA fine-tuning results and comparison"
git push
Write-Host "Push complete."

Write-Host ""
Write-Host "=== Pipeline Complete ==="
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

$ErrorActionPreference = "Continue"

Write-Host "=== Baseline Experiment Started ==="
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

# Step 1: Generate baseline responses
Write-Host ""
Write-Host "[1/2] Generating baseline responses (50 questions, ~2.5h)..."
python -u experiments/scripts/baseline_comparison.py generate --sample 50
Write-Host "[1/2] Done. Exit code: $LASTEXITCODE"

# Step 2: Compare with judge
Write-Host ""
Write-Host "[2/2] Comparing system vs baseline with GPT-as-Judge (~1h)..."
python -u experiments/scripts/baseline_comparison.py compare --sample 50
Write-Host "[2/2] Done. Exit code: $LASTEXITCODE"

# Step 3: Generate new charts
Write-Host ""
Write-Host "[3/3] Generating charts..."
python experiments/scripts/generate_charts.py
Write-Host "[3/3] Done."

# Step 4: Push
Write-Host ""
Write-Host "[4/4] Pushing results..."
git add experiments/results/ experiments/charts/
git commit -m "exp: baseline comparison results"
git push
Write-Host "[4/4] Done."

Write-Host ""
Write-Host "=== Baseline Experiment Complete ==="
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

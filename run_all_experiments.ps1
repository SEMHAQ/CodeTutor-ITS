# ============================================================
# CodeTutor-ITS Full Experiment Pipeline
# Runs all experiments, generates charts, pushes results.
# Max runtime: ~8 hours. Continues on errors.
# ============================================================

$ErrorActionPreference = "Continue"
$StartTime = Get-Date
$MaxRuntime = New-TimeSpan -Hours 8
$LogDir = "experiments\logs"
$ResultsDir = "experiments\results"
$ChartsDir = "experiments\charts"

# Create directories
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
New-Item -ItemType Directory -Force -Path $ResultsDir | Out-Null
New-Item -ItemType Directory -Force -Path $ChartsDir | Out-Null

$LogFile = "$LogDir\run_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

function Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] $msg"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line
}

function TimeLeft {
    $elapsed = (Get-Date) - $StartTime
    return $MaxRuntime - $elapsed
}

function HasTime($minutes) {
    return (TimeLeft).TotalMinutes -gt $minutes
}

Log "=== CodeTutor-ITS Experiment Pipeline Started ==="
Log "Max runtime: 8 hours"
Log ""

# ------------------------------------------------------------
# Step 0: Pull latest code
# ------------------------------------------------------------
Log "Step 0: Pulling latest code..."
try {
    git pull 2>&1 | ForEach-Object { Log "  $_" }
    Log "Git pull done."
} catch {
    Log "Git pull failed: $_"
}
Log ""

# ------------------------------------------------------------
# Step 1: Install dependencies
# ------------------------------------------------------------
Log "Step 1: Installing dependencies..."
try {
    pip install huggingface_hub rouge-score nltk pandas matplotlib seaborn 2>&1 | ForEach-Object { Log "  $_" }
    Log "Dependencies installed."
} catch {
    Log "Dependency install failed: $_"
}
Log ""

# ------------------------------------------------------------
# Step 2: Check backend is running (user starts manually)
# ------------------------------------------------------------
Log "Step 2: Checking backend..."
try {
    $health = Invoke-WebRequest -Uri "http://localhost:8000/docs" -TimeoutSec 10 -ErrorAction Stop
    Log "Backend is running (status $($health.StatusCode))"
} catch {
    Log "WARNING: Backend not responding at localhost:8000. Start it first!"
    Log "  Run: python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"
    Log "  Press Enter to continue anyway (some experiments will fail)..."
    Read-Host
}
Log ""

# ------------------------------------------------------------
# Helper: Run a step with error handling
# ------------------------------------------------------------
function RunStep($name, $command, $timeoutMinutes = 120) {
    if (-not (HasTime 5)) {
        Log "SKIP $name - not enough time remaining"
        return
    }
    Log "Starting: $name (timeout: ${timeoutMinutes}min)"
    try {
        $proc = Start-Process -FilePath "python" -ArgumentList $command `
            -PassThru -NoNewWindow `
            -RedirectStandardOutput "$LogDir\$($name -replace ' ','_')_stdout.log" `
            -RedirectStandardError "$LogDir\$($name -replace ' ','_')_stderr.log"

        $completed = $proc.WaitForExit($timeoutMinutes * 60 * 1000)
        if ($completed) {
            Log "  Finished: $name (exit code: $($proc.ExitCode))"
        } else {
            Log "  TIMEOUT: $name after ${timeoutMinutes}min, killing..."
            $proc.Kill()
        }
    } catch {
        Log "  ERROR in $name : $_"
    }
    Log ""
}

# ------------------------------------------------------------
# Step 3: Experiment 1 - Tutoring Quality (BLEU/ROUGE-L)
# ------------------------------------------------------------
if (HasTime 60) {
    RunStep "Exp1-TutoringQuality" "-u experiments/scripts/evaluate_tutoring_quality.py --sample 50" 90
} else {
    Log "SKIP Exp1 - not enough time"
}

# ------------------------------------------------------------
# Step 4: Experiment 2 - Prompt Comparison
# ------------------------------------------------------------
if (HasTime 90) {
    RunStep "Exp2-PromptComparison" "-u experiments/scripts/prompt_comparison.py --sample 50" 120
} else {
    Log "SKIP Exp2 - not enough time"
}

# ------------------------------------------------------------
# Step 5: Experiment 3 - Ablation Study
# ------------------------------------------------------------
if (HasTime 120) {
    RunStep "Exp3-AblationStudy" "-u experiments/scripts/ablation_study.py --sample 50" 180
} else {
    Log "SKIP Exp3 - not enough time"
}

# ------------------------------------------------------------
# Step 6: Experiment 4 - GPT-as-Judge
# ------------------------------------------------------------
if (HasTime 30) {
    RunStep "Exp4-GPTJudge" "-u experiments/scripts/gpt_judge_evaluation.py --sample 50" 60
} else {
    Log "SKIP Exp4 - not enough time"
}

# ------------------------------------------------------------
# Step 7: Experiment 5 - Generate Baseline Responses
# ------------------------------------------------------------
if (HasTime 60) {
    RunStep "Exp5-BaselineGen" "-u experiments/scripts/baseline_comparison.py generate --sample 50" 90
} else {
    Log "SKIP Exp5 - not enough time"
}

# ------------------------------------------------------------
# Step 8: Experiment 6 - Baseline Comparison (Judge)
# ------------------------------------------------------------
if (HasTime 60) {
    RunStep "Exp6-BaselineCompare" "-u experiments/scripts/baseline_comparison.py compare --sample 50" 120
} else {
    Log "SKIP Exp6 - not enough time"
}

# ------------------------------------------------------------
# Step 9: Generate Charts (PDF)
# ------------------------------------------------------------
Log "Step 9: Generating charts..."
try {
    python experiments/scripts/generate_charts.py 2>&1 | ForEach-Object { Log "  $_" }
    Log "Charts generated."
} catch {
    Log "Chart generation failed: $_"
}
Log ""

# ------------------------------------------------------------
# Step 10: Summary
# ------------------------------------------------------------
Log "=== Results Summary ==="
$resultFiles = Get-ChildItem -Path $ResultsDir -Filter "*.csv" -ErrorAction SilentlyContinue
foreach ($f in $resultFiles) {
    $lines = (Get-Content $f.FullName | Measure-Object -Line).Lines
    Log "  $($f.Name): $lines lines"
}

$chartFiles = Get-ChildItem -Path $ChartsDir -Filter "*.pdf" -ErrorAction SilentlyContinue
foreach ($f in $chartFiles) {
    Log "  $($f.Name): $([math]::Round($f.Length/1KB))KB"
}
Log ""

# ------------------------------------------------------------
# Step 11: Git commit and push
# ------------------------------------------------------------
Log "Step 11: Committing and pushing results..."
try {
    git add experiments/results/ experiments/charts/ experiments/logs/ 2>&1 | ForEach-Object { Log "  $_" }

    $commitMsg = "exp: experiment results $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git commit -m $commitMsg 2>&1 | ForEach-Object { Log "  $_" }

    git push 2>&1 | ForEach-Object { Log "  $_" }
    Log "Push complete."
} catch {
    Log "Git push failed: $_"
}
Log ""

$elapsed = (Get-Date) - $StartTime
Log "=== Pipeline Complete ==="
Log "Total runtime: $($elapsed.Hours)h $($elapsed.Minutes)m $($elapsed.Seconds)s"
Log "Log file: $LogFile"

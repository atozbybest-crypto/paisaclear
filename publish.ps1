# Publish PaisaClear: build, copy into the repo, commit, pull, push.
# Usage:  .\publish.ps1 -Message "What changed"
#
# Merge policy: on conflicts take OUR version (-X ours). The usual conflict is
# in site/*.html, which is generated — the local build is always the newer one.

param(
    [Parameter(Mandatory = $true)][string]$Message,
    [switch]$SkipBuild
)

$ErrorActionPreference = "Stop"

$src = "C:\Users\Gowtham_Sravya\Documents\deepseek-harness\default-workspace\paisaclear"
# Repository location: prefer the copy outside OneDrive (no file locks).
$candidates = @(
    "C:\dev\paisaclear-git\paisaclear",
    (Join-Path ([Environment]::GetFolderPath('MyDocuments')) "paisaclear-git\paisaclear")
)
$dst = $candidates | Where-Object { Test-Path (Join-Path $_ ".git") } | Select-Object -First 1
if (-not $dst) { $dst = $candidates[0] }
$python = "C:\Users\Gowtham_Sravya\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
$git = (Get-ChildItem "$env:LOCALAPPDATA\GitHubDesktop\app-*\resources\app\git\cmd\git.exe" |
        Select-Object -First 1).FullName

if (-not (Test-Path $git)) { throw "Bundled git not found. Is GitHub Desktop installed?" }
if (-not (Test-Path $dst)) { throw "Repository not found at $dst" }

# 0. Never leave a half-finished merge behind.
Push-Location $dst
if (Test-Path ".git\MERGE_HEAD") {
    Write-Host "Aborting an unfinished merge..." -ForegroundColor Yellow
    & $git merge --abort
}
& $git config gc.auto 0 | Out-Null
Pop-Location

# 1. Build
if (-not $SkipBuild) {
    Write-Host "Building..." -ForegroundColor Cyan
    & $python "$src\build.py" | Select-Object -Last 4
    & $python "$src\bundle.py" | Select-Object -Last 2
}

# 2. Copy into the repo
Write-Host "Copying into the repository..." -ForegroundColor Cyan
robocopy $src $dst /E /XD ".tools-office" ".lic-render" ".git" /NFL /NDL /NJH /NJS | Out-Null

# 3. Commit, merge, push
Push-Location $dst
& $git add -A
$staged = (& $git diff --cached --name-only | Measure-Object).Count
if ($staged -gt 0) {
    & $git commit -m $Message | Select-Object -Last 3
} else {
    Write-Host "Nothing new to commit." -ForegroundColor Yellow
}

Write-Host "Pulling latest from GitHub..." -ForegroundColor Cyan
& $git pull --no-rebase -X ours origin main | Select-Object -Last 5

Write-Host "Pushing..." -ForegroundColor Cyan
& $git push
Pop-Location

Write-Host ""
Write-Host "Done. Last three commits:" -ForegroundColor Green
Push-Location $dst
& $git --no-pager log --oneline -3
& $git --no-pager status -sb | Select-Object -First 1
Pop-Location

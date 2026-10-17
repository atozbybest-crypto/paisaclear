# Starts the PaisaClear preview server.
# Right-click > "Run with PowerShell", or:  pwsh -File start.ps1

Set-Location -LiteralPath $PSScriptRoot

$candidates = @()

$py = Get-Command py -ErrorAction SilentlyContinue
if ($py) { $candidates += $py.Source }

$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) { $candidates += $python.Source }

$bundled = Join-Path $env:USERPROFILE ".dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
if (Test-Path -LiteralPath $bundled) { $candidates += $bundled }

$exe = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1

if (-not $exe) {
    Write-Host ""
    Write-Host "  Python was not found on this machine." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  You do not need it: double-click PaisaClear.html instead."
    Write-Host "  That file is the whole site and needs nothing installed."
    Write-Host ""
    Read-Host "Press Enter to close"
    exit 1
}

& $exe serve.py

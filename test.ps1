# Execution policy
Set-ExecutionPolicy RemoteSigned -Scope Process

# Root of project
$root = $PSScriptRoot
Set-Location "$root\backend"

# Activate venv (IMPORTANT: dot sourcing)
. .\..\venv\Scripts\Activate.ps1

# Run tests
python -m pytest

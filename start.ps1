# Setting the root path to the directory of this script
$rootPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Backend
$backendProcess = Start-Process powershell -PassThru -ArgumentList @(
    "-NoExit",
    "-Command",
    @"
`$host.UI.RawUI.WindowTitle = 'Backend'
cd '$rootPath'
. .\venv\Scripts\Activate.ps1
cd backend
python run.py
"@
)

# Save PID
$backendProcess.Id | Out-File "$rootPath\PowerShellPIDs\backend.pid"

# Frontend
$frontendProcess = Start-Process powershell -PassThru -ArgumentList @(
    "-NoExit",
    "-Command",
    @"
`$host.UI.RawUI.WindowTitle = 'Frontend'
cd '$rootPath'
. .\venv\Scripts\Activate.ps1
cd frontend
npm run dev
"@
)

# Save PID
$frontendProcess.Id | Out-File "$rootPath\PowerShellPIDs\frontend.pid"

Write-Host "Backend + Frontend started"

$rootPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Backend stop
if (Test-Path "$rootPath\PowerShellPIDs\backend.pid") {
    $backendPid = Get-Content "$rootPath\PowerShellPIDs\backend.pid"
    taskkill /PID $backendPid /T /F
    Remove-Item "$rootPath\PowerShellPIDs\backend.pid"
    Write-Host "Backend stopped"
}

# Frontend stop
if (Test-Path "$rootPath\PowerShellPIDs\frontend.pid") {
    $frontendPid = Get-Content "$rootPath\PowerShellPIDs\frontend.pid"
    taskkill /PID $frontendPid /T /F
    Remove-Item "$rootPath\PowerShellPIDs\frontend.pid"
    Write-Host "Frontend stopped"
}

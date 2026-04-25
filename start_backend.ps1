$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $repoRoot "backed"
$port = 8000

$listeners = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
foreach ($listener in $listeners) {
    $pidToStop = $listener.OwningProcess
    if ($pidToStop -and $pidToStop -ne $PID) {
        $process = Get-Process -Id $pidToStop -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "Deteniendo proceso en puerto $port (PID $pidToStop: $($process.ProcessName))..."
            Stop-Process -Id $pidToStop -Force
        }
    }
}

Set-Location $backendDir
Write-Host "Iniciando backend en http://127.0.0.1:$port ..."
py -m uvicorn app.main:app --host 127.0.0.1 --port $port

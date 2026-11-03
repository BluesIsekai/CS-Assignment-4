# Run from any directory. Ctrl+C stops both loopback-only servers.
$ErrorActionPreference = 'Stop'
$pythonPath = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'First run: python -m venv .venv ; then .\.venv\Scripts\python.exe -m pip install -r requirements.txt (inside CSRF).'
}
$victim = $null
$attacker = $null
try {
    $victim = Start-Process -FilePath $pythonPath -ArgumentList 'app.py' -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -PassThru
    $attacker = Start-Process -FilePath $pythonPath -ArgumentList 'attacker.py' -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -PassThru
    Write-Host 'Victim: http://127.0.0.1:5000 | Attacker: http://localhost:8001'
    Write-Host 'Keep this terminal open. Press Ctrl+C when finished.'
    while (-not $victim.HasExited -and -not $attacker.HasExited) { Start-Sleep -Seconds 1 }
    throw 'A demo server stopped. Check that ports 5000 and 8001 are free.'
}
finally {
    foreach ($process in @($victim, $attacker)) {
        if ($null -ne $process -and -not $process.HasExited) { Stop-Process -Id $process.Id }
    }
}

param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

if ($Clean) {
    Remove-Item -Recurse -Force "$ProjectRoot\build" -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force "$ProjectRoot\dist" -ErrorAction SilentlyContinue
}

if (!(Test-Path "$ProjectRoot\.venv")) {
    py -3 -m venv "$ProjectRoot\.venv"
}

& "$ProjectRoot\.venv\Scripts\python.exe" -m pip install --upgrade pip
& "$ProjectRoot\.venv\Scripts\python.exe" -m pip install -r "$ProjectRoot\requirements-windows.txt"

$IconArg = @()
if (Test-Path "$ProjectRoot\Flint.ico") {
    $IconArg = @("--icon", "$ProjectRoot\Flint.ico")
}

& "$ProjectRoot\.venv\Scripts\pyinstaller.exe" `
    --noconfirm `
    --windowed `
    --name Flint `
    --onedir `
    @IconArg `
    "$ProjectRoot\lang.py"

Write-Host ""
Write-Host "Built: $ProjectRoot\dist\Flint\Flint.exe"
Write-Host "Next: open installer\flint.iss in Inno Setup and compile."

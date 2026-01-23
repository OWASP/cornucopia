# Install Elixir to D: drive
# This script downloads and extracts Elixir and Erlang to D:\elixir

$InstallDir = "D:\elixir"
$ErlangDir = "$InstallDir\erlang"
$ElixirDir = "$InstallDir\elixir-bin"

Write-Host "Creating installation directory..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
New-Item -ItemType Directory -Force -Path $ErlangDir | Out-Null
New-Item -ItemType Directory -Force -Path $ElixirDir | Out-Null

Write-Host "`nDownloading Erlang OTP 26..." -ForegroundColor Green
$ErlangUrl = "https://github.com/erlang/otp/releases/download/OTP-26.2.5/otp_win64_26.2.5.exe"
$ErlangInstaller = "$env:TEMP\erlang-installer.exe"
Invoke-WebRequest -Uri $ErlangUrl -OutFile $ErlangInstaller

Write-Host "Installing Erlang to D:\elixir\erlang..." -ForegroundColor Green
Start-Process -FilePath $ErlangInstaller -ArgumentList "/S", "/D=$ErlangDir" -Wait

Write-Host "`nDownloading Elixir 1.16..." -ForegroundColor Green
$ElixirUrl = "https://github.com/elixir-lang/elixir/releases/download/v1.16.3/elixir-otp-26.zip"
$ElixirZip = "$env:TEMP\elixir.zip"
Invoke-WebRequest -Uri $ElixirUrl -OutFile $ElixirZip

Write-Host "Extracting Elixir to D:\elixir\elixir-bin..." -ForegroundColor Green
Expand-Archive -Path $ElixirZip -DestinationPath $ElixirDir -Force

Write-Host "`nAdding to PATH for this session..." -ForegroundColor Green
$env:Path = "$ErlangDir\bin;$ElixirDir\bin;$env:Path"

Write-Host "`nVerifying installation..." -ForegroundColor Green
elixir --version

Write-Host "`n===========================================================" -ForegroundColor Cyan
Write-Host "Elixir installed successfully to D:\elixir!" -ForegroundColor Green
Write-Host "`nTo make this permanent, add these to your System PATH:" -ForegroundColor Yellow
Write-Host "  D:\elixir\erlang\bin" -ForegroundColor White
Write-Host "  D:\elixir\elixir-bin\bin" -ForegroundColor White
Write-Host "`nFor now, the PATH is set for this PowerShell session only." -ForegroundColor Yellow
Write-Host "===========================================================" -ForegroundColor Cyan

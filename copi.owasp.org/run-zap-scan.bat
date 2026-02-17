@echo off
REM OWASP ZAP DAST Scan Script for Copi Application (Windows)
REM This script runs a ZAP security scan against the locally running Copi application

setlocal enabledelayedexpansion

REM Configuration
if "%TARGET_URL%"=="" set TARGET_URL=http://localhost:4000/games/new
if "%REPORT_DIR%"=="" set REPORT_DIR=zap-reports
set ZAP_IMAGE=ghcr.io/zaproxy/zaproxy:stable

echo === OWASP ZAP DAST Scanner for Copi ===
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Check if application is running
echo Checking if Copi application is running...
curl -f -s "%TARGET_URL%" >nul 2>&1
if errorlevel 1 (
    echo Error: Copi application is not accessible at %TARGET_URL%
    echo Please start the application first:
    echo   cd copi.owasp.org
    echo   mix phx.server
    exit /b 1
)
echo [OK] Application is running
echo.

REM Create report directory
if not exist "%REPORT_DIR%" mkdir "%REPORT_DIR%"
echo Reports will be saved to: %REPORT_DIR%
echo.

REM Pull latest ZAP image
echo Pulling latest ZAP Docker image...
docker pull %ZAP_IMAGE%
echo.

REM Run ZAP scan
echo Starting ZAP Full Scan...
echo Target: %TARGET_URL%
echo This may take 30-45 minutes...
echo.

docker run --rm --network="host" -v "%CD%\%REPORT_DIR%:/zap/wrk/:rw" -t %ZAP_IMAGE% zap-full-scan.py -t "%TARGET_URL%" -r copi_dast_report.html -w copi_dast_report.md -J copi_dast_report.json -x copi_dast_report.xml -a -j -d -m 10 -T 30

echo.
echo === Scan Complete ===
echo.

REM Check for reports
if exist "%REPORT_DIR%\copi_dast_report.json" (
    echo [OK] Reports generated successfully
    echo.
    echo Available reports:
    dir /B "%REPORT_DIR%"
    echo.
    echo To view the HTML report:
    echo   start %REPORT_DIR%\copi_dast_report.html
    echo.
) else (
    echo [ERROR] Reports not found. Check the scan output for errors.
    exit /b 1
)

endlocal

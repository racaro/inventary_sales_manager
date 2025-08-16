@echo off
echo Checking if Docker Desktop is running...
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker Desktop is not running.
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo Building Stock Manager Docker image...
docker-compose build

if errorlevel 1 (
    echo Error building Docker image.
    pause
    exit /b 1
)

echo Starting Stock Manager container...
docker-compose up -d

if errorlevel 1 (
    echo Error starting container.
    pause
    exit /b 1
)

echo.
echo Stock Manager is starting...
echo You can access the application via VNC at localhost:5901
echo Use any VNC viewer to connect (no password required)
echo.
echo To stop the application, run: docker-compose down
echo To view logs, run: docker-compose logs -f
echo.
pause

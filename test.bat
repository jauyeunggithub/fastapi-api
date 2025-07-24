@echo off
setlocal

echo.
echo === STEP 1: Building Docker containers ===
docker-compose build

echo.
echo === STEP 3: Running tests ===
docker-compose run --rm test

echo.
echo === STEP 4: Cleaning up containers and volumes ===
docker-compose down -v

echo.
echo === All steps completed successfully! ===
endlocal

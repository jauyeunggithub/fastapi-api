@echo off
setlocal

echo.
echo === STEP 1: Building Docker containers ===
docker-compose build

echo.
echo === STEP 2: Running database migrations ===
docker-compose run --rm web python -c "from app.models import Base; from app.database import engine; Base.metadata.create_all(bind=engine)"


echo.
echo === STEP 3: Running tests ===
docker-compose run --rm test

echo.
echo === STEP 4: Cleaning up containers and volumes ===
docker-compose down -v

echo.
echo === All steps completed successfully! ===
endlocal

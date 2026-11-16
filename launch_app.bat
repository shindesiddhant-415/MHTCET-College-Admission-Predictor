@echo off
echo =====================================================================
echo  MHT-CET College Admission Predictor & Recommendation System
echo  React 18 SPA + FastAPI Machine Learning REST Backend
echo =====================================================================
echo.
echo [1/2] Launching browser to http://localhost:8000 ...
start http://localhost:8000
echo.
echo [2/2] Starting FastAPI ASGI server with React SPA on port 8000...
echo (Press Ctrl+C to stop the server)
echo.
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
pause


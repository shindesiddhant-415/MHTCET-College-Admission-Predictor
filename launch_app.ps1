Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host " MHT-CET College Admission Predictor & Recommendation System" -ForegroundColor White
Write-Host " React 18 SPA + FastAPI Machine Learning REST Backend" -ForegroundColor Gray
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[1/2] Opening browser to http://localhost:8000 ..." -ForegroundColor Green
Start-Process "http://localhost:8000"
Write-Host ""
Write-Host "[2/2] Starting FastAPI server on port 8000 (Ctrl+C to stop)..." -ForegroundColor Yellow
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000


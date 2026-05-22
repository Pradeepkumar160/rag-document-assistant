# ============================================================
# RAG Document Assistant — PowerShell Startup Script
# Run this from the rag-document-assistant\ folder
# ============================================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  RAG Document Assistant — Docker Launcher  " -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check Docker is running
Write-Host "[1/4] Checking Docker..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    Write-Host "      Docker is running." -ForegroundColor Green
} catch {
    Write-Host "      ERROR: Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# 2. Stop any old containers cleanly
Write-Host ""
Write-Host "[2/4] Stopping any existing containers..." -ForegroundColor Yellow
docker compose down
Write-Host "      Done." -ForegroundColor Green

# 3. Build and start all services
Write-Host ""
Write-Host "[3/4] Building and starting all services (this may take several minutes on first run)..." -ForegroundColor Yellow
Write-Host "      Pulling Ollama image + llama3 + nomic-embed-text models..." -ForegroundColor Gray
docker compose up --build -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: docker compose up failed. Check the output above." -ForegroundColor Red
    exit 1
}

# 4. Wait for services and show URLs
Write-Host ""
Write-Host "[4/4] Waiting for services to become healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  All services started!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Streamlit UI   -> http://localhost:8501" -ForegroundColor Cyan
Write-Host "  FastAPI Docs   -> http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  Ollama API     -> http://localhost:11434" -ForegroundColor Cyan
Write-Host ""
Write-Host "  NOTE: First startup takes 5-10 minutes to download AI models." -ForegroundColor Yellow
Write-Host "        Watch progress with:  docker compose logs -f ollama-pull" -ForegroundColor Yellow
Write-Host ""
Write-Host "  To stop all services:  docker compose down" -ForegroundColor Gray
Write-Host "  To view logs:          docker compose logs -f" -ForegroundColor Gray
Write-Host ""

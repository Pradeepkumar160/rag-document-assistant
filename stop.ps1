# ============================================================
# RAG Document Assistant — Stop All Services
# ============================================================
Write-Host ""
Write-Host "Stopping all RAG containers..." -ForegroundColor Yellow
docker compose down
Write-Host "All stopped." -ForegroundColor Green
Write-Host ""

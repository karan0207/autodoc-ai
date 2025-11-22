Write-Host "🔍 Backend Diagnostics" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check 1: Backend Health
Write-Host "1. Backend Health Check" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 5
    Write-Host "   ✅ Backend: HEALTHY" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Backend: NOT RESPONDING" -ForegroundColor Red
}
Write-Host ""

# Check 2: Weaviate
Write-Host "2. Weaviate Vector DB" -ForegroundColor Yellow
try {
    $weaviate = Invoke-RestMethod -Uri "http://localhost:8080/v1/meta" -Method Get -TimeoutSec 5
    Write-Host "   ✅ Weaviate: RUNNING (v$($weaviate.version))" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Weaviate: NOT RESPONDING" -ForegroundColor Red
    Write-Host "   → Run: docker-compose up -d" -ForegroundColor Yellow
}
Write-Host ""

# Check 3: Ollama
Write-Host "3. Ollama LLM Service" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 5
    $ollama = $response.Content | ConvertFrom-Json
    Write-Host "   ✅ Ollama: RUNNING" -ForegroundColor Green
    Write-Host "   Models:" -ForegroundColor Gray
    foreach ($model in $ollama.models) {
        Write-Host "   - $($model.name)" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ❌ Ollama: NOT RESPONDING" -ForegroundColor Red
    Write-Host "   → Run: docker-compose up -d" -ForegroundColor Yellow
}
Write-Host ""

# Check 4: Redis
Write-Host "4. Redis Cache" -ForegroundColor Yellow
try {
    $redis = docker exec crawler-redis-1 redis-cli ping 2>&1
    if ($redis -eq "PONG") {
        Write-Host "   ✅ Redis: RUNNING" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Redis: NOT RESPONDING" -ForegroundColor Red
    }
} catch {
    Write-Host "   ❌ Redis: NOT RESPONDING" -ForegroundColor Red
}
Write-Host ""

Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "💡 Recommendations:" -ForegroundColor Cyan
Write-Host ""
Write-Host "If any service is down:" -ForegroundColor Yellow
Write-Host "  1. Make sure Docker is running" -ForegroundColor Gray
Write-Host "  2. Run: docker-compose up -d" -ForegroundColor Gray
Write-Host "  3. Wait 10 seconds for services to start" -ForegroundColor Gray
Write-Host "  4. Restart backend: Ctrl+C and run uvicorn again" -ForegroundColor Gray

# Quick Test Script for AutoDoc AI Backend
# Tests the complete pipeline: ingest → generate

Write-Host "🧪 Testing AutoDoc AI Backend..." -ForegroundColor Cyan
Write-Host ""

# Check if services are running
Write-Host "1️⃣ Checking Docker services..." -ForegroundColor Yellow
docker-compose ps
Write-Host ""

# Wait for services to be ready
Write-Host "2️⃣ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Test 1: Health check
Write-Host "3️⃣ Testing backend health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get
    Write-Host "✅ Backend is running!" -ForegroundColor Green
    Write-Host "Response: $($health | ConvertTo-Json)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Backend not responding at http://localhost:8000/" -ForegroundColor Red
    Write-Host "Make sure backend is running: cd backend && .\venv\Scripts\python.exe -m uvicorn backend.main:app --reload" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Test 2: Ingest a simple webpage
Write-Host "4️⃣ Testing ingestion (crawling a simple page)..." -ForegroundColor Yellow
$ingestBody = @{
    url = "https://example.com"
    source = "web"
} | ConvertTo-Json

try {
    $ingestResponse = Invoke-RestMethod -Uri "http://localhost:8000/ingest" -Method Post -Body $ingestBody -ContentType "application/json"
    Write-Host "✅ Ingestion started!" -ForegroundColor Green
    Write-Host "Job ID: $($ingestResponse.job_id)" -ForegroundColor Cyan
    $jobId = $ingestResponse.job_id
} catch {
    Write-Host "❌ Ingestion failed!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Gray
    exit 1
}
Write-Host ""

# Wait for ingestion to complete
Write-Host "5️⃣ Waiting for ingestion to complete..." -ForegroundColor Yellow
Start-Sleep -Seconds 15
Write-Host ""

# Test 3: Generate documentation
Write-Host "6️⃣ Testing documentation generation..." -ForegroundColor Yellow
$generateBody = @{
    job_id = $jobId
    prompt = "Summarize the content of this website"
    type = "custom"
} | ConvertTo-Json

try {
    $generateResponse = Invoke-RestMethod -Uri "http://localhost:8000/generate" -Method Post -Body $generateBody -ContentType "application/json"
    Write-Host "✅ Documentation generated!" -ForegroundColor Green
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "Generated Content:" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host $generateResponse.content -ForegroundColor White
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Sources used: $($generateResponse.sources.Count)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Generation failed!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Gray
    exit 1
}
Write-Host ""

Write-Host "✅ ALL TESTS PASSED! Your backend is fully functional! 🎉" -ForegroundColor Green
Write-Host ""
Write-Host "Performance Note:" -ForegroundColor Yellow
Write-Host "  - Ingestion time: ~10-15 seconds" -ForegroundColor Gray
Write-Host "  - Generation time: ~10-30 seconds (depends on content)" -ForegroundColor Gray
Write-Host "  - This is normal for CPU-based models on laptops" -ForegroundColor Gray

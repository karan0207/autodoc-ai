Write-Host "🚀 Testing Fast Prototype Pipeline" -ForegroundColor Cyan
Write-Host "════════════════════════════════════" -ForegroundColor Cyan

# 1. Ingest
Write-Host "1. Starting Ingestion..." -ForegroundColor Yellow
$body = @{ 
    url = "https://example.com"
    repo_url = "https://github.com/microsoft/vscode"
} | ConvertTo-Json

try {
    $ingest = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/ingest" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 10
    $job_id = $ingest.job_id
    Write-Host "✅ Ingestion started! Job ID: $job_id" -ForegroundColor Green
} catch {
    Write-Host "❌ Ingestion failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Wait a moment for the "fast" ingestion to finish
Start-Sleep -Seconds 2

# 2. Check Stats
Write-Host "2. Checking Stats..." -ForegroundColor Yellow
try {
    $stats = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/debug/stats?job_id=$job_id" -Method Get
    Write-Host "✅ Found $($stats.total_documents) documents total" -ForegroundColor Green
    if ($stats.samples.Count -gt 0) {
        Write-Host "   Sample: $($stats.samples[0].content_preview)..." -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Stats check failed: $($_.Exception.Message)" -ForegroundColor Red
}

# 3. Generate
Write-Host "3. Generating Documentation..." -ForegroundColor Yellow
$genBody = @{
    job_id = $job_id
    prompt = "What is this project about?"
    type = "product"
} | ConvertTo-Json

try {
    $gen = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/generate" -Method Post -Body $genBody -ContentType "application/json" -TimeoutSec 60
    Write-Host "✅ Generation Successful!" -ForegroundColor Green
    Write-Host "------------------------------------------------" -ForegroundColor Gray
    Write-Host $gen.content -ForegroundColor White
    Write-Host "------------------------------------------------" -ForegroundColor Gray
} catch {
    Write-Host "❌ Generation failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Response: $($_.ErrorDetails.Message)" -ForegroundColor Red
}

Write-Host "🧪 Simple Component Test" -ForegroundColor Cyan
Write-Host ""

# Test just ingestion start (no waiting)
Write-Host "Starting ingestion..." -ForegroundColor Yellow
$body = @{ 
    url = "https://example.com"
    repo_url = "https://github.com/microsoft/vscode"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/ingest" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 10
    Write-Host "✅ Ingestion started" -ForegroundColor Green
    Write-Host "Job ID: $($result.job_id)" -ForegroundColor Cyan
    $jobId = $result.job_id
} catch {
    Write-Host "❌ Failed: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Now check the backend terminal for progress logs..." -ForegroundColor Yellow
Write-Host "Look for:" -ForegroundColor Gray
Write-Host "  - Crawling..." -ForegroundColor Gray  
Write-Host "  - Fetching GitHub..." -ForegroundColor Gray
Write-Host "  - Embedding generation..." -ForegroundColor Gray
Write-Host "  - Storing in vector DB..." -ForegroundColor Gray
Write-Host ""
Write-Host "Job ID for later: $jobId" -ForegroundColor Cyan

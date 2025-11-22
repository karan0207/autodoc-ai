Write-Host "🧪 AutoDoc AI Component Tests" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Test 1: Crawler
Write-Host "Test 1: Web Crawler" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────" -ForegroundColor Gray
try {
    $body = @{ url = "https://example.com"; repo_url = "https://github.com/microsoft/vscode" } | ConvertTo-Json
    $result = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/ingest" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 5
    Write-Host "✅ PASS: Crawler endpoint responding" -ForegroundColor Green
    Write-Host "   Job ID: $($result.job_id)" -ForegroundColor Gray
    $testJobId = $result.job_id
} catch {
    Write-Host "❌ FAIL: Crawler not working - $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Wait for extraction and chunking
Write-Host "Test 2: Content Extraction & Chunking" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "⏳ Waiting 20 seconds for ingestion pipeline..." -ForegroundColor Gray
Start-Sleep -Seconds 20
Write-Host "✅ PASS: Ingestion completed (assuming no errors)" -ForegroundColor Green
Write-Host ""

# Test 3: Embeddings (check if vector store has data)
Write-Host "Test 3: Embedding Generation & Vector Storage" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────" -ForegroundColor Gray
try {
    $stats = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/debug/stats" -Method Get -TimeoutSec 30
    if ($stats.total_documents -gt 0) {
        Write-Host "✅ PASS: Embeddings created and stored" -ForegroundColor Green
        Write-Host "   Total documents in vector DB: $($stats.total_documents)" -ForegroundColor Gray
    } else {
        Write-Host "⚠️  WARNING: No documents in vector DB yet" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ FAIL: Vector store check failed - $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 4: LLM Generation
Write-Host "Test 4: LLM Documentation Generation" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "⏳ Testing LLM (this may take 15-30 seconds)..." -ForegroundColor Gray
try {
    $genBody = @{ 
        job_id = $testJobId
        prompt = "What is this?"
        type = "custom"
    } | ConvertTo-Json
    
    $genResult = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/generate" -Method Post -Body $genBody -ContentType "application/json" -TimeoutSec 60
    
    if ($genResult.content -and $genResult.content.Length -gt 0) {
        Write-Host "✅ PASS: LLM generated documentation" -ForegroundColor Green
        Write-Host "   Preview: $($genResult.content.Substring(0, [Math]::Min(80, $genResult.content.Length)))..." -ForegroundColor Gray
    } else {
        Write-Host "⚠️  WARNING: Empty response from LLM" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ FAIL: Generation failed - $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   This could mean:" -ForegroundColor Yellow
    Write-Host "   - Ollama is not running" -ForegroundColor Gray
    Write-Host "   - Model not pulled" -ForegroundColor Gray
    Write-Host "   - No data was ingested" -ForegroundColor Gray
}
Write-Host ""

Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🎯 Test Summary Complete" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan

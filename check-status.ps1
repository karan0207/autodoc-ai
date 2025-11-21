#!/usr/bin/env pwsh
# Quick Status Checker for AutoDoc AI

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   AutoDoc AI - System Status Check" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Docker containers
Write-Host "🐳 Docker Containers:" -ForegroundColor Yellow
docker ps --format "table {{.Names}}\t{{.Status}}" | Out-String

# Check Ollama models
Write-Host "`n🤖 Ollama Models:" -ForegroundColor Yellow
docker exec crawler-ollama-1 ollama list

# Check Vector Database
Write-Host "`n📊 Vector Database Stats:" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/debug/stats" -Method Get
    Write-Host "Total Documents: $($response.total_documents)" -ForegroundColor $(if ($response.total_documents -gt 0) { "Green" } else { "Red" })
    Write-Host "Sample Count: $($response.samples.Count)"
} catch {
    Write-Host "❌ Cannot reach backend server" -ForegroundColor Red
}

# Check Services
Write-Host "`n🌐 Service Endpoints:" -ForegroundColor Yellow

$services = @(
    @{Name="Backend (Health)"; Url="http://localhost:8000/health"},
    @{Name="Weaviate"; Url="http://localhost:8080/v1/meta"},
    @{Name="Ollama"; Url="http://localhost:11434/api/tags"},
    @{Name="Frontend"; Url="http://localhost:3000"}
)

foreach ($service in $services) {
    try {
        $null = Invoke-WebRequest -Uri $service.Url -TimeoutSec 2 -UseBasicParsing
        Write-Host "  ✅ $($service.Name)" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ $($service.Name)" -ForegroundColor Red
    }
}

Write-Host "`n========================================`n" -ForegroundColor Cyan
Write-Host "💡 Quick Actions:" -ForegroundColor Yellow
Write-Host "  • Check full diagnostics: type 'Get-Content DIAGNOSTIC_SUMMARY.md'"
Write-Host "  • Monitor model download: docker logs crawler-ollama-1 --tail 10"
Write-Host "  • Open frontend: start http://localhost:3000"
Write-Host "  • Check debug endpoint: start http://localhost:8000/api/v1/debug/stats"
Write-Host ""

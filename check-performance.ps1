#!/usr/bin/env pwsh
# Performance Optimization Script for AutoDoc AI
# Analyzes system and recommends optimal settings

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  AutoDoc AI - Performance Analyzer" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Get system info
$totalRAM = (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB
$freeRAM = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB
$cpu = Get-CimInstance Win32_Processor
$cores = $cpu.NumberOfCores
$threads = $cpu.NumberOfLogicalProcessors

Write-Host "📊 System Analysis:" -ForegroundColor Yellow
Write-Host "  CPU: $($cpu.Name)"
Write-Host "  Cores/Threads: $cores cores / $threads threads"
Write-Host "  Total RAM: $([math]::Round($totalRAM, 1)) GB"
Write-Host "  Free RAM: $([math]::Round($freeRAM/1024, 1)) GB"

# Check Docker
Write-Host "`n🐳 Docker Status:" -ForegroundColor Yellow
try {
    $dockerStats = docker stats --no-stream --format "{{.Name}}: {{.MemUsage}}" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Docker is running" -ForegroundColor Green
        foreach ($stat in $dockerStats) {
            Write-Host "  $stat"
        }
    } else {
        Write-Host "  ❌ Docker is not running" -ForegroundColor Red
    }
} catch {
    Write-Host "  ❌ Cannot access Docker" -ForegroundColor Red
}

# Recommendations
Write-Host "`n💡 Recommended Settings:" -ForegroundColor Yellow

if ($totalRAM -ge 15) {
    Write-Host "  Profile: BALANCED (Your system is good!)" -ForegroundColor Green
    Write-Host "    • max_pages: 50"
    Write-Host "    • batch_size: 50"
    Write-Host "    • model: llama3.2 (standard)"
    Write-Host "    • Expected time: 2-5 minutes per ingestion"
} elseif ($totalRAM -ge 12) {
    Write-Host "  Profile: LIGHT" -ForegroundColor Yellow
    Write-Host "    • max_pages: 30"
    Write-Host "    • batch_size: 30"
    Write-Host "    • model: llama3.2:1b (faster)"
    Write-Host "    • Expected time: 1-3 minutes per ingestion"
} else {
    Write-Host "  Profile: MINIMAL" -ForegroundColor Red
    Write-Host "    • max_pages: 15"
    Write-Host "    • batch_size: 20"
    Write-Host "    • model: llama3.2:1b (faster)"
    Write-Host "    • Expected time: 1-2 minutes per ingestion"
    Write-Host "    ⚠️  Consider closing other applications"
}

# Current usage
Write-Host "`n📈 Current Resource Usage:" -ForegroundColor Yellow
$usedRAM = $totalRAM - ($freeRAM/1024)
$ramPercent = [math]::Round(($usedRAM / $totalRAM) * 100, 1)

if ($ramPercent -gt 80) {
    Write-Host "  ⚠️  RAM Usage: $ramPercent% (HIGH - close some apps)" -ForegroundColor Red
} elseif ($ramPercent -gt 60) {
    Write-Host "  ⚠️  RAM Usage: $ramPercent% (MODERATE)" -ForegroundColor Yellow
} else {
    Write-Host "  ✅ RAM Usage: $ramPercent% (GOOD)" -ForegroundColor Green
}

# Disk space
Write-Host "`n💾 Disk Space:" -ForegroundColor Yellow
$disk = Get-PSDrive C
$freeSpace = [math]::Round($disk.Free / 1GB, 1)
if ($freeSpace -lt 5) {
    Write-Host "  ⚠️  Free Space: $freeSpace GB (LOW - need 5+ GB)" -ForegroundColor Red
} elseif ($freeSpace -lt 10) {
    Write-Host "  ⚠️  Free Space: $freeSpace GB (MODERATE)" -ForegroundColor Yellow
} else {
    Write-Host "  ✅ Free Space: $freeSpace GB (GOOD)" -ForegroundColor Green
}

# Action items
Write-Host "`n✅ Pre-flight Checklist:" -ForegroundColor Yellow

# Check if Docker containers are running
$dockerRunning = $false
try {
    $containers = docker ps --format "{{.Names}}" 2>$null
    if ($containers -match "crawler-ollama" -and $containers -match "crawler-weaviate") {
        Write-Host "  ✅ All Docker containers running" -ForegroundColor Green
        $dockerRunning = $true
    } else {
        Write-Host "  ❌ Some Docker containers missing" -ForegroundColor Red
        Write-Host "     Run: docker-compose up -d"
    }
} catch {
    Write-Host "  ❌ Cannot check Docker containers" -ForegroundColor Red
}

# Check Ollama models
if ($dockerRunning) {
    try {
        $models = docker exec crawler-ollama-1 ollama list 2>$null
        if ($models -match "llama") {
            Write-Host "  ✅ Ollama models installed" -ForegroundColor Green
        } else {
            Write-Host "  ❌ No Ollama models found" -ForegroundColor Red
            Write-Host "     Run: docker exec crawler-ollama-1 ollama pull llama3.2"
        }
    } catch {
        Write-Host "  ⚠️  Cannot check Ollama models" -ForegroundColor Yellow
    }
}

# Check backend
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($response.status -eq "ok") {
        Write-Host "  ✅ Backend server running" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Backend server not responding" -ForegroundColor Red
    }
} catch {
    Write-Host "  ❌ Backend server not accessible" -ForegroundColor Red
}

# Check frontend
try {
    $null = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
    Write-Host "  ✅ Frontend server running" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Frontend server not accessible" -ForegroundColor Red
    Write-Host "     Run: cd frontend && npm run dev"
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "💡 Quick Actions:" -ForegroundColor Yellow
Write-Host "  • Full report: Get-Content SYSTEM_REQUIREMENTS.md"
Write-Host "  • Monitor resources: docker stats"
Write-Host "  • Check system: .\check-status.ps1"
Write-Host "  • Test ingestion: Open http://localhost:3000"
Write-Host "`n"

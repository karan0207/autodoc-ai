# 💻 System Requirements & Performance Guide

## ✅ Your Current System

**Detected Configuration:**
- **CPU:** AMD Ryzen 5 5500U (6 cores, 12 threads) ✅ GOOD
- **RAM:** 15.7 GB (~16GB) ✅ GOOD
- **OS:** Windows 11 ✅ SUPPORTED
- **Docker:** Running ✅ WORKING

**Verdict:** ✅ **Your laptop CAN run this project comfortably!**

---

## 📊 Current Resource Usage

### Docker Containers (Real-time)
| Container | CPU Usage | Memory Usage | Limit |
|-----------|-----------|--------------|-------|
| Ollama | 0.00% | 109.5 MB | 7.4 GB |
| Weaviate | 0.83% | 55.6 MB | 7.4 GB |
| Redis | 0.52% | 9.6 MB | 7.4 GB |

**Total Docker Memory:** ~175 MB (idle state)
**During Ingestion:** Can spike to 1-2 GB

---

## 🎯 Minimum vs Recommended Requirements

### Minimum Requirements (Will Work, Slower)
- **CPU:** 4 cores / 8 threads
- **RAM:** 8 GB
- **Disk Space:** 10 GB free
- **Internet:** Stable connection for model downloads
- **Docker:** Docker Desktop or Docker Engine

### Recommended (Your System)
- **CPU:** 6+ cores / 12+ threads ✅
- **RAM:** 16 GB ✅
- **Disk Space:** 20 GB free
- **GPU:** Optional (not required, CPU works fine)
- **SSD:** Recommended for faster I/O

### Ideal (Production/Heavy Use)
- **CPU:** 8+ cores / 16+ threads
- **RAM:** 32 GB
- **Disk Space:** 50 GB SSD
- **GPU:** 8GB+ VRAM (for faster LLM inference)

---

## ⏱️ Expected Time Estimates

### First-Time Setup
| Task | Time | Notes |
|------|------|-------|
| **Clone & Install Dependencies** | 5-10 mins | One-time |
| **Docker Images Download** | 5-10 mins | ~2-3 GB total |
| **Ollama Model (llama3.2)** | 5-10 mins | ~2 GB |
| **Sentence-Transformers Model** | 2-3 mins | ~90 MB |
| **Total First Setup** | **15-30 mins** | One-time cost |

### Regular Operations (On Your System)
| Operation | Time | Resource Impact |
|-----------|------|-----------------|
| **Start All Services** | 10-30 sec | Low |
| **Website Crawl (small site)** | 30-90 sec | Medium |
| **Website Crawl (large site)** | 2-5 mins | High |
| **GitHub Data Fetch** | 10-20 sec | Low |
| **Embedding Generation (100 chunks)** | 5-15 sec | Medium-High |
| **Vector Storage** | 1-3 sec | Low |
| **Documentation Generation** | 10-30 sec | High (LLM) |
| **Complete Ingestion (FastAPI docs)** | **1-3 mins** | High |

### Resource-Intensive Phases
- **Crawling:** CPU-intensive (Playwright browser automation)
- **Embedding:** CPU/RAM-intensive (tensor operations)
- **LLM Generation:** CPU-intensive (model inference)

---

## 🚀 Performance Optimization Tips

### 1. Reduce Memory Usage

**Limit Docker Memory:**
```yaml
# In docker-compose.yml, add to each service:
services:
  ollama:
    mem_limit: 2g
    mem_reservation: 1g
  weaviate:
    mem_limit: 1g
  redis:
    mem_limit: 512m
```

### 2. Speed Up Ingestion

**Reduce Crawler Pages:**
```python
# In backend/crawler/crawler.py
self.max_pages = 10  # Instead of 50
```

**Smaller Batch Sizes:**
```python
# In backend/routes/ingest.py, line 92
batch_size = 20  # Instead of 50
```

### 3. Use Smaller LLM Model

**Switch to smaller model:**
```python
# In backend/rag/generator.py
self.model = "llama3.2:1b"  # 1B params instead of 3B
```

Download it:
```bash
docker exec crawler-ollama-1 ollama pull llama3.2:1b
```

### 4. Limit Concurrent Operations

**Process sequentially instead of parallel:**
- Crawl → Embed → Store (one at a time)
- Reduces peak memory usage

---

## 🔧 Monitoring Your System

### Check Resource Usage (Live)

**Monitor Docker:**
```bash
# Live stats
docker stats

# Detailed info
docker ps -a
```

**Monitor System:**
```powershell
# CPU & Memory
Get-Counter '\Processor(_Total)\% Processor Time'
Get-Counter '\Memory\Available MBytes'

# Or use Task Manager (Ctrl+Shift+Esc)
```

### Warning Signs

**System Under Stress:**
- ⚠️ RAM usage > 90%
- ⚠️ Constant 100% CPU
- ⚠️ Disk thrashing (constant disk activity)
- ⚠️ System becomes unresponsive

**If This Happens:**
1. Reduce `max_pages` in crawler
2. Use smaller batch sizes
3. Close other applications
4. Consider smaller LLM model

---

## 🎮 Recommended Settings for Your Laptop

Based on your **Ryzen 5 5500U + 16GB RAM**:

### Optimal Configuration

**Crawler:**
```python
max_pages = 20  # Balances speed & resources
```

**Embedding Batch:**
```python
batch_size = 30  # Good for 16GB RAM
```

**LLM Model:**
```python
model = "llama3.2"  # 3B params - works well
# OR for faster: "llama3.2:1b"
```

**Docker Memory Limits:**
```yaml
ollama: 4g max      # For model + inference
weaviate: 2g max    # For vector storage
redis: 512m max     # For queue management
```

---

## 📈 Scalability Guide

### Small Projects (1-10 pages)
- **Time:** 1-2 minutes
- **Memory:** < 1 GB
- **Your System:** ✅ Excellent

### Medium Projects (10-50 pages)
- **Time:** 2-5 minutes
- **Memory:** 1-2 GB
- **Your System:** ✅ Very Good

### Large Projects (50-200 pages)
- **Time:** 5-15 minutes
- **Memory:** 2-4 GB
- **Your System:** ✅ Good (may need optimization)

### Very Large Projects (200+ pages)
- **Time:** 15-60 minutes
- **Memory:** 4-8 GB
- **Your System:** ⚠️ Possible, but:
  - Use smaller batches
  - Process in chunks
  - Consider reducing max_pages
  - Monitor memory closely

---

## ⚡ Quick Performance Test

Run this to test your system:

```bash
# 1. Check Docker resources
docker stats --no-stream

# 2. Run quick health check
.\check-status.ps1

# 3. Test small ingestion
# Use frontend with:
# - Website: https://www.example.com (small, fast)
# - GitHub: https://github.com/tiangolo/fastapi
# Expected time: < 1 minute
```

---

## 🛡️ Ensuring Smooth Operation

### Pre-flight Checklist

Before running ingestion:

- [ ] **Check available RAM:** Should have 4-6 GB free
- [ ] **Check disk space:** Should have 5+ GB free
- [ ] **Close heavy apps:** Chrome with many tabs, IDEs, games
- [ ] **Docker is running:** `docker ps` shows 3 containers
- [ ] **Models are ready:** `docker exec crawler-ollama-1 ollama list`
- [ ] **Backend is healthy:** http://localhost:8000/health

### During Operation

Monitor these:
- **Task Manager** - RAM and CPU usage
- **Backend terminal** - Look for errors
- **Docker stats** - Container resource usage

### If System Slows Down

**Immediate Actions:**
1. Wait for current operation to complete
2. Check if disk is full: `Get-PSDrive C`
3. Restart Docker if needed: `docker-compose restart`
4. Close other applications

**Long-term Fixes:**
1. Apply optimization tips above
2. Consider using smaller LLM model
3. Reduce max_pages for crawling
4. Process sites in smaller batches

---

## 🎯 Recommended Workflow for Your System

### Option 1: Fast & Light (Recommended)
```python
# Settings
max_pages = 15
batch_size = 25
model = "llama3.2:1b"  # Faster model

# Expected Performance:
# - Ingestion: 1-2 minutes
# - Generation: 5-10 seconds
# - Memory: < 2 GB peak
```

### Option 2: Balanced (Current)
```python
# Settings
max_pages = 50
batch_size = 50
model = "llama3.2"  # Standard model

# Expected Performance:
# - Ingestion: 2-5 minutes
# - Generation: 10-20 seconds
# - Memory: 2-3 GB peak
```

### Option 3: Maximum Quality (Use Sparingly)
```python
# Settings
max_pages = 100
batch_size = 50
model = "llama3.2"

# Expected Performance:
# - Ingestion: 5-15 minutes
# - Generation: 15-30 seconds
# - Memory: 3-5 GB peak
# ⚠️ Monitor system closely
```

---

## 💡 Pro Tips

1. **Run overnight for large sites** - Let it work while you sleep
2. **Test with small sites first** - Verify everything works
3. **Monitor first run** - Watch resource usage patterns
4. **Keep Docker Desktop updated** - Better performance
5. **Use SSD if available** - Significantly faster I/O
6. **Close browser tabs** - Chrome can use 2-4 GB easily

---

## ❓ FAQ

**Q: Can I run this on 8GB RAM?**
A: Yes, but use smaller batches and reduce max_pages to 10-15.

**Q: Do I need a GPU?**
A: No, CPU inference works fine for this project.

**Q: Why is it slow?**
A: Check Docker memory limits, reduce batch sizes, use smaller model.

**Q: How to make it faster?**
A: Use llama3.2:1b model, reduce max_pages, increase batch sizes if you have RAM.

**Q: Will it damage my laptop?**
A: No, CPU usage is normal. System will throttle if needed.

---

## 📋 Summary

**Your System:** AMD Ryzen 5 5500U + 16GB RAM

✅ **CAN run this project comfortably**
✅ **Expected time:** 1-5 minutes per ingestion
✅ **Optimization:** Minor tweaks recommended
✅ **Long-term:** Suitable for development and testing

**Next Steps:**
1. Review optimization tips if needed
2. Run a small test ingestion
3. Monitor resource usage
4. Adjust settings based on your needs

---

**Last Updated:** 2025-11-21
**System Analyzed:** AMD Ryzen 5 5500U, 16GB RAM, Windows 11

# AutoDoc AI - Local Setup Guide

This guide will help you set up AutoDoc AI with **local models** (no API keys required).

## Quick Start

### 1. Start Infrastructure
```bash
docker-compose up -d
```

This will start:
- **Weaviate** (Vector Database) on port 8080
- **Redis** (Task Queue) on port 6379
- **Ollama** (Local LLM) on port 11434

### 2. Pull Ollama Model
The system uses `llama3.2` by default. Pull it:
```bash
docker exec -it crawler-ollama-1 ollama pull llama3.2
```

You can also use other models by changing the `model` variable in `backend/rag/generator.py`.

### 3. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

This includes:
- `sentence-transformers` for local embeddings
- `torch` for model inference

### 4. Start Backend
```bash
cd ..
.\start_backend.bat
```

### 5. Start Frontend
```bash
.\start_frontend.bat
```

### 6. Use the App
Open [http://localhost:3000](http://localhost:3000)

## How It Works

### Embeddings
- Uses **sentence-transformers** with `all-MiniLM-L6-v2` model
- Runs locally, no API calls
- 384-dimensional embeddings

### Text Generation
- Uses **Ollama** with `llama3.2` (or any model you pull)
- Completely local
- No rate limits or API costs

## Troubleshooting

### Ollama Model Not Found
If you get an error about the model not being pulled:
```bash
docker exec -it crawler-ollama-1 ollama pull llama3.2
```

### Slow Generation
Local models are slower than cloud APIs. For better performance:
- Use a GPU-enabled Ollama setup
- Use smaller models like `llama3.2:1b`
- Reduce context size

### Memory Issues
Sentence-transformers and PyTorch can use significant memory. Close other applications if needed.

## Alternative Models

You can use different Ollama models by editing `backend/rag/generator.py`:
```python
self.model = "mistral"  # or "codellama", "phi3", etc.
```

Then pull the model:
```bash
docker exec -it crawler-ollama-1 ollama pull mistral
```

# Cloud Migration Setup Guide

## Prerequisites

You need to sign up for free accounts and obtain API keys for:

### 1. **Supabase** (PostgreSQL + pgvector)
- Sign up at: https://supabase.com
- Create a new project
- Go to Project Settings → API → copy:
  - `SUPABASE_URL` (Project URL)
  - `SUPABASE_SERVICE_KEY` (Service Role key - not the anon key!)
- Run the SQL migration:
  1. Go to SQL Editor in Supabase dashboard
  2. Copy contents of `backend/migrations/001_initial_schema.sql`
  3. Paste and run

### 2. **Jina AI** (Web Scraping + Embeddings)
- Sign up at: https://jina.ai
- Get API key from: https://jina.ai/api
- Copy your `JINA_API_KEY`

### 3. **Groq** (Fast LLM Inference)
- Sign up at: https://groq.com
- Get API key from: https://console.groq.com/keys
- Copy your `GROQ_API_KEY`

### 4. **GitHub** (Optional, for repo fetching)
- Get a personal access token: https://github.com/settings/tokens
- Copy your `GITHUB_TOKEN`

## Installation Steps

### 1. Update Environment Variables

Create or update `backend/.env`:

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key-here

# Jina AI
JINA_API_KEY=jina_your-api-key-here

# Groq
GROQ_API_KEY=gsk_your-api-key-here

# GitHub (optional)
GITHUB_TOKEN=ghp_your-token-here
```

### 2. Install New Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `supabase` - Supabase Python client
- `groq` - Groq API client
- `httpx` - Modern HTTP client

### 3. Run Database Migration

1. Open Supabase dashboard → SQL Editor
2. Copy the SQL from `backend/migrations/001_initial_schema.sql`
3. Run the migration (creates tables, indexes, and search function)

### 4. Test the Setup

```bash
# Start backend
cd backend
python -m uvicorn backend.main:app --reload

# In another terminal, test health
curl http://localhost:8000/health
```

### 5. Start Frontend

```bash
cd frontend
npm run dev
```

Visit http://localhost:3000 and test the full flow!

## What Changed?

### Removed Dependencies
- ❌ Playwright (slow browser automation)
- ❌ sentence-transformers (large local model)
- ❌ torch (heavy ML framework)
- ❌ weaviate-client (replaced by Supabase)
- ❌ redis (not needed)

### Added Dependencies
- ✅ supabase (efficient vector DB)
- ✅ groq (ultra-fast LLM API)
- ✅ httpx (modern HTTP client)

### Performance Improvements
- **Scraping**: Instant (Jina API) vs 5-30s (Playwright)
- **Embeddings**: <1s vs 10s+ (local model)
- **Generation**: <5s vs 30s+ (Groq vs local)
- **Storage**: Persistent (Supabase) vs in-memory

## Troubleshooting

### "SUPABASE_URL not set"
- Check `.env` file exists in `backend/` directory
- Verify variable names match exactly

### "Table 'chunks' does not exist"
- Run the SQL migration in Supabase dashboard
- Check the SQL Editor for errors

### "Jina API authentication failed"
- Verify your JINA_API_KEY is correct
- Check you have quota remaining at https://jina.ai/api

### "Groq API error"
- Verify your GROQ_API_KEY is correct
- Check rate limits at https://console.groq.com/

## Next Steps

Test the full workflow:
1. Go to **Ingest Sources**
2. Enter a website URL (e.g., https://fastapi.tiangolo.com)
3. Enter a GitHub repo (e.g., https://github.com/tiangolo/fastapi)
4. Click **Start Ingestion**
5. Wait for success (should complete in seconds!)
6. Go to **Dashboard**
7. Click **API Reference** or any generation button
8. View generated docs in **Library**

Enjoy your blazing-fast documentation generator! 🚀

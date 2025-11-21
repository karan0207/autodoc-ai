# Troubleshooting: "No relevant context found to generate documentation"

## Problem
When testing the app, you're seeing the error message: **"No relevant context found to generate documentation"** on the frontend.

## Root Cause
This error occurs when the RAG (Retrieval-Augmented Generation) system cannot find any relevant chunks in the vector database for the given `job_id`. This means the retriever is returning an empty context list.

## Diagnosis Steps

### Step 1: Check if data is in the vector database

Open your browser and go to:
```
http://localhost:8000/api/v1/debug/stats
```

This will show you:
- Total number of documents stored
- Sample documents (first 5)

If you have a specific job_id, check:
```
http://localhost:8000/api/v1/debug/stats?job_id=YOUR_JOB_ID
```

**Expected Result:** You should see documents with your job_id
**If no documents:** The ingestion process either failed or didn't complete

### Step 2: Check backend logs

Look at your backend terminal for logs. You should see:
```
INFO:     Starting ingestion for job <job_id>
INFO:     Crawling <url>...
INFO:     Crawled <N> pages
INFO:     Fetching from <repo_url>...
INFO:     Job <job_id> completed. Stored <N> chunks.
```

**If you see "No pages were crawled":** 
- The website might be blocking the crawler
- The URL might be incorrect
- Check if the website is accessible

### Step 3: Check Weaviate

Verify Weaviate is running:
```bash
docker ps
```

You should see a Weaviate container running on port 8080.

Check Weaviate directly:
```
http://localhost:8080/v1/meta
```

### Step 4: Test the retrieval process

Watch the backend logs when you click a "Generate" button. You should see:
```
INFO:     Retrieving context for job <job_id> with prompt: <your prompt>
INFO:     Creating embedding for query: <query>...
INFO:     Searching vector store with job_id=<job_id>, limit=5
INFO:     Found <N> results from vector store
INFO:     Retrieved <N> context chunks for job <job_id>
```

**If "Found 0 results":**
- The job_id might not match
- No documents were stored for this job
- The query embedding might not match any stored embeddings

## Common Issues and Solutions

### Issue 1: Ingestion hasn't completed
**Symptom:** You click generate immediately after starting ingestion
**Solution:** Wait 30-60 seconds for ingestion to complete. Check backend logs for "Job completed" message.

### Issue 2: Crawler got no data
**Symptom:** Logs show "Crawled 0 pages" or "No pages were crawled"
**Solution:** 
- Try a different website URL (e.g., `https://docs.python.org/3/`)
- Check if the site requires authentication
- Verify the URL is accessible

### Issue 3: Job ID mismatch
**Symptom:** Debug endpoint shows documents, but retrieval finds nothing
**Solution:**
- Copy the exact job_id from the ingestion response
- Make sure you're using the same job_id for generation

### Issue 4: Ollama/Embeddings not working
**Symptom:** Error during ingestion phase
**Solution:**
```bash
# Check Ollama is running
docker exec -it crawler-ollama-1 ollama list

# Pull required model
docker exec -it crawler-ollama-1 ollama pull nomic-embed-text
```

### Issue 5: Weaviate connection issues
**Symptom:** Errors about Weaviate connection in logs
**Solution:**
```bash
# Restart Weaviate
docker-compose restart weaviate

# Check logs
docker-compose logs weaviate
```

## Quick Test

To quickly test if everything is working:

1. **Start fresh ingestion** with a known-good URL:
   - Website URL: `https://fastapi.tiangolo.com/`
   - GitHub URL: `https://github.com/tiangolo/fastapi`

2. **Wait for completion** (watch backend logs)

3. **Check debug endpoint**:
   ```
   http://localhost:8000/api/v1/debug/stats
   ```

4. **Generate documentation** with the job_id from step 1

## Debugging Checklist

- [ ] Backend server is running (port 8000)
- [ ] Frontend is running (port 3000)
- [ ] Weaviate is running (port 8080)
- [ ] Ollama is running (port 11434)
- [ ] Model `nomic-embed-text` is pulled in Ollama
- [ ] Ingestion completed successfully (check logs)
- [ ] Debug endpoint shows documents for your job_id
- [ ] You're using the correct job_id from ingestion response

## Enhanced Error Messages

The code has been updated with better logging to help diagnose issues:
- Shows number of context chunks retrieved
- Logs search parameters (job_id, limit)
- Warns when no context is found
- Debug endpoint to inspect database contents

## Next Steps

1. Check the debug endpoint first: `http://localhost:8000/api/v1/debug/stats`
2. Review the backend logs for any errors
3. Try a test ingestion with the URLs above
4. Share the backend logs if issues persist

-- AutoDoc AI Database Schema
-- Run this in Supabase SQL Editor

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Chunks table for storing document embeddings
CREATE TABLE IF NOT EXISTS chunks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id TEXT NOT NULL,
  content TEXT NOT NULL,
  metadata JSONB DEFAULT '{}'::jsonb,
  embedding vector(768), -- Jina embeddings are 768-dimensional
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for vector similarity search (cosine distance)
CREATE INDEX IF NOT EXISTS chunks_embedding_idx 
ON chunks 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Index for job_id lookups
CREATE INDEX IF NOT EXISTS chunks_job_id_idx 
ON chunks (job_id);

-- Jobs table for tracking ingestion status
CREATE TABLE IF NOT EXISTS jobs (
  job_id TEXT PRIMARY KEY,
  status TEXT NOT NULL DEFAULT 'processing',
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

-- Index for status filtering
CREATE INDEX IF NOT EXISTS jobs_status_idx 
ON jobs (status);

-- Function to search similar chunks
CREATE OR REPLACE FUNCTION match_chunks(
  query_embedding vector(768),
  match_count int DEFAULT 5,
  filter_job_id text DEFAULT NULL
)
RETURNS TABLE (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    chunks.id,
    chunks.content,
    chunks.metadata,
    1 - (chunks.embedding <=> query_embedding) AS similarity
  FROM chunks
  WHERE filter_job_id IS NULL OR chunks.job_id = filter_job_id
  ORDER BY chunks.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- Grant permissions (adjust for your setup)
-- GRANT ALL ON chunks TO authenticated;
-- GRANT ALL ON jobs TO authenticated;

-- Migration: Update vector dimensions from 768 to 384 for HuggingFace

-- Drop the old function first
DROP FUNCTION IF EXISTS match_chunks;

-- Drop the old embedding column
ALTER TABLE chunks DROP COLUMN IF EXISTS embedding;

-- Add new embedding column with 384 dimensions
ALTER TABLE chunks ADD COLUMN embedding vector(384);

-- Recreate the index for 384-dimensional vectors
DROP INDEX IF EXISTS chunks_embedding_idx;
CREATE INDEX chunks_embedding_idx 
ON chunks 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Recreate the search function for 384 dimensions
CREATE OR REPLACE FUNCTION match_chunks(
  query_embedding vector(384),
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

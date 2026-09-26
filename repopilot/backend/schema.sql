-- Enable pgvector (Run this manually in Supabase SQL Editor if not done yet)
-- CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    role TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS repositories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    url TEXT NOT NULL,
    default_branch TEXT,
    analyzed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS onboarding_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repo_id UUID REFERENCES repositories(id),
    role TEXT NOT NULL,
    plan_json JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS code_chunks (
    id BIGSERIAL PRIMARY KEY,
    repo_id UUID REFERENCES repositories(id),
    path TEXT NOT NULL,
    start_line INT NOT NULL,
    end_line INT NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536)
);

CREATE INDEX IF NOT EXISTS code_chunks_embedding_idx 
ON code_chunks USING ivfflat (embedding vector_cosine_ops);
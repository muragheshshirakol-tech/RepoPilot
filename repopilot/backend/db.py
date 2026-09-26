import os
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import json

# Initialize connection pool
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# Min 1, Max 10 connections in the pool
db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL)

def get_db_connection():
    """Get a connection from the pool."""
    try:
        return db_pool.getconn()
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise

def release_db_connection(conn):
    """Return a connection to the pool."""
    if conn:
        db_pool.putconn(conn)

class DatabaseContextManager:
    """Context manager for safe database operations."""
    def __enter__(self):
        self.conn = get_db_connection()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        release_db_connection(self.conn)

def init_db():
    """Initialize the database by running schema.sql."""
    try:
        with DatabaseContextManager() as conn:
            with open("schema.sql", "r") as f:
                schema_sql = f.read()
            with conn.cursor() as cur:
                cur.execute(schema_sql)
            print("Database initialized successfully.")
    except FileNotFoundError:
        print("Warning: schema.sql not found. Skipping init_db.")
    except psycopg2.Error as e:
        print(f"Failed to initialize database: {e}")
        raise

def create_repo(url: str, job_id: str) -> str:
    """Create a new repository record."""
    with DatabaseContextManager() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO repositories (id, url) VALUES (%s, %s) RETURNING id",
                (job_id, url)
            )
            result = cur.fetchone()
            return result["id"]

def get_repo(repo_id: str) -> dict:
    """Get repository details by ID."""
    with DatabaseContextManager() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM repositories WHERE id = %s", (repo_id,))
            return cur.fetchone()

def save_plan(repo_id: str, role: str, plan_dict: dict) -> None:
    """Save the generated onboarding plan."""
    with DatabaseContextManager() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO onboarding_plans (repo_id, role, plan_json) 
                   VALUES (%s, %s, %s) 
                   ON CONFLICT (repo_id) DO UPDATE SET plan_json = EXCLUDED.plan_json""",
                (repo_id, role, json.dumps(plan_dict))
            )

def get_plan(repo_id: str) -> dict:
    """Get the onboarding plan for a repository."""
    with DatabaseContextManager() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT plan_json FROM onboarding_plans WHERE repo_id = %s", (repo_id,))
            result = cur.fetchone()
            return result["plan_json"] if result else None

def save_chunk(repo_id: str, path: str, start: int, end: int, content: str, embedding: list) -> None:
    """Save a code chunk with its vector embedding."""
    with DatabaseContextManager() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO code_chunks (repo_id, path, start_line, end_line, content, embedding) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (repo_id, path, start, end, content, embedding)
            )

def search_chunks(repo_id: str, query_embedding: list, top_k: int = 10) -> list:
    """Search for similar code chunks using pgvector cosine distance."""
    with DatabaseContextManager() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """SELECT path, start_line, end_line, content 
                   FROM code_chunks 
                   WHERE repo_id = %s 
                   ORDER BY embedding <=> %s 
                   LIMIT %s""",
                (repo_id, query_embedding, top_k)
            )
            return cur.fetchall()

# Auto-initialize on import (optional, but good for quick starts)
if __name__ == "__main__":
    init_db()
    print("DB module loaded and tested.")
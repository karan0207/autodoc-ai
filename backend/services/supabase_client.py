"""
Supabase client for vector storage using pgvector.

This module provides a connection to Supabase PostgreSQL database
with pgvector extension for storing and querying document embeddings.
"""

from supabase import create_client, Client
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

# Load .env from backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
logger = logging.getLogger(__name__)


class SupabaseClient:
    """Singleton Supabase client for database operations."""
    
    _instance: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get or create Supabase client instance."""
        if cls._instance is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_SERVICE_KEY")
            
            if not url or not key:
                raise ValueError(
                    "SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env"
                )
            
            cls._instance = create_client(url, key)
            logger.info("✅ Supabase client initialized")
        
        return cls._instance
    
    @classmethod
    def test_connection(cls) -> bool:
        """Test database connection."""
        try:
            client = cls.get_client()
            # Simple query to test connection
            result = client.table("chunks").select("count", count="exact").limit(0).execute()
            logger.info("✅ Supabase connection successful")
            return True
        except Exception as e:
            logger.error(f"❌ Supabase connection failed: {e}")
            return False
    
    @classmethod
    async def initialize_schema(cls) -> None:
        """
        Initialize database schema with pgvector extension and tables.
        This should be run once during setup.
        """
        client = cls.get_client()
        
        # Note: pgvector extension and table creation should be done via Supabase dashboard
        # or SQL editor, not via Python client for security reasons
        logger.info("⚠️  Please run the schema migration SQL in Supabase dashboard")
        logger.info("SQL available in: backend/migrations/001_initial_schema.sql")

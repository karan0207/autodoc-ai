from typing import List, Dict
import re

class Chunker:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        """
        Split text into chunks with overlap.
        """
        if not text:
            return []
            
        chunks = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            
            # Try to find a natural break point (newline) if possible
            if end < text_len:
                # Look back for a newline
                last_newline = text.rfind('\n', start, end)
                if last_newline != -1 and last_newline > start + (self.chunk_size // 2):
                    end = last_newline + 1
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append({
                    "content": chunk_text,
                    "metadata": metadata
                })
            
            start = end - self.overlap
            if start < 0: start = 0
            
            # Avoid infinite loop if no progress
            if start >= end:
                start = end
            
        return chunks

# AutoDoc AI Backend

This is the FastAPI backend for AutoDoc AI, handling web crawling, text processing, embedding generation, RAG retrieval, and LLM-based documentation generation.

## Features

- **Web Crawling**: Playwright-based crawler for documentation websites
- **GitHub Integration**: Fetch README, changelog, and commit history
- **Text Processing**: Semantic chunking with configurable chunk sizes
- **Embeddings**: HuggingFace API integration for text embeddings
- **Vector Storage**: Weaviate vector database for similarity search
- **RAG**: Retrieval-Augmented Generation for context-aware documentation
- **LLM Generation**: OpenAI GPT-4 integration for multiple doc types

## Architecture

```
routes/           # FastAPI endpoints
├── ingest.py    # Ingestion endpoints
├── generate.py  # Documentation generation
└── status.py    # Job status tracking

services/        # Business logic
├── ingestion_service.py
├── generation_service.py
└── ...

crawler/         # Web crawling
embeddings/      # Embedding & vector storage
github/          # GitHub API integration
processors/      # Text chunking
rag/             # RAG retriever
```

## Setup

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file (copy from `.env.example`):

```env
OPENAI_API_KEY=your-openai-api-key
HUGGINGFACE_API_TOKEN=your-huggingface-token
WEAVIATE_URL=http://localhost:8080
```

### 3. Start Weaviate

```bash
docker-compose up -d
```

### 4. Run the Server

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Key Endpoints

### Ingestion

- `POST /ingest/start` - Start ingestion job
- `GET /ingest/status/{job_id}` - Get job status
- `GET /jobs` - List all jobs

### Generation

- `POST /generate/api-reference` - Generate API reference
- `POST /generate/product-description` - Generate product description
- `POST /generate/changelog-summary` - Generate changelog summary
- `POST /generate/seo-landing` - Generate SEO landing page

## Development

### Project Structure

- **Modular Design**: Each feature in its own module
- **Async/Await**: All I/O operations are async
- **Type Hints**: Full type annotations
- **Logging**: Comprehensive logging throughout
- **Error Handling**: Proper exception handling and user feedback

### Adding a New Generation Type

1. Add route in `routes/generate.py`
2. Implement logic in `services/generation_service.py`
3. Create prompt in the service
4. Test the endpoint

### Running Tests

```bash
pytest
pytest --cov=. --cov-report=html  # With coverage
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Yes | - |
| `HUGGINGFACE_API_TOKEN` | HuggingFace API token | Yes | - |
| `WEAVIATE_URL` | Weaviate instance URL | Yes | `http://localhost:8080` |
| `LOG_LEVEL` | Logging level | No | `INFO` |

## Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **playwright**: Web automation
- **beautifulsoup4**: HTML parsing
- **weaviate-client**: Vector database client
- **openai**: OpenAI API client
- **python-dotenv**: Environment variable management
- **pydantic**: Data validation

## Troubleshooting

### Weaviate Connection Issues

Ensure Docker is running and Weaviate is accessible:
```bash
docker ps
curl http://localhost:8080/v1/.well-known/ready
```

### Playwright Installation

If Playwright browsers aren't installed:
```bash
playwright install chromium
```

### API Rate Limits

- OpenAI: Monitor usage at platform.openai.com
- HuggingFace: Free tier has rate limits, consider upgrading

## License

MIT

# AutoDoc AI

AutoDoc AI is an automatic documentation generator that ingests a company’s website and GitHub repositories to generate structured documentation using LLMs and RAG.

## Features

- **Ingestion**: Crawls documentation websites and fetches GitHub repository content (README, Changelog, Commits).
- **Processing**: Chunks text semantically and stores embeddings in a local Weaviate vector database.
- **Generation**: Uses OpenAI GPT-4o to generate:
    - API References
    - Product Descriptions
    - Changelog Summaries
    - SEO Landing Pages
- **Export**: Export generated documentation to Markdown or copy to clipboard.

## Architecture

- **Backend**: Python FastAPI
- **Frontend**: Next.js + Tailwind CSS + Shadcn UI
- **Database**: Weaviate (Vector DB), Redis (Task Queue)
- **Infrastructure**: Docker Compose

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.10+
- OpenAI API Key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd autodoc-ai
   ```

2. **Start Infrastructure**
   ```bash
   docker-compose up -d
   ```

3. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   
   # Create .env file
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

   Run the backend:
   ```bash
   uvicorn main:app --reload
   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Usage**
   - Open `http://localhost:3000`
   - Enter a documentation URL (e.g., `https://fastapi.tiangolo.com/`) and a GitHub Repo URL.
   - Click "Start Ingestion".
   - Once finished, select a generation type (e.g., "API Reference").
   - View and export the generated documentation.

## API Documentation

The backend API documentation is available at `http://localhost:8000/docs`.

## License

MIT

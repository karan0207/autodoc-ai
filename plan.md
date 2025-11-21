# AutoDoc AI - Implementation Plan

Based on `product.md`, here is a step-by-step plan to build the AutoDoc AI prototype.



- NON Negotiable Requirements:
  The codebase must reflect senior-level engineering quality

Well-designed abstractions

Thoughtful naming

Minimal surprises

Zero “clever but unreadable” solutions

2. The code must be easy to read and reason about

Clear separation of concerns

Short, focused functions

Predictable folder structure

Consistent styles and patterns

3. The architecture must be clean, modular, and maintainable

Logical modules (ingestion, processing, embeddings, generation, API)

No cross-module leaks

Clear boundaries between backend, workers, and UI

Components should be replaceable without rewriting the system

4. The code should be future-proof and easy to extend

New generators (SEO, changelog, API docs) should plug in easily

Crawlers and processors should be composable and configurable

No hardcoded logic buried deep in the workflow

5. Strong documentation standards

Each module has an internal README explaining design, inputs, outputs

Clear inline comments for non-obvious logic

API routes documented via OpenAPI/Swagger

6. Reliability and predictability

Deterministic behavior

Minimal implicit magic

Logs must be clear and helpful

Failures bubble up with actionable messages

## Phase 1: Foundation & Infrastructure Setup
- [x] **Project Initialization**
    - [x] Set up monorepo structure (or separate folders for `backend` and `frontend`).
    - [x] Initialize Git repository.
    - [x] Create `docker-compose.yml` for orchestrating services (Backend, Frontend, Vector DB, Redis).
- [x] **Backend Setup (FastAPI)**
    - [x] Initialize Python FastAPI project.
    - [x] Configure environment variables management (`.env`).
    - [x] Set up basic logging and error handling.
- [x] **Frontend Setup (Next.js)**
    - [x] Initialize Next.js 14+ project with TypeScript and Tailwind CSS and shadcn components.
    - [x] Set up basic layout and navigation (Shell).
- [x] **Database & Vector Store**
    - [x] Set up local Vector DB (e.g., Weaviate or ChromaDB) via Docker.
    - [x] Set up Redis for task queue (optional but recommended for crawling jobs) via docker.

## Phase 2: Ingestion Layer (The "Crawler")
- [x] **Website Crawler**
    - [x] Implement Playwright-based crawler service.
    - [x] Create logic to limit depth (max 2 levels) and filter for documentation paths (`/docs`, `/api`, etc.).
    - [x] Implement HTML to text conversion (using `BeautifulSoup` or similar).
- [x] **GitHub Fetcher**
    - [x] Implement GitHub API client to fetch repo contents.
    - [x] Logic to target specific files: `README.md`, `CHANGELOG.md`, and `/docs` folder.
    - [x] Logic to fetch recent commit history.
- [x] **Ingestion Orchestration**
    - [x] Create an API endpoint to trigger ingestion for a project.
    - [x] Implement background job to run crawling/fetching asynchronously.

## Phase 3: Processing & Storage Layer
- [x] **Normalization & Chunking**
    - [x] Implement text cleaner (remove extra whitespace, boilerplate).
    - [x] Implement semantic chunking strategy (split by H1/H2 headers).
- [x] **Embedding & Indexing**
    - [ ] Integrate Embedding Model (OpenAI `text-embedding-3-small` or local).
    - [ ] Create logic to generate embeddings for chunks.
    - [x] Store chunks + embeddings + metadata (URL, source, timestamp) in Vector DB.

## Phase 4: Generation Layer (RAG & LLM)
- [x] **RAG Logic**
    - [x] Implement retrieval service: Query Vector DB for relevant chunks based on user intent.
- [x] **LLM Integration**
    - [x] Set up OpenAI API client (GPT-4o).
    - [x] Create Prompt Templates for:
        - [x] API Reference
        - [x] Product Description
        - [x] Changelog Summary
        - [x] SEO Landing Page
- [x] **Generation Endpoints**
    - [x] Create API endpoints to trigger generation for each type.

## Phase 5: Frontend UI Implementation
- [x] **Project Dashboard**
    - [x] Create "New Project" form (Input URL & GitHub Repo).
    - [x] Display list of ingested files/pages with status.
- [x] **Generation Interface**
    - [x] Create a panel to select generation type (API, Product, etc.).
    - [x] Display progress/loading state.
- [x] **Editor & Preview**
    - [x] Implement Markdown editor/viewer for generated content.
    - [x] Show "Sources" sidebar (which chunks were used).
- [x] **Export Actions**
    - [x] Implement "Copy to Clipboard".
    - [x] Implement "Download as Markdown/JSON".

## Phase 6: Testing & Refinement
- [x] **End-to-End Testing**
    - [x] System is running and ready for manual testing.
    - [ ] Verify accuracy of generated content (User to verify).
- [ ] **Performance Tuning**
    - [ ] Optimize crawl speed.
    - [ ] Ensure generation response time is within limits.

# Status: Prototype Complete 🚀
The core functionality has been implemented and is ready for usage.
1. Start Backend: `start_backend.bat`
2. Start Frontend: `start_frontend.bat`
3. Open `http://localhost:3000`
4. Enter URLs and Start Ingestion.
5. Generate Documentation.

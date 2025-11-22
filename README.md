<div align="center">

# 🤖 AutoDoc AI

**Automatic Documentation Generator powered by LLMs and RAG**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-black?logo=next.js&logoColor=white)](https://nextjs.org/)

</div>

---

## 📖 Overview

AutoDoc AI automatically generates comprehensive, structured documentation by ingesting your company's website and GitHub repositories. Using advanced LLM technology and Retrieval-Augmented Generation (RAG), it produces high-quality API references, product descriptions, changelog summaries, and SEO-optimized landing pages.

## ✨ Features

- 🕷️ **Smart Web Crawling**: Automatically crawls documentation websites using Playwright
- 📦 **GitHub Integration**: Fetches repository content including READMEs, changelogs, and commits
- 🧠 **AI-Powered Processing**: Semantic chunking and embedding generation with HuggingFace
- 💾 **Vector Storage**: Efficient similarity search using Weaviate vector database
- 🤖 **LLM Generation**: Multiple documentation types powered by OpenAI GPT-4
  - API References
  - Product Descriptions
  - Changelog Summaries
  - SEO Landing Pages
- 📤 **Export Options**: Markdown export and clipboard copy functionality
- 🎨 **Modern UI**: Beautiful, responsive interface built with Next.js and Shadcn UI

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   FastAPI    │─────▶│  Weaviate   │
│  (Next.js)  │      │   Backend    │      │ (Vector DB) │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  OpenAI API  │
                     │   (GPT-4)    │
                     └──────────────┘
```

**Tech Stack:**
- **Backend**: Python 3.10+, FastAPI, asyncio
- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS, Shadcn UI
- **Vector Database**: Weaviate
- **Embeddings**: HuggingFace Inference API
- **LLM**: OpenAI GPT-4
- **Web Scraping**: Playwright, BeautifulSoup4
- **Infrastructure**: Docker Compose

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ and npm
- Python 3.10+
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))
- HuggingFace API Token ([Get one here](https://huggingface.co/settings/tokens))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/autodoc-ai.git
   cd autodoc-ai
   ```

2. **Start Docker Services**
   ```bash
   docker-compose up -d
   ```
   This starts Weaviate on `http://localhost:8080`

3. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   HUGGINGFACE_API_TOKEN=your-huggingface-token-here
   WEAVIATE_URL=http://localhost:8080
   ```

5. **Run Backend**
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   Backend will be available at `http://localhost:8000`
   API docs at `http://localhost:8000/docs`

6. **Frontend Setup** (New Terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Frontend will be available at `http://localhost:3000`

### Using the Application

1. Open `http://localhost:3000` in your browser
2. Enter a documentation URL (e.g., `https://fastapi.tiangolo.com/`)
3. Optionally add a GitHub repository URL
4. Click **"Start Ingestion"** and wait for processing
5. Select a documentation type to generate:
   - **API Reference**: Complete API documentation
   - **Product Description**: Marketing-ready product overview
   - **Changelog Summary**: Condensed version history
   - **SEO Landing Page**: Search-optimized landing content
6. Preview, copy to clipboard, or export as Markdown

## 📁 Project Structure

```
autodoc-ai/
├── backend/
│   ├── crawler/          # Web crawling logic
│   ├── embeddings/       # Embedding generation & vector storage
│   ├── github/           # GitHub API integration
│   ├── processors/       # Text chunking and processing
│   ├── rag/              # RAG retriever
│   ├── routes/           # FastAPI endpoints
│   ├── services/         # Business logic services
│   ├── main.py           # FastAPI application entry
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── app/              # Next.js app directory
│   ├── components/       # React components
│   ├── lib/              # Utility functions
│   └── public/           # Static assets
├── docker-compose.yml    # Docker services configuration
├── LICENSE               # MIT License
└── README.md             # This file
```

## 🛠️ Development

### Running Tests

Backend tests:
```bash
cd backend
pytest
```

### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | Yes |
| `HUGGINGFACE_API_TOKEN` | HuggingFace token for embeddings | Yes |
| `WEAVIATE_URL` | Weaviate instance URL | Yes |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Next.js](https://nextjs.org/) for the React framework
- [Weaviate](https://weaviate.io/) for vector database technology
- [OpenAI](https://openai.com/) for GPT-4 API
- [HuggingFace](https://huggingface.co/) for embeddings API
- [Shadcn UI](https://ui.shadcn.com/) for beautiful UI components

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

<div align="center">
Made with ❤️ by the AutoDoc AI team
</div>

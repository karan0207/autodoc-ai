🎯 Product: AutoDoc AI — Automatic Documentation Generator

A tool that ingests a company’s website, docs, and GitHub repos, then generates structured documentation like API references, product descriptions, SEO pages, and changelog summaries using LLMs + RAG.

Prototype goal:
End-to-end single-project ingestion → preview → generate docs → export.

🔥 1. Core Problem

Companies have scattered documentation across websites, GitHub repos, README files, and changelogs.
Keeping them updated manually is slow and inconsistent.

🎯 2. Prototype Goal

Build a system that:

Crawls a website + GitHub repo

Converts everything into clean text chunks

Embeds + indexes it

Allows user to click “Generate” to produce:

API references

Product overview

Technical descriptions

SEO-ready landing pages

Changelog summaries

Shows sources & lets user edit

Export as Markdown or JSON

Prototype should be single-tenant, single-project, but fully functional.

🧱 3. High-Level Architecture

Ingestion Layer

Website crawler (Playwright-based)

GitHub fetcher (README, docs/, changelog, commits)

File normalizer (HTML → text, MD → text, code → docstrings)

Processing Layer

Document cleanup

Chunking by semantic boundaries (H1/H2)

Embeddings (OpenAI or local model)

Vector DB (Weaviate, Pinecone, or local FAISS)

Generation Layer

RAG: retrieve top chunks by topic

LLM templates for:

API Reference

Product Description

SEO Page

Changelog Summary

Feature Overview

UI / Dashboard

Project setup screen

Crawl status + ingested files viewer

“Generate Documentation” panel

Preview & edit markdown

Export to file or GitHub

🗂 4. Prototype Scope (must-have)
4.1 Project Creation

User pastes:

Website URL (root)

GitHub repo link

System begins ingestion automatically

4.2 Crawler

Crawl only:

docs paths (/docs, /guide, /api)

sitemap URLs if found

Depth: 2 levels max

Fetch raw HTML and convert to clean text

4.3 GitHub Fetcher

Pull:

README.md

/docs folder

CHANGELOG.md

Last 20 commits

Store content with metadata

4.4 Normalization & Chunking

Clean text

Extract sections by heading

Store chunks in vector DB with metadata:

url/path

heading

timestamp

4.5 LLM Generation Templates

Prototype includes 3 generators:

API Reference Generator

Input: “Generate API reference for all endpoints”

Output: Markdown containing endpoint info, params, examples

Product Description Generator

2–3 paragraphs describing product features, use cases

Changelog Summary

Summarize changes across last 5 GitHub commits or CHANGELOG sections

4.6 Preview UI

Show generated markdown

Highlight source snippets for each paragraph

Let user edit text before exporting

4.7 Export

Export to:

Markdown file

JSON

Copy to clipboard

🧪 5. Optional but useful (Prototype+1)

SEO landing page generator

Sidebar documentation generator (sections + pages)

FAQ generator

Multi-project support

Auth/login

Schedule auto-rebuilds

Push to GitHub PR

🔧 6. Technical Stack Recommendation

Backend:

Python (FastAPI)

Playwright for crawling

GitHub REST API for repo ingestion

FAISS or Weaviate for vector store

Redis queue (optional)

LLM Layer:

OpenAI GPT-4o / GPT-5

Embeddings: text-embedding-3-large or similar

Frontend:

Next.js

Tailwind

Editor: MDX editor or simple textarea for prototype

Infra:

Docker

Local FS or S3 bucket for snapshots

📂 7. Suggested Directory Structure (prototype)
/autodoc
  /backend
    /crawler
    /github
    /processors
    /embeddings
    /rag
    /routes
    main.py
  /frontend
    /app
    /components
  /shared
  docker-compose.yml
  README.md

📝 8. User Flow (Prototype)

User enters project name + URLs

Crawler + GitHub fetcher run in background

System extracts + chunks + embeds

User selects a generator:

“Generate Product Overview”

“Generate API Docs”

“Generate Changelog Summary”

LLM uses RAG to generate output

User edits and exports

🧭 9. Success Criteria (for your prototype)

End-to-end flow works reliably

Output is accurate and grounded (sources shown)

Ingestion handles at least:

20 website pages

20 markdown files

Response time: <8 seconds for generation

Code is clean enough to extend
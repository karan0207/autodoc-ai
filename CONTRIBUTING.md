# Contributing to AutoDoc AI

First off, thank you for considering contributing to AutoDoc AI! It's people like you that make AutoDoc AI such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct of being respectful and constructive.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if relevant**
- **Include your environment details** (OS, Python version, Node version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any alternatives you've considered**

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** if applicable
4. **Ensure the test suite passes**
5. **Update documentation** as needed
6. **Write a clear commit message**

## Development Setup

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## Coding Standards

### Python (Backend)

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Use async/await for I/O operations

Example:
```python
async def fetch_data(url: str) -> Dict[str, Any]:
    """
    Fetch data from the specified URL.
    
    Args:
        url: The URL to fetch data from
        
    Returns:
        Dictionary containing the fetched data
        
    Raises:
        HTTPException: If the request fails
    """
    # Implementation here
    pass
```

### TypeScript/React (Frontend)

- Use TypeScript for type safety
- Follow React best practices and hooks conventions
- Use functional components
- Keep components small and focused
- Use meaningful variable and function names

Example:
```typescript
interface DocumentProps {
  title: string;
  content: string;
  onExport: () => void;
}

export function DocumentPreview({ title, content, onExport }: DocumentProps) {
  // Implementation here
}
```

## Project Structure

### Backend

- `crawler/` - Web crawling logic
- `embeddings/` - Embedding generation and vector storage
- `github/` - GitHub API integration
- `processors/` - Text processing and chunking
- `rag/` - RAG retrieval logic
- `routes/` - FastAPI route handlers
- `services/` - Business logic

### Frontend

- `app/` - Next.js pages and routes
- `components/` - Reusable React components
- `lib/` - Utility functions and helpers
- `public/` - Static assets

## Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

Examples:
```
feat: Add GitHub commit history fetching
fix: Resolve embedding timeout issue
docs: Update installation instructions
refactor: Simplify crawler URL validation
test: Add tests for chunking service
```

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

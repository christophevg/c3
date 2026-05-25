# Web Application README Template

Use this template for Flask, FastAPI, Django, or other web applications.

```markdown
# {app-name}

[![CI](https://img.shields.io/github/actions/workflow/status/{user}/{repo}/ci.yml.svg)][ci]
[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]
[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)

> One-line description of what the app does.

## Overview

Brief description of the application, its purpose, and target users.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask / FastAPI / Django |
| Frontend | Vue.js / React / Template engine |
| Database | MongoDB / PostgreSQL / SQLite |
| Cache | Redis (optional) |

## Quick Start

\`\`\`bash
# Clone
git clone https://github.com/{user}/{repo}.git
cd {repo}

# Install dependencies
uv sync

# Run
uv run python app.py
\`\`\`

Access at: http://localhost:5000

## Screenshots

<!-- Add screenshot or GIF here -->
![App Screenshot](docs/screenshot.png)

## Features

| Feature | Description |
|---------|-------------|
| Feature 1 | Description |
| Feature 2 | Description |

## Installation

### Requirements

- Python 3.X+
- [uv](https://docs.astral.sh/uv/) for dependency management
- Node.js X+ (if frontend build needed)
- Database (MongoDB/PostgreSQL)

### Setup

\`\`\`bash
# Install dependencies
uv sync

# Install frontend dependencies (if applicable)
cd frontend
npm install
\`\`\`

### Configuration

Create `.env` file:

\`\`\`bash
# Required
SECRET_KEY=your-secret-key
DATABASE_URL=mongodb://localhost:27017/dbname

# Optional
DEBUG=True
LOG_LEVEL=INFO
\`\`\`

### Database Setup

\`\`\`bash
# Initialize database
uv run python scripts/init_db.py
\`\`\`

## Usage

### Development

\`\`\`bash
# Run development server
uv run python app.py

# Or with auto-reload
uv run flask run --debug
\`\`\`

### Production

\`\`\`bash
# Using gunicorn + uvicorn
uv run gunicorn app:app -w 1 -k uvicorn.workers.UvicornWorker

# Using docker
docker-compose up -d
\`\`\`

## Project Structure

\`\`\`
{app-name}/
├── app.py              # Main application
├── config.py           # Configuration
├── models/             # Data models
├── routes/             # API routes / views
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── tests/              # Test suite
└── pyproject.toml      # Dependencies
\`\`\`

## Testing

\`\`\`bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app
\`\`\`

## Deployment

### Docker

\`\`\`bash
docker build -t {app-name} .
docker run -p 5000:5000 {app-name}
\`\`\`

### Heroku

\`\`\`bash
heroku create
git push heroku main
\`\`\`

### Manual

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | - | Application secret |
| `DATABASE_URL` | Yes | - | Database connection |
| `DEBUG` | No | False | Enable debug mode |
| `LOG_LEVEL` | No | INFO | Logging level |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[MIT](LICENSE)

[ci]: https://github.com/{user}/{repo}/actions
[license]: https://github.com/{user}/{repo}/blob/main/LICENSE
```

## Badge Reference

For web applications, include these badges (3 total):

| Badge | Markdown |
|-------|----------|
| CI | `[![CI](https://img.shields.io/github/actions/workflow/status/{user}/{repo}/ci.yml.svg)][ci]` *(only if workflow exists)* |
| License | `[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]` |
| Agentic | `[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)` |

**Important:**

- **CI badge only if workflow exists** — check `.github/workflows/` before adding
- **Agentic badge is required** for all projects built using agentic workflow

## Section Guidelines

- **Tech Stack**: Clear table of technologies used
- **Screenshots**: Visual preview is important for web apps
- **Configuration**: Document environment variables
- **Deployment**: Multiple options if applicable
- **Project Structure**: Help contributors navigate the codebase
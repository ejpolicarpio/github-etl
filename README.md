# GitHub ETL

FastAPI-based service for extracting, transforming, and loading GitHub repository data into PostgreSQL.

## Overview

This application provides a RESTful API to fetch GitHub repository information and store it in a PostgreSQL database for analysis and reporting. It uses the GitHub API to extract repository metadata and efficiently loads it into a structured database schema.

## Tech Stack

- **Runtime**: Python 3.12 with UV package manager
- **Framework**: FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL 15
- **Migrations**: Alembic
- **Dependencies**: asyncpg, Pydantic, Loguru

## Features

- GitHub repository data extraction via GitHub API
- Structured data storage in PostgreSQL
- RESTful API endpoints for data access
- Database migrations with Alembic
- Asynchronous database operations
- Comprehensive logging

## Prerequisites

- Python 3.12+
- PostgreSQL 15+
- UV package manager
- GitHub API token (for API access)

## Local Development

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/github-etl.git
   cd github-etl
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start PostgreSQL** (using Docker):
   ```bash
   docker-compose up -d postgres
   ```

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the application:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

7. **Access the API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Development

Build and run the entire stack using Docker Compose:

```bash
docker-compose up --build
```

## Configuration

The application uses environment variables for configuration:

- `DATABASE_URL`: PostgreSQL connection string
- `GITHUB_TOKEN`: GitHub API token
- `LOG_LEVEL`: Logging level (default: INFO)
- `PORT`: Application port (default: 8000)

See `.env.example` for a complete list of configuration options.

## API Endpoints

- `GET /docs` - API documentation (Swagger UI)
- `GET /health` - Health check endpoint
- Additional endpoints documented in Swagger UI

## Database Schema

The application uses SQLAlchemy models to manage the database schema. Run migrations to set up the database:

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Infrastructure

This application is deployed using Kubernetes with Helm charts and ArgoCD GitOps.

**Infrastructure Repository**: [github-etl-infrastructure](../github-etl-infrastructure)

The infrastructure repo provides:
- Helm charts for Kubernetes deployment
- ArgoCD manifests for GitOps
- Development and production environment configurations
- Automated deployment scripts

## Deployment

### Local Kubernetes (Minikube)

Refer to the [infrastructure repository](../github-etl-infrastructure) for local deployment instructions.

### Production

Production deployments are managed via ArgoCD GitOps:
1. Push changes to the main branch
2. CI/CD builds and pushes Docker image
3. ArgoCD automatically syncs and deploys to production

## Development Workflow

1. Create a feature branch
2. Make changes and test locally
3. Run tests: `pytest`
4. Commit and push changes
5. Create a pull request
6. After merge, CI/CD handles deployment

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_repositories.py
```

## License

MIT

## Related Repositories

- **[Infrastructure](../github-etl-infrastructure)** - Kubernetes, Helm, and ArgoCD configurations
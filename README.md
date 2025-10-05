# GitHub ETL

FastAPI-based service for extracting, transforming, and loading GitHub repository data into PostgreSQL.

## Overview

This application provides a RESTful API to fetch GitHub repository information and store it in a PostgreSQL database for analysis and reporting. It uses the GitHub API to extract repository metadata and efficiently loads it into a structured database schema.

**This repository works in partnership with [github-etl-infrastructure](../github-etl-infrastructure)** which handles all Kubernetes deployment, Helm charts, and GitOps configurations.

## Repository Partnership

- **github-etl** (this repo): Application code, Dockerfile, dependencies, and local development
- **github-etl-infrastructure**: Kubernetes manifests, Helm charts, ArgoCD configs, and deployment automation

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

---

## Getting Started: Step-by-Step Instructions

### Step 1: Prerequisites Setup

Before starting, ensure you have the following installed:

- [ ] **Python 3.12+** - `python --version`
- [ ] **UV package manager** - `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] **Docker Desktop** - For running PostgreSQL and Minikube
- [ ] **Minikube** - `brew install minikube` (macOS)
- [ ] **kubectl** - `brew install kubectl`
- [ ] **Helm 3.x** - `brew install helm`
- [ ] **GitHub API token** - Create at https://github.com/settings/tokens

### Step 2: Clone Both Repositories

```bash
# Navigate to your projects directory
cd ~/Documents/projects

# Clone the application repository
git clone https://github.com/yourusername/github-etl.git

# Clone the infrastructure repository
git clone https://github.com/yourusername/github-etl-infrastructure.git

# You should now have:
# ~/Documents/projects/github-etl/
# ~/Documents/projects/github-etl-infrastructure/
```

### Step 3: Local Application Development

**Work in the `github-etl` directory:**

```bash
cd github-etl
```

1. **Install Python dependencies:**
   ```bash
   uv sync
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your configuration:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/github_etl
   GITHUB_TOKEN=your_github_token_here
   LOG_LEVEL=INFO
   PORT=8000
   ```

3. **Start PostgreSQL using Docker:**
   ```bash
   docker-compose up -d postgres
   ```

4. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start the application:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

6. **Verify the application is running:**
   - Open http://localhost:8000/docs for Swagger UI
   - Open http://localhost:8000/redoc for ReDoc
   - Test the health endpoint: `curl http://localhost:8000/health`

### Step 4: Docker Development (Optional)

To run the entire stack with Docker Compose:

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Step 5: Kubernetes Deployment Setup

**Switch to the `github-etl-infrastructure` directory:**

```bash
cd ../github-etl-infrastructure
```

Follow these steps in order:

1. **Start Minikube cluster:**
   ```bash
   ./scripts/setup-minikube.sh
   ```

   Verify cluster is running:
   ```bash
   kubectl cluster-info
   minikube status
   ```

2. **Install ArgoCD:**
   ```bash
   ./scripts/install-argocd.sh
   ```

   Wait for ArgoCD to be ready:
   ```bash
   kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s
   ```

3. **Get ArgoCD admin password:**
   ```bash
   kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
   ```

4. **Access ArgoCD UI:**
   ```bash
   kubectl port-forward svc/argocd-server -n argocd 8080:443
   ```
   - Open https://localhost:8080
   - Username: `admin`
   - Password: (from previous step)

5. **Deploy the application to Kubernetes:**
   ```bash
   # Deploy to development environment
   ./scripts/deploy.sh github-etl dev

   # Or deploy using Helm directly
   helm upgrade --install github-etl ./helm/github-etl \
     -f ./helm/github-etl/values-dev.yaml \
     -n github-etl --create-namespace
   ```

6. **Verify deployment:**
   ```bash
   kubectl get pods -n github-etl
   kubectl get svc -n github-etl
   ```

7. **Access the application in Kubernetes:**
   ```bash
   kubectl port-forward -n github-etl svc/github-etl 8000:8000
   ```
   Open http://localhost:8000/docs

### Step 6: Development Workflow

When making changes to the application:

1. **Make code changes in `github-etl` repository:**
   ```bash
   cd ~/Documents/projects/github-etl
   # Edit your code
   ```

2. **Test locally first:**
   ```bash
   # Run tests
   pytest

   # Test locally with Docker
   docker-compose up --build
   ```

3. **Build and push Docker image:**
   ```bash
   # Build image
   docker build -t yourusername/github-etl:v1.0.0 .

   # Push to registry
   docker push yourusername/github-etl:v1.0.0
   ```

4. **Update Helm chart in `github-etl-infrastructure`:**
   ```bash
   cd ~/Documents/projects/github-etl-infrastructure

   # Edit helm/github-etl/values.yaml to update image tag
   # Or update Chart.yaml version
   ```

5. **Deploy updated version:**
   ```bash
   ./scripts/deploy.sh github-etl dev
   ```

6. **Verify deployment:**
   ```bash
   kubectl rollout status deployment/github-etl -n github-etl
   kubectl logs -f deployment/github-etl -n github-etl
   ```

### Step 7: Production Deployment

Production uses GitOps with ArgoCD:

1. **Commit changes to both repositories:**
   ```bash
   # In github-etl
   git add .
   git commit -m "feat: add new feature"
   git push origin main

   # In github-etl-infrastructure
   git add .
   git commit -m "chore: update deployment config"
   git push origin main
   ```

2. **ArgoCD automatically syncs:**
   - Watches the infrastructure repository
   - Detects changes
   - Applies updates to production cluster

3. **Monitor deployment:**
   - Check ArgoCD UI
   - View application status
   - Review sync logs

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

## Related Repositories

- **[Infrastructure](../github-etl-infrastructure)** - Kubernetes, Helm, and ArgoCD configurations
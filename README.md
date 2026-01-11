# Crypto Tracker - Pricing Service

A microservice for monitoring and retrieving cryptocurrency price data as part of the Azure Crypto Tracker Application. Built with Flask and integrated with CoinGecko API, this service provides real-time cryptocurrency pricing information with support for price alerts and market data analysis.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Locally](#running-locally)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [CI/CD Deployment](#cicd-deployment)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)

## Features

- 🪙 Real-time cryptocurrency price tracking
- 📊 Market data retrieval and analysis
- 🔔 Price alert triggering system
- 🔐 JWT authentication
- 📚 Swagger/OpenAPI documentation
- 🧪 Comprehensive test coverage
- ☁️ Azure-native deployment (AKS)
- 🐳 Docker containerization

## Prerequisites

- Python 3.12+
- PostgreSQL 12+
- Docker (for containerized deployment)
- kubectl (for Kubernetes deployment)
- Azure CLI (for Azure deployment)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd pricing-service
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Initialize Database

Create a PostgreSQL database:

```bash
createdb pricing_db
```

Run database migrations:

```bash
alembic upgrade head
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Service Configuration
SERVICE_NAME=pricing-service
SERVICE_VERSION=1.0.0
ENVIRONMENT=development

# Security
SECRET_KEY=your-secret-key-here-change-in-production

# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-db-password
POSTGRES_DB=pricing_db
DB_HOST=localhost
DB_PORT=5432

# External API Configuration
COINGECKO_API_KEY=your-coingecko-api-key

# Logging
EXTERNAL_LOG_LEVEL=WARNING
LOG_REQUEST_COMPLETION=errors
```

### Sensitive Variables for Production

For production deployments, use Azure Key Vault or environment-specific secrets:

```bash
export SECRET_KEY=<production-secret-key>
export POSTGRES_PASSWORD=<secure-password>
export COINGECKO_API_KEY=<api-key>
```

## Running Locally

### Start the Application

```bash
# Using Flask development server
python -m flask run --host 0.0.0.0 --port 5000

# Or using gunicorn (production-like)
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

The application will be available at `http://localhost:5000`

### Access Swagger Documentation

Navigate to `http://localhost:5000/apidocs/` to access the interactive Swagger UI with all available endpoints.

### Health Check

Test the service health:

```bash
curl http://localhost:5000/health
```

## API Documentation

The API is documented using Swagger/OpenAPI 2.0 and is automatically generated from the code.

### Available Endpoints

#### Health Check
- `GET /health` - Service health status and version information

#### Coin Endpoints
- `GET /coins` - Retrieve list of tracked coins
- `GET /coins/<coin_id>` - Get specific coin details
- `POST /coins` - Add a new coin (requires authentication)

#### Price Data
- `GET /prices/<coin_id>` - Get current price data
- `GET /market-data/<coin_id>` - Get market data for a coin

#### Alerts
- `POST /alerts` - Create a price alert (requires authentication)
- `GET /alerts` - List user's alerts (requires authentication)

Full API documentation is available at the `/apidocs/` endpoint when running the application.

## Testing

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=app --cov-report=term-missing
```

### Test Files

- `tests/test_coin_api.py` - API endpoint tests
- `tests/test_coin_service.py` - Business logic tests
- `tests/test_health.py` - Health check tests
- `tests/test_models.py` - Database model tests

## Docker Deployment

### Build Docker Image

```bash
docker build -t pricing-service:latest .
```

### Run Docker Container Locally

```bash
docker run -p 5000:5000 \
  -e POSTGRES_HOST=host.docker.internal \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=your-password \
  -e SECRET_KEY=your-secret \
  -e COINGECKO_API_KEY=your-api-key \
  pricing-service:latest
```

### Push to Azure Container Registry

```bash
az acr build --registry cryptotracker --image pricing-service:latest .
```

## CI/CD Deployment

The project uses GitHub Actions for automated testing, building, and deployment to Azure Kubernetes Service (AKS).

### CI/CD Pipeline Overview

The pipeline (`.github/workflows/ci-cd.yml`) consists of three main jobs:

#### 1. **Test Job** (`test`)
- Runs on Ubuntu latest
- Sets up Python 3.12
- Installs dependencies
- Runs pytest with coverage reporting
- Ensures all tests pass before proceeding

**Trigger**: Automatically runs on every push to `main` branch

```yaml
- name: Run tests
  run: PYTHONPATH="${PYTHONPATH}:$(pwd)" pytest --cov=app --cov-report=term-missing
```

#### 2. **Build and Push Job** (`build-and-push`)
- **Depends on**: `test` job (runs only if tests pass)
- Sets up Docker Buildx for multi-platform builds
- Authenticates with Azure Container Registry (ACR)
- Builds Docker image for `linux/amd64` platform
- Pushes image to ACR with two tags:
  - `<SHA>` - Short commit SHA for traceability
  - `latest` - For easy reference to the most recent build

**Docker Image Naming Convention**:
```
cryptotracker.azurecr.io/pricing-service:<commit-sha>
cryptotracker.azurecr.io/pricing-service:latest
```

**Caching**: Uses GitHub Actions cache to speed up builds

#### 3. **Deploy to AKS Job** (`deploy-to-aks`)
- **Depends on**: `build-and-push` job (runs only after successful image push)
- Authenticates to Azure using OIDC (workload identity federation)
- Sets AKS cluster context
- Creates Docker registry secret for image pulling
- Updates the `pricing-service` deployment with new image
- Verifies rollout status and pod health

**Deployment Steps**:

```bash
# 1. Login to Azure using OIDC credentials
az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET -t $AZURE_TENANT_ID

# 2. Set AKS context
az aks get-credentials --name crypto-tracker --resource-group crypto-tracker

# 3. Create/update image pull secret
kubectl create secret docker-registry acr-creds --docker-server=cryptotracker.azurecr.io ...

# 4. Update deployment with new image
kubectl set image deployment/pricing-service pricing-service=cryptotracker.azurecr.io/pricing-service:<SHA>

# 5. Monitor rollout
kubectl rollout status deployment/pricing-service --timeout=180s
```

### Required GitHub Secrets

Configure these secrets in your repository settings (`Settings > Secrets and variables > Actions`):

| Secret | Description | Example |
|--------|-------------|---------|
| `ACR_USERNAME` | Azure Container Registry username | `<ACR-name>` |
| `ACR_PASSWORD` | Azure Container Registry password | `<ACR-password>` |
| `AZURE_CLIENT_ID` | Azure Service Principal client ID | `00000000-0000-0000-0000-000000000000` |
| `AZURE_TENANT_ID` | Azure tenant ID | `00000000-0000-0000-0000-000000000000` |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID | `00000000-0000-0000-0000-000000000000` |

### Required GitHub Variables

Configure these variables in your repository settings (`Settings > Secrets and variables > Actions`):

| Variable | Description | Example |
|----------|-------------|---------|
| `AKS_NAME` | AKS cluster name | `crypto-tracker` |
| `AKS_RG` | AKS resource group name | `crypto-tracker` |

### Deployment Flow

```
Push to main branch
    ↓
Run Tests (pytest)
    ↓
Tests Pass?
    ├─ No → Fail pipeline, notify
    └─ Yes ↓
      Build Docker Image
          ↓
      Push to ACR
          ↓
      Update AKS Deployment
          ↓
      Verify Rollout
          ↓
      Deployment Complete ✓
```

### Manual Deployment (if needed)

If you need to deploy manually without pushing code:

```bash
# 1. Build image locally
docker build -t cryptotracker.azurecr.io/pricing-service:custom-tag .

# 2. Push to ACR
az acr build --registry cryptotracker --image pricing-service:custom-tag .

# 3. Update deployment
kubectl set image deployment/pricing-service pricing-service=cryptotracker.azurecr.io/pricing-service:custom-tag

# 4. Monitor
kubectl rollout status deployment/pricing-service
```

### Troubleshooting Deployments

**Check deployment status**:
```bash
kubectl describe deployment pricing-service
kubectl get pods -l app=pricing-service
kubectl logs -l app=pricing-service
```

**View recent image**:
```bash
az acr repository show-tags --name cryptotracker --repository pricing-service
```

**Rollback to previous version**:
```bash
kubectl rollout undo deployment/pricing-service
```

## Project Structure

```
pricing-service/
├── app/
│   ├── __init__.py           # Application factory
│   ├── config.py             # Configuration management
│   ├── api/                  # API endpoints
│   │   ├── coin.py           # Coin endpoints
│   │   └── health.py         # Health check endpoint
│   ├── middleware/           # Custom middleware
│   │   └── auth_middleware.py # JWT authentication
│   ├── models/               # Database models
│   │   ├── coinModels.py
│   │   └── marketData.py
│   ├── repositories/         # Data access layer
│   │   └── coin_repository.py
│   ├── services/             # Business logic
│   │   ├── alert_trigger_service.py
│   │   ├── coin_service.py
│   │   └── price_service.py
│   └── utils/                # Utility functions
│       ├── coingecko.py      # CoinGecko API client
│       ├── json.py           # JSON utilities
│       ├── jwt_service.py    # JWT handling
│       ├── logger.py         # Logging configuration
│       └── resilience.py     # Retry/resilience logic
├── migrations/               # Alembic database migrations
├── tests/                    # Test suite
├── Dockerfile                # Docker configuration
├── requirements.txt          # Python dependencies
├── pytest.ini               # pytest configuration
├── wsgi.py                  # WSGI entry point
└── alembic.ini              # Alembic configuration
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVICE_NAME` | `pricing-service` | Service identifier |
| `SERVICE_VERSION` | `1.0.0` | API version |
| `ENVIRONMENT` | `development` | Environment (development/staging/production) |
| `SECRET_KEY` | `dev-secret-key-...` | JWT signing key (change in production!) |
| `POSTGRES_USER` | `postgres` | Database user |
| `POSTGRES_PASSWORD` | `postgres` | Database password |
| `POSTGRES_DB` | `pricing_db` | Database name |
| `DB_HOST` | `localhost` | Database hostname |
| `DB_PORT` | `5432` | Database port |
| `COINGECKO_API_KEY` | - | CoinGecko API key (optional, for higher limits) |
| `EXTERNAL_LOG_LEVEL` | `WARNING` | Logging level for external libraries |
| `LOG_REQUEST_COMPLETION` | `errors` | Request logging level |

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and ensure tests pass: `pytest`
3. Commit with clear messages: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Create Pull Request

All tests must pass and coverage should be maintained above 80%.

## Support & Troubleshooting

### Common Issues

**Database connection errors**:
- Ensure PostgreSQL is running
- Check `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` in `.env`

**CoinGecko API errors**:
- Verify internet connectivity
- Check `COINGECKO_API_KEY` if using authenticated requests
- Monitor rate limits (free tier: 10-50 calls/minute)

**Import errors**:
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Clear Python cache: `find . -type d -name __pycache__ -exec rm -r {} +`

## License

[Add license information here]

## Changelog

### Version 1.0.0
- Initial release
- Core pricing service functionality
- JWT authentication
- Swagger/OpenAPI documentation
- CI/CD pipeline with AKS deployment

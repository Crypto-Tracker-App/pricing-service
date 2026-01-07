# CryptoTracker - Pricing Service

A Flask-based microservice for the CryptoTracker application that fetches and manages cryptocurrency pricing data from CoinGecko.

## Overview

The Pricing Service is responsible for:
- Fetching current cryptocurrency prices
- Retrieving cryptocurrency market data
- Managing coin metadata and information
- Storing and updating coin data in the database
- Providing pricing endpoints for other CryptoTracker services

## Technology Stack

- **Language**: Python 3.14.
- **Framework**: Flask 3.1
- **ORM**: Flask-SQLAlchemy 3.1.1
- **WSGI Server**: Gunicorn 21.2.0
- **Data Source**: CoinGecko API (via coingecko-sdk 1.12.0)
- **Database**: PostgreSQL 18
- **Migrations**: Alembic 1.17.

## Local Development
.
### Installation

```bash
# Clone the repository
git clone https://github.com/Crypto-Tracker-App/pricing-service.git
cd pricing-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
POSTGRES_USER=dev_user
POSTGRES_PASSWORD=dev_password
POSTGRES_DB=dev_db
DB_PORT=5432
DB_HOST=localhost

COINGECKO_API_KEY=your_api_key_here
```

### Running with Docker Compose

```bash
# Start PostgreSQL and the application
docker-compose up

# The application will be available at http://localhost:12000
```

### Running Locally

```bash
# Run database migrations
alembic upgrade head

# Seed the database with initial coin data
flask seed

# Start the Flask development server
python wsgi.py
```

### CLI Commands

```bash
# Seed database with coin data
flask seed

# Update market data for all coins
flask update-market-data
```

## API Endpoints

### Health Check
```
GET /health
```
Returns health status and database connectivity check.

**Response:**
```json
{
  "status": "ok",
  "detail": "database connection ok"
}
```

### Get Top Coins
```
GET /api/top-coins?limit={limit}&offset={offset}
```
Retrieves top coins by market cap rank with pagination.

**Query Parameters:**
- `limit` (optional): Number of coins to return (default: 10, max: 100)
- `offset` (optional): Number of coins to skip (default: 0)

**Example:** `GET /api/top-coins?limit=20&offset=0`

**Response:**
```json
{
  "status": "success",
  "data": [...],
  "pagination": {
    "limit": 20,
    "offset": 0,
    "returned": 20
  }
}
```

### Get Coin by ID
```
GET /api/coin/{coin_id}
```
Retrieves a single coin's metadata and market data by CoinGecko ID.

**Path Parameters:**
- `coin_id`: CoinGecko coin identifier (e.g., "bitcoin", "ethereum")

**Example:** `GET /api/coin/bitcoin`

**Response:**
```json
{
  "status": "success",
  "data": {
    "id": "bitcoin",
    "name": "Bitcoin",
    "symbol": "BTC",
    ...
  }
}
```

## Deployment

### Azure Cloud Architecture

The Pricing Service is designed to run on Azure using the following services:

- **Azure Kubernetes Service (AKS)** - Container orchestration
- **Azure Container Registry (ACR)** - Private container image registry
- **Azure Monitor** - Application insights and logging

### Docker

The application is containerized using Docker with Python 3.14 Alpine base image.

```bash
# Build Docker image
docker build -t pricing-service:latest .

# Run container locally
docker run -p 12000:12000 \
  -e POSTGRES_USER=dev_user \
  -e POSTGRES_PASSWORD=dev_password \
  -e POSTGRES_DB=dev_db \
  -e DB_HOST=postgres \
  -e DB_PORT=5432 \
  -e COINGECKO_API_KEY=your_api_key \
  pricing-service:latest
```

The application runs on port **12000** using Gunicorn.

### Azure Container Registry

```bash
# Login to Azure
az login

# Login to Azure Container Registry
az acr login --name <your-acr-name>

# Tag image for ACR
docker tag pricing-service:latest cryptotracker.azurecr.io/pricing-service:latest

# Push image to ACR
docker push cryptotracker.azurecr.io/pricing-service:latest
```

### Azure Kubernetes Service Deployment

```bash
# Connect to AKS cluster
az aks get-credentials --resource-group <resource-group> --name <aks-cluster-name>

# Create Kubernetes namespace (optional)
kubectl create namespace crypto-tracker

# Deploy to AKS
kubectl apply -f k8s/ -n crypto-tracker

# Verify deployment
kubectl get pods -n crypto-tracker
kubectl get services -n crypto-tracker

# Check logs
kubectl logs -f deployment/pricing-service -n crypto-tracker
```

### CI/CD with GitHub Actions

Automated deployment pipeline:
1. **Build** - Build Docker image on push to main branch
2. **Push** - Push image to Azure Container Registry
3. **Deploy** - Update AKS deployment with new image
4. **Verify** - Run health checks

*Note: GitHub Actions workflow configuration coming soon.*

## Project Structure

```
pricing-service/
├── wsgi.py                     # Flask application entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container image definition
├── docker-compose.yml          # Docker Compose configuration
├── alembic.ini                 # Alembic migration configuration
├── app/
│   ├── __init__.py             # Flask app factory and CLI commands
│   ├── config.py               # Application configuration
│   ├── api/                    # API endpoints
│   │   ├── health.py           # Health check endpoint
│   │   └── coin.py             # Coin-related endpoints
│   ├── models/                 # Database models
│   │   ├── coinModels.py       # Coin entity model
│   │   └── marketData.py       # Market data model
│   ├── repositories/           # Data access layer
│   │   └── coin_repository.py  # Coin repository
│   ├── services/               # Business logic
│   │   ├── coin_service.py     # Coin service
│   │   └── price_service.py    # Price service
│   └── utils/                  # Utilities and helpers
│       ├── coingecko.py        # CoinGecko API client
│       ├── json.py             # JSON serialization utilities
│       └── logger.py           # Logging utilities
├── migrations/                 # Alembic database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 238525e66797_initialization_added_coin_and_.py
└── k8s/                        # Kubernetes manifests (currently empty)
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `POSTGRES_USER` | PostgreSQL username | Yes | postgres |
| `POSTGRES_PASSWORD` | PostgreSQL password | Yes | postgres |
| `POSTGRES_DB` | PostgreSQL database name | Yes | pricing_db |
| `DB_PORT` | PostgreSQL port | No | 5432 |
| `DB_HOST` | PostgreSQL host | No | localhost |
| `COINGECKO_API_KEY` | CoinGecko API key | Yes | - |
| `SERVICE_NAME` | Service identifier for logging | No | pricing-service |
| `SERVICE_VERSION` | Service version for logging | No | 1.0.0 |
| `ENVIRONMENT` | Deployment environment | No | development |
| `EXTERNAL_LOG_LEVEL` | Log level for external libraries | No | WARNING |
| `LOG_REQUEST_COMPLETION` | Request logging mode (errors\|all\|off) | No | errors |

### Azure-Specific Configuration

When deploying to Azure, these variables are typically managed through:
- **Azure Key Vault** - For sensitive data (passwords, API keys)
- **Kubernetes ConfigMaps** - For non-sensitive configuration
- **Kubernetes Secrets** - For sensitive configuration in-cluster

Example Kubernetes Secret:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: pricing-service-secrets
type: Opaque
stringData:
  POSTGRES_PASSWORD: <your-db-password>
  COINGECKO_API_KEY: <your-api-key>
```

# CryptoTracker - Pricing Service

A Flask-based microservice for the CryptoTracker application that fetches and manages cryptocurrency pricing data from CoinGecko.

## Overview

The Pricing Service is responsible for:
- Fetching current cryptocurrency prices
- Retrieving historical price data
- Storing pricing data in the database
- Providing pricing endpoints for other CryptoTracker services

## Technology Stack

- **Language**: Python 3.x
- **Framework**: Flask
- **Cloud Provider**: Azure
- **Data Source**: CoinGecko API
- **Database**: PostgreSQL (in-cluster)

## Local Development

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
FLASK_ENV=development
FLASK_APP=wsgi.py

POSTGRES_USER=dev_user
POSTGRES_PASSWORD=dev_password
POSTGRES_DB=userservice_db
DB_PORT=5432
DB_HOST=localhost

COINGECKO_API_KEY=your_api_key_here
LOG_LEVEL=INFO
```

## API Endpoints

### Health Check
```
GET /health
```

## Deployment

### Azure Services Used
- Azure Kubernetes Service (AKS) - Minimal cluster configuration
- PostgreSQL (in-cluster deployment)
- Logging Service (in-cluster)
- Azure Container Registry (ACR)

### Kubernetes Deployment

The service runs as a containerized application in a Kubernetes cluster.

Deployment is automated via CI/CD pipeline (GitHub Actions).

Manual deployment:
```bash
# Build Docker image
docker build -t pricing-service:latest .

# Tag and push to Azure Container Registry
az acr login --name <your-acr-name>
docker tag pricing-service:latest <your-acr-name>.azurecr.io/pricing-service:latest
docker push <your-acr-name>.azurecr.io/pricing-service:latest

# Deploy to AKS
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Monitoring & Logging

Logging is configured using a centralized logging service running in the cluster:
- Request/response logging
- Error tracking
- Performance monitoring
- External API call tracking (CoinGecko)

## Project Structure

```
pricing-service/
├── wsgi.py                  # Flask application entry point
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container image definition
├── .dockerignore          # Docker ignore file
├── k8s/                   # Kubernetes manifests
│   ├── pricingservice-deployment.yaml
│   ├── pricingservice-service.yaml
│   ├── pricingservice-configmap.yaml
│   ├── pricingservice-secret.yaml
│   ├── postgres-pvc.yaml
│   ├── postgres-service.yaml
│   └── postgres-deployment.yaml
├── app/
│   ├── models/              # Database models
│   ├── routes/              # API routes
│   └── utils/               # Utilities and helpers
├── migrations/           # Database migrations
└── tests/               # Test suite
```

## Development Roadmap

- [x] Create project structure
- [ ] Add CI/CD pipeline
- [ ] Create Dockerfile
- [ ] Create Kubernetes manifests
- [ ] Set up Azure infrastructure (AKS, ACR)
- [ ] Configure database
- [ ] Add database migrations
- [ ] Implement CoinGecko API client
- [ ] Add fetch current price endpoint
- [ ] Add fetch historical price endpoint
- [ ] Add logging and monitoring
- [ ] Add health check and readiness probes
- [ ] Add comprehensive tests
- [ ] Future: Implement caching layer
- [ ] Future: Add authentication/authorization

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `FLASK_ENV` | Environment (development/production) | Yes |
| `DATABASE_URL` | PostgreSQL connection string (in-cluster) | Yes |
| `COINGECKO_API_KEY` | CoinGecko API key | Yes |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | No |
| `LOGGING_SERVICE_URL` | In-cluster logging service endpoint | No |

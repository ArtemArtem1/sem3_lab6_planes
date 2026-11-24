# Lab 6 - Docker and CI

## Description

Containerized microservice application for storing aircraft data.
Based on Laboratory Work 5.

## Technologies

- Python 3.12
- FastAPI
- Pydantic
- HTTPX
- SQLite
- Docker
- Docker Compose
- GitHub Actions
- Ruff
- Mypy
- Pytest

## Architecture

Client -> API Gateway -> Storage Service -> SQLite

Services communicate through the Docker Compose network.
SQLite data is stored in a persistent Docker volume.

## Docker features

- Multi-stage Dockerfiles
- Python 3.12-slim base image
- Non-root user
- Separate runtime and development dependencies
- Docker layer caching
- Healthchecks
- Service discovery
- Persistent storage
- Environment-based configuration

## Configuration

```bash
cp .env.example .env
```

## Start application

```bash
docker compose up --build -d
```

## Check container status

```bash
docker compose ps
```

## Healthcheck

```bash
curl http://localhost:8000/health
```

## Swagger UI

http://localhost:8000/docs

## Create aircraft

```bash
curl -X POST http://localhost:8000/planes \
  -H "Content-Type: application/json" \
  -d '{"registration":"ra-89001","model":"Sukhoi Superjet 100","airline":"Rossiya"}'
```

## Get aircraft

```bash
curl http://localhost:8000/planes/1
```

## Failure handling

```bash
docker compose stop storage
curl -i http://localhost:8000/planes/1
docker compose start storage
```

Expected response during storage failure: HTTP 503.

## Persistent storage

```bash
docker compose down
docker compose up -d
```

Aircraft records are preserved in the named Docker volume.

## Check image size

```bash
docker images
```

## Check non-root user

```bash
docker compose exec storage whoami
docker compose exec gateway whoami
```

Expected result: app.

## Local tests

Run the following commands separately in storage_service
and api_gateway directories:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
ruff check .
mypy .
python -m pytest -v
```

Storage Service: 5 tests.
API Gateway: 7 tests.

## Continuous Integration

GitHub Actions runs the following steps on every push:

1. Create a clean virtual environment.
2. Install dependencies.
3. Run Ruff.
4. Run Mypy.
5. Run Pytest.
6. Build Docker images.

Workflow: .github/workflows/ci.yml

## Stop application

```bash
docker compose down
```

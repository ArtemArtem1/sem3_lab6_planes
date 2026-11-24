# System architecture

## Service interaction

```text
              Client
                 |
                 | HTTP
                 v
        +-----------------+
        |   API Gateway   |
        |    Port 8000    |
        +-----------------+
                 |
                 | REST / httpx
                 v
        +-----------------+
        | Storage Service |
        |    Port 8001    |
        +-----------------+
                 |
                 v
              SQLite
```

## Service boundaries

API Gateway is responsible for accepting external requests,
validating input and forwarding operations to Storage Service.

Storage Service is responsible for storing and retrieving
aircraft data using SQLite.

API Gateway does not access the database directly.
Services communicate only through the HTTP API.

Each service has its own configuration, dependencies
and independent entry point.

## Application layers

Both services contain three layers:

- api: HTTP endpoints and Pydantic schemas.
- domain: business rules, data models and repository interfaces.
- storage: implementations of repository interfaces.

The Storage Service uses SQLitePlaneRepository.
The API Gateway uses HTTPPlaneRepository.

Both implementations satisfy the PlaneRepository protocol.

The domain layer does not depend on FastAPI, SQLite or httpx.
Dependencies are injected through constructors.

The main.py module is the composition root.

## Dependency direction

```text
api --------> domain <-------- storage
                 |
               ports
```

The domain defines interfaces.
Infrastructure implements these interfaces.

## API contract

Both services support:

- POST /planes
- GET /planes/{plane_id}

Aircraft fields:

- id: integer identifier
- registration: aircraft registration
- model: aircraft model
- airline: airline name

Both services use compatible JSON schemas.

## Configuration

Configuration is loaded from environment variables
and .env files using pydantic-settings.

Host, port, database path, storage URL, request timeout
and logging level are configurable.

## Failure handling

API Gateway uses an explicit HTTP timeout.

Connection errors, timeouts and invalid storage responses
are converted to StorageUnavailableError.

API Gateway returns HTTP 503 when Storage Service
is unavailable and writes a warning to the log.

After Storage Service restarts, API Gateway can continue
processing requests without restarting.

## Testing

Domain tests use an in-memory fake repository.

HTTP client tests use mocks to simulate network failures.

No real network or database is required for unit tests.

- Storage Service: 5 domain tests.
- API Gateway: 5 domain tests and 2 HTTP client tests.
- Total: 12 tests.

## Container deployment

Both microservices run in separate Docker containers.

```text
Host
  |
  | localhost:8000
  |
  v
API Gateway Container
  |
  | HTTP: storage:8001
  |
  v
Storage Service Container
  |
  v
Docker Volume: planes_data
```

Docker Compose provides an internal network and DNS-based
service discovery.

Both containers use multi-stage images and run as a
non-root user.

The gateway starts only after the storage service becomes
healthy.

SQLite records are preserved in a named Docker volume
when containers are removed and recreated.

GitHub Actions automatically checks and builds both services.

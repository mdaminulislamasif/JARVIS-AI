# Jarvis-Cheng Bot Integration API

This directory contains the implementation of the Jarvis-Cheng Bot Integration API, which provides a secure REST API and WebSocket interface for external systems to control and interact with Cheng Bot programmatically.

## Project Structure

```
.cheng_bot/api/
├── __init__.py           # Package initialization
├── config.py             # Configuration file loader
├── models.py             # Core data models
├── requirements.txt      # Python dependencies
├── venv/                 # Python virtual environment
└── README.md            # This file
```

## Setup

### 1. Create Virtual Environment

```bash
python -m venv .cheng_bot/api/venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
.cheng_bot/api/venv/Scripts/activate
```

**Linux/Mac:**
```bash
source .cheng_bot/api/venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r .cheng_bot/api/requirements.txt
```

## Configuration

Configuration is loaded from `.cheng_bot/config.yaml`. The configuration file supports environment variable substitution using the `${VAR_NAME}` syntax.

### Environment Variables

- `JWT_SECRET`: Secret key for JWT token signing (required for production)

### Configuration Sections

- **api**: HTTP server settings (host, port, CORS)
- **authentication**: Authentication settings (API keys, JWT, rate limiting)
- **sessions**: Session management settings (timeout, max concurrent)
- **commands**: Command execution settings (timeouts, queue size, worker pool)
- **logging**: Operation logging settings (directory, rotation, retention)
- **security**: Security settings (workspace root, allowed commands, whitelist)

## Core Data Models

The API uses Pydantic models for data validation and serialization:

### Command Models
- `CommandRequest`: Request to execute a command
- `CommandResponse`: Response from command execution
- `Command`: Internal command representation
- `CommandResult`: Internal command result

### Session Models
- `Session`: Client session for maintaining context
- `SessionCreateRequest`: Request to create a new session
- `SessionResponse`: Response containing session information

### Event Models
- `Event`: Event published to subscribers
- `EventSubscription`: Event subscription request

### Status Models
- `SystemStatus`: Current system operational status
- `ResourceUsage`: System resource usage information
- `HealthStatus`: System health check status

### Authentication Models
- `ClientIdentity`: Authenticated client identity
- `AuthenticationRequest`: Authentication request

### Log Models
- `LogEntry`: Operation log entry
- `LogFilters`: Filters for querying logs

## API Keys

API keys are stored in `.cheng_bot/api_keys.json`. Each key has:
- `key`: The API key string (format: `cheng_bot_<env>_<random>`)
- `client_id`: Unique client identifier
- `permissions`: List of granted permissions (read, write, execute, admin)
- `rate_limit`: Requests per minute limit
- `description`: Human-readable description
- `created_at`: Creation timestamp
- `active`: Whether the key is active

### Sample API Key

A sample development API key is provided:
```
cheng_bot_dev_sample_key_for_testing_only_123
```

**⚠️ WARNING:** This is a sample key for development only. Generate secure keys for production use.

## Permissions

The API supports four permission levels:
- `READ`: Read files and query status
- `WRITE`: Modify files
- `EXECUTE`: Execute shell commands
- `ADMIN`: Full system access

## Next Steps

This completes Task 1 (project structure and core dependencies). The next tasks will implement:

1. Authentication service (API key and JWT validation)
2. Security validator (path validation, command sanitization)
3. Command validator and executor
4. Session management
5. Status monitoring
6. HTTP REST API endpoints
7. Event publisher/subscriber
8. WebSocket server
9. Operation logging
10. Error handling and recovery

## Development

### Running Tests

```bash
pytest .cheng_bot/api/tests/
```

### Code Style

The project follows PEP 8 style guidelines. Use `black` for formatting:

```bash
black .cheng_bot/api/
```

### Type Checking

Use `mypy` for static type checking:

```bash
mypy .cheng_bot/api/
```

## Documentation

- [Requirements Document](../specs/jarvis-cheng_bot-integration/requirements.md)
- [Design Document](../specs/jarvis-cheng_bot-integration/design.md)
- [Implementation Tasks](../specs/jarvis-cheng_bot-integration/tasks.md)

## License

This is part of the Cheng Bot project.

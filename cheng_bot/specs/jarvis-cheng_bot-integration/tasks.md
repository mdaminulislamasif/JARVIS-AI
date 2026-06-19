# Implementation Plan: Jarvis-Cheng Bot Integration

## Overview

This implementation plan breaks down the Jarvis-Cheng Bot Integration feature into discrete coding tasks. The feature provides a secure REST API and WebSocket interface that allows external systems (like Jarvis) to control Cheng Bot programmatically. The implementation uses Python with FastAPI for the backend, following an incremental approach that validates functionality at each step.

## Tasks

- [-] 1. Set up project structure and core dependencies
  - Create directory structure: `.cheng_bot/api/` for API code
  - Set up Python virtual environment and install FastAPI, uvicorn, websockets, PyJWT, structlog
  - Create configuration file loader for `config.yaml`
  - Define core data models (CommandRequest, CommandResponse, Session, Event)
  - _Requirements: 1.1, 1.3, 1.4_

- [ ] 2. Implement authentication service
  - [ ] 2.1 Create API key validator
    - Implement `APIKeyStore` class for loading and validating API keys from file
    - Implement `APIKeyValidator` class with `validate()` method
    - Create sample API keys file format (`.cheng_bot/api_keys.json`)
    - _Requirements: 2.1, 2.2_
  
  - [ ] 2.2 Create JWT token validator
    - Implement `JWTValidator` class using PyJWT library
    - Add token generation method for testing
    - Validate token expiration and claims
    - _Requirements: 2.3_
  
  - [ ] 2.3 Implement rate limiter
    - Create `RateLimiter` class with in-memory token bucket algorithm
    - Track requests per client ID
    - Enforce configurable rate limits
    - _Requirements: 2.5_
  
  - [ ] 2.4 Create authentication middleware
    - Implement FastAPI dependency for authentication
    - Extract credentials from headers (API key or JWT)
    - Return `ClientIdentity` object with permissions
    - Handle authentication failures with 401 responses
    - _Requirements: 2.1, 2.4_
  
  - [ ]* 2.5 Write unit tests for authentication service
    - Test valid/invalid API key authentication
    - Test valid/expired JWT tokens
    - Test rate limiting enforcement
    - Test whitelist checking
    - _Requirements: 2.1, 2.2, 2.3, 2.5, 2.6_

- [ ] 3. Implement security validator
  - [ ] 3.1 Create path validation logic
    - Implement `SecurityValidator.validate_file_path()` method
    - Resolve paths to absolute and check if within workspace root
    - Reject paths with `..`, symbolic links outside workspace
    - _Requirements: 9.1, 9.3, 9.4_
  
  - [ ] 3.2 Create shell command sanitizer
    - Implement `SecurityValidator.validate_shell_command()` method
    - Check command against whitelist
    - Sanitize shell metacharacters
    - _Requirements: 9.2, 9.5_
  
  - [ ] 3.3 Implement permission checker
    - Create `Permission` enum (READ, WRITE, EXECUTE, ADMIN)
    - Implement `check_permission()` method
    - _Requirements: 9.3, 9.6_
  
  - [ ]* 3.4 Write security tests
    - Test directory traversal prevention (`../../etc/passwd`)
    - Test command injection prevention (`; rm -rf /`)
    - Test paths outside workspace are rejected
    - Test permission enforcement
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6_

- [ ] 4. Implement command validator and executor
  - [ ] 4.1 Create command schema definitions
    - Define `COMMAND_TYPES` dictionary with schemas for each command type
    - Implement schema validation using Pydantic models
    - Create `Command` and `CommandResult` data classes
    - _Requirements: 11.1, 11.2, 11.3_
  
  - [ ] 4.2 Implement command validator
    - Create `CommandValidator` class
    - Validate command type exists
    - Validate parameters against schema
    - Return validation errors with details
    - _Requirements: 11.3, 11.4_
  
  - [ ] 4.3 Implement synchronous command executor
    - Create `CommandExecutor` class
    - Implement `execute_command()` for sync execution
    - Support command types: `read_file`, `write_file`, `list_directory`
    - Track execution duration and modified files
    - Return `CommandResult` with status and output
    - _Requirements: 3.1, 3.2, 3.3, 3.6, 3.7_
  
  - [ ] 4.4 Add command queue for async execution
    - Implement `CommandQueue` using `asyncio.Queue`
    - Create worker pool with configurable size
    - Implement `execute_async()` method that returns command_id
    - Store command results in memory for retrieval
    - _Requirements: 3.8, 3.9_
  
  - [ ] 4.5 Add remaining command types
    - Implement `execute_shell` command with security validation
    - Implement `search_code` command
    - Implement `analyze_code` command
    - _Requirements: 3.4, 3.5, 3.6_
  
  - [ ]* 4.6 Write unit tests for command execution
    - Test command validation (valid/invalid schemas)
    - Test synchronous command execution
    - Test async command execution and result retrieval
    - Test command timeout handling
    - Test FIFO queue ordering
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9_

- [ ] 5. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implement session management
  - [ ] 6.1 Create session store
    - Implement `SessionStore` class with in-memory storage
    - Store sessions by session_id
    - Support concurrent access with thread-safe operations
    - _Requirements: 5.1, 5.6_
  
  - [ ] 6.2 Implement session manager
    - Create `SessionManager` class
    - Implement `create_session()` with unique ID generation
    - Implement `get_session()` and `close_session()` methods
    - Implement `refresh_session()` to update last_activity
    - _Requirements: 5.1, 5.2, 5.5_
  
  - [ ] 6.3 Add session timeout handling
    - Implement background task for `cleanup_expired_sessions()`
    - Check sessions against timeout threshold (30 minutes)
    - Clean up resources for expired sessions
    - _Requirements: 5.3, 5.4_
  
  - [ ]* 6.4 Write unit tests for session management
    - Test session creation and retrieval
    - Test session timeout after inactivity
    - Test session cleanup
    - Test concurrent sessions
    - Test session context persistence
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [ ] 7. Implement status monitoring
  - [ ] 7.1 Create status collector
    - Implement `StatusMonitor` class
    - Track system state (idle, busy, error)
    - Count active operations and queued commands
    - _Requirements: 4.1, 4.3_
  
  - [ ] 7.2 Add resource usage monitoring
    - Use `psutil` library for CPU and memory monitoring
    - Implement `get_resource_usage()` method
    - _Requirements: 4.4_
  
  - [ ] 7.3 Implement health check
    - Create `health_check()` method
    - Check API, executor, and storage components
    - Return health status with component details
    - _Requirements: 4.6_
  
  - [ ]* 7.4 Write unit tests for status monitoring
    - Test status reporting within 100ms
    - Test active operations tracking
    - Test resource usage reporting
    - Test health check endpoint
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.6_

- [ ] 8. Implement HTTP REST API endpoints
  - [ ] 8.1 Create FastAPI application and router
    - Initialize FastAPI app with CORS middleware
    - Create API router with `/api/v1` prefix
    - Add authentication dependency to all routes
    - _Requirements: 1.1_
  
  - [ ] 8.2 Implement command endpoints
    - `POST /api/v1/commands` - Submit command for execution
    - `GET /api/v1/commands/{id}` - Get command status
    - `GET /api/v1/commands/{id}/output` - Get command output
    - `DELETE /api/v1/commands/{id}` - Cancel running command
    - _Requirements: 3.1, 3.7, 6.1, 6.2_
  
  - [ ] 8.3 Implement status and health endpoints
    - `GET /api/v1/status` - Get system status
    - `GET /api/v1/health` - Health check
    - _Requirements: 4.1, 4.2, 4.6_
  
  - [ ] 8.4 Implement session endpoints
    - `POST /api/v1/sessions` - Create session
    - `GET /api/v1/sessions/{id}` - Get session details
    - `DELETE /api/v1/sessions/{id}` - Close session
    - _Requirements: 5.1, 5.5_
  
  - [ ] 8.5 Implement schema and logs endpoints
    - `GET /api/v1/schema` - Get all command schemas
    - `GET /api/v1/schema/{command_type}` - Get specific schema
    - `GET /api/v1/logs` - Query operation logs
    - _Requirements: 11.1, 11.6, 7.5_
  
  - [ ]* 8.6 Write integration tests for HTTP endpoints
    - Test each endpoint with valid requests
    - Test authentication failures (401)
    - Test authorization failures (403)
    - Test validation errors (400)
    - Test resource not found (404)
    - _Requirements: 1.1, 1.3, 1.4, 1.5, 2.4, 3.7, 4.1, 5.1, 11.1_

- [ ] 9. Implement event publisher and subscriber
  - [ ] 9.1 Create event publisher
    - Implement `EventPublisher` class
    - Support `publish()` for broadcast events
    - Support `publish_to_client()` for targeted events
    - Define event types (file_changed, command_completed, error, state_changed)
    - _Requirements: 10.1, 10.2, 10.3_
  
  - [ ] 9.2 Create event subscriber
    - Implement `EventSubscriber` class
    - Support `subscribe()` and `unsubscribe()` methods
    - Filter events by type for each client
    - _Requirements: 10.4, 10.5_
  
  - [ ] 9.3 Add event buffering
    - Buffer events when client is disconnected
    - Implement `get_buffered_events()` method
    - Deliver buffered events on reconnection
    - _Requirements: 10.6_
  
  - [ ]* 9.4 Write unit tests for event system
    - Test event publishing to all subscribers
    - Test targeted event publishing
    - Test subscription and unsubscription
    - Test event filtering by type
    - Test event buffering during disconnection
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

- [ ] 10. Implement WebSocket server and real-time events
  - [ ] 10.1 Create WebSocket endpoint
    - Add `WS /api/v1/ws` endpoint to FastAPI
    - Handle WebSocket connection lifecycle
    - Authenticate WebSocket connections
    - _Requirements: 1.2_
  
  - [ ] 10.2 Integrate event streaming
    - Connect WebSocket clients to EventSubscriber
    - Stream events to connected clients in real-time
    - Handle client disconnections gracefully
    - _Requirements: 10.1, 10.2, 10.3_
  
  - [ ] 10.3 Add subscription management over WebSocket
    - Accept subscription messages from clients
    - Allow clients to subscribe/unsubscribe to event types
    - Send buffered events on reconnection
    - _Requirements: 10.4, 10.5, 10.6_
  
  - [ ]* 10.4 Write integration tests for WebSocket
    - Test WebSocket connection and authentication
    - Test event streaming to clients
    - Test subscription/unsubscription
    - Test event buffering and delivery
    - Test multiple concurrent WebSocket connections
    - _Requirements: 1.2, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

- [ ] 11. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 12. Implement operation logging and audit trail
  - [ ] 12.1 Create operation logger
    - Implement `OperationLogger` class
    - Log commands received with timestamp, client_id, session_id
    - Log command results with status and duration
    - Use structured logging with `structlog`
    - _Requirements: 7.1, 7.2_
  
  - [ ] 12.2 Add log persistence and rotation
    - Write logs to disk in `.cheng_bot/logs/` directory
    - Implement log rotation when size exceeds 100MB
    - Implement log retention (30 days)
    - _Requirements: 7.3, 7.4, 7.6_
  
  - [ ] 12.3 Implement log query engine
    - Create `query_logs()` method with filters
    - Support filtering by timestamp, client_id, command_type, status
    - Return matching log entries
    - _Requirements: 7.5_
  
  - [ ]* 12.4 Write unit tests for logging
    - Test command logging
    - Test result logging
    - Test log rotation
    - Test log querying with various filters
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 13. Implement error handling and recovery
  - [ ] 13.1 Add global error handlers
    - Create FastAPI exception handlers for common errors
    - Return standardized error responses with error codes
    - Log all errors with context
    - _Requirements: 1.5, 8.2, 8.3_
  
  - [ ] 13.2 Implement command timeout handling
    - Add timeout wrapper for command execution
    - Terminate commands that exceed timeout
    - Return timeout error to client
    - _Requirements: 8.3_
  
  - [ ] 13.3 Add circuit breaker
    - Implement circuit breaker pattern for command executor
    - Open circuit after 5 consecutive failures
    - Half-open state after 30 seconds
    - Close circuit after 2 successful requests
    - _Requirements: 8.6_
  
  - [ ] 13.4 Implement retry logic
    - Add exponential backoff retry for transient failures
    - Maximum 3 retry attempts
    - Configurable retry policy per command type
    - _Requirements: 8.4_
  
  - [ ]* 13.5 Write integration tests for error handling
    - Test error responses for various failure scenarios
    - Test timeout handling
    - Test circuit breaker behavior
    - Test retry logic
    - Test graceful degradation
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

- [ ] 14. Integrate components and wire everything together
  - [ ] 14.1 Create main application entry point
    - Initialize all components (AuthService, CommandExecutor, SessionManager, etc.)
    - Wire dependencies between components
    - Load configuration from `config.yaml`
    - Start FastAPI server with uvicorn
    - _Requirements: 1.1, 1.2_
  
  - [ ] 14.2 Connect command executor to event publisher
    - Publish `command_completed` events after execution
    - Publish `error` events on failures
    - Publish `file_changed` events when files are modified
    - _Requirements: 10.1, 10.2, 10.3_
  
  - [ ] 14.3 Connect status monitor to event publisher
    - Publish `state_changed` events when system state changes
    - Broadcast state changes to all connected clients
    - _Requirements: 4.5_
  
  - [ ] 14.4 Integrate operation logger with all components
    - Log all commands received by API
    - Log all authentication attempts
    - Log all security violations
    - _Requirements: 7.1, 7.2_
  
  - [ ]* 14.5 Write end-to-end integration tests
    - Test complete workflow: authenticate → create session → execute commands → receive events → close session
    - Test multiple concurrent sessions
    - Test long-running async commands
    - Test error recovery
    - _Requirements: All requirements_

- [ ] 15. Add configuration and deployment setup
  - [ ] 15.1 Create configuration file template
    - Create `config.yaml` with all configurable parameters
    - Add environment variable substitution support
    - Document all configuration options
    - _Requirements: 2.2, 2.3, 2.5, 3.8, 5.3, 7.3, 7.4, 9.5_
  
  - [ ] 15.2 Create API key management utilities
    - Create script to generate new API keys
    - Create script to revoke API keys
    - Create script to list active API keys
    - _Requirements: 2.2_
  
  - [ ] 15.3 Add startup and shutdown handlers
    - Implement graceful shutdown for FastAPI
    - Clean up resources (sessions, queued commands)
    - Close WebSocket connections gracefully
    - _Requirements: 5.4_

- [ ] 16. Performance optimization and load testing
  - [ ] 16.1 Optimize command execution performance
    - Profile command execution paths
    - Optimize hot paths for <500ms execution
    - Optimize status checks for <50ms response
    - _Requirements: 3.1, 4.2, 12.3_
  
  - [ ] 16.2 Add connection pooling and resource limits
    - Limit concurrent command executions to 10
    - Limit command queue size to 1000
    - Limit concurrent WebSocket connections
    - _Requirements: 12.1, 12.4_
  
  - [ ]* 16.3 Run load tests
    - Test 100 requests/second sustained load
    - Test burst traffic (200 req/s for 30 seconds)
    - Test concurrent command execution (20 simultaneous)
    - Test WebSocket stress (100 connected clients)
    - Verify performance requirements are met
    - _Requirements: 12.2, 12.3, 12.4, 12.5_

- [ ] 17. Create API documentation
  - [ ] 17.1 Generate OpenAPI documentation
    - FastAPI automatically generates OpenAPI schema
    - Add descriptions to all endpoints
    - Add request/response examples
    - _Requirements: 11.1, 11.2_
  
  - [ ] 17.2 Write usage guide
    - Document authentication setup
    - Provide example API calls with curl
    - Document WebSocket connection flow
    - Provide example event subscriptions
    - _Requirements: 1.1, 1.2, 2.1, 2.3_
  
  - [ ] 17.3 Create client SDK examples
    - Provide Python client example
    - Provide JavaScript client example
    - Show authentication, command execution, event handling
    - _Requirements: 1.1, 1.2, 3.1, 10.1_

- [ ] 18. Final checkpoint - Ensure all tests pass
  - Run complete test suite (unit + integration + load tests)
  - Verify all requirements are met
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- The implementation uses Python with FastAPI as specified in the design document
- Security is enforced at multiple layers: authentication, authorization, input validation, and sandboxing
- All components are designed for testability with clear interfaces
- The feature supports both synchronous and asynchronous command execution
- Real-time event streaming enables external systems to monitor Cheng Bot operations
- Comprehensive logging provides audit trail for security and troubleshooting

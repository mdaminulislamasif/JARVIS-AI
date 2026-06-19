"""
Core data models for the Jarvis-Cheng Bot Integration API.

This module defines the data structures used throughout the API including
CommandRequest, CommandResponse, Session, and Event models.
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum
from pydantic import BaseModel, Field
import uuid


class Permission(str, Enum):
    """Permission levels for API access."""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class CommandStatus(str, Enum):
    """Status of command execution."""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    TIMEOUT = "timeout"
    QUEUED = "queued"
    RUNNING = "running"
    CANCELLED = "cancelled"


class SystemState(str, Enum):
    """Operational state of the system."""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"


class EventType(str, Enum):
    """Types of events that can be published."""
    FILE_CHANGED = "file_changed"
    COMMAND_COMPLETED = "command_completed"
    ERROR = "error"
    STATE_CHANGED = "state_changed"


# ============================================================================
# Command Models
# ============================================================================

class CommandRequest(BaseModel):
    """Request to execute a command."""
    command_type: str = Field(..., description="Type of command to execute")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Command parameters")
    timeout: int = Field(default=30, description="Timeout in seconds")
    async_execution: bool = Field(default=False, description="Execute asynchronously")
    session_id: Optional[str] = Field(default=None, description="Session ID for context")
    
    class Config:
        json_schema_extra = {
            "example": {
                "command_type": "read_file",
                "parameters": {"path": "src/main.py"},
                "timeout": 30,
                "async_execution": False,
                "session_id": "sess_abc123"
            }
        }


class ErrorDetail(BaseModel):
    """Detailed error information."""
    error_code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional error context")


class CommandResponse(BaseModel):
    """Response from command execution."""
    command_id: str = Field(..., description="Unique command identifier")
    status: CommandStatus = Field(..., description="Execution status")
    output: Optional[Any] = Field(default=None, description="Command output")
    error: Optional[ErrorDetail] = Field(default=None, description="Error details if failed")
    duration_ms: int = Field(..., description="Execution duration in milliseconds")
    modified_files: List[str] = Field(default_factory=list, description="Files modified by command")
    request_id: str = Field(..., description="Request ID for tracing")
    
    class Config:
        json_schema_extra = {
            "example": {
                "command_id": "cmd_xyz789",
                "status": "success",
                "output": "File contents here...",
                "error": None,
                "duration_ms": 45,
                "modified_files": [],
                "request_id": "req_abc123"
            }
        }


class Command(BaseModel):
    """Internal command representation."""
    command_id: str = Field(default_factory=lambda: f"cmd_{uuid.uuid4().hex[:12]}")
    command_type: str
    parameters: Dict[str, Any]
    timeout: int = 30
    session_id: Optional[str] = None
    client_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CommandResult(BaseModel):
    """Internal command result representation."""
    command_id: str
    status: CommandStatus
    output: Optional[Any] = None
    error: Optional[str] = None
    duration_ms: int
    modified_files: List[str] = Field(default_factory=list)
    completed_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Session Models
# ============================================================================

class Session(BaseModel):
    """Client session for maintaining context."""
    session_id: str = Field(default_factory=lambda: f"sess_{uuid.uuid4().hex[:12]}")
    client_id: str = Field(..., description="Client identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    timeout_seconds: int = Field(default=1800, description="Session timeout in seconds")
    context: Dict[str, Any] = Field(default_factory=dict, description="Session context data")
    permissions: List[Permission] = Field(default_factory=list, description="Session permissions")
    active: bool = Field(default=True, description="Whether session is active")
    
    def is_expired(self) -> bool:
        """Check if session has expired."""
        elapsed = (datetime.utcnow() - self.last_activity).total_seconds()
        return elapsed > self.timeout_seconds
    
    def refresh(self) -> None:
        """Update last activity timestamp."""
        self.last_activity = datetime.utcnow()
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "sess_abc123",
                "client_id": "jarvis_main",
                "created_at": "2024-01-15T10:30:00Z",
                "last_activity": "2024-01-15T10:35:00Z",
                "timeout_seconds": 1800,
                "context": {"workspace": "/home/user/project"},
                "permissions": ["read", "write"],
                "active": True
            }
        }


class SessionCreateRequest(BaseModel):
    """Request to create a new session."""
    client_id: Optional[str] = Field(default=None, description="Optional client identifier")
    timeout_seconds: Optional[int] = Field(default=None, description="Optional custom timeout")
    context: Dict[str, Any] = Field(default_factory=dict, description="Initial session context")


class SessionResponse(BaseModel):
    """Response containing session information."""
    session_id: str
    client_id: str
    created_at: datetime
    timeout_seconds: int
    active: bool


# ============================================================================
# Event Models
# ============================================================================

class Event(BaseModel):
    """Event published to subscribers."""
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:12]}")
    event_type: EventType = Field(..., description="Type of event")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = Field(..., description="Event payload")
    client_id: Optional[str] = Field(default=None, description="Target client (None for broadcast)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "event_id": "evt_xyz789",
                "event_type": "file_changed",
                "timestamp": "2024-01-15T10:30:00Z",
                "data": {
                    "path": "src/main.py",
                    "change_type": "modified"
                },
                "client_id": None
            }
        }


class EventSubscription(BaseModel):
    """Event subscription request."""
    event_types: List[EventType] = Field(..., description="Event types to subscribe to")


# ============================================================================
# Status Models
# ============================================================================

class ResourceUsage(BaseModel):
    """System resource usage information."""
    cpu_percent: float = Field(..., description="CPU usage percentage")
    memory_mb: float = Field(..., description="Memory usage in MB")
    memory_percent: float = Field(..., description="Memory usage percentage")
    disk_usage_percent: Optional[float] = Field(default=None, description="Disk usage percentage")


class SystemStatus(BaseModel):
    """Current system operational status."""
    state: SystemState = Field(..., description="Current system state")
    active_operations: int = Field(..., description="Number of active operations")
    queued_commands: int = Field(..., description="Number of queued commands")
    connected_clients: int = Field(default=0, description="Number of connected clients")
    uptime_seconds: int = Field(..., description="System uptime in seconds")
    resource_usage: ResourceUsage = Field(..., description="Resource usage information")
    last_error: Optional[str] = Field(default=None, description="Last error message")


class HealthStatus(BaseModel):
    """System health check status."""
    healthy: bool = Field(..., description="Overall health status")
    checks: Dict[str, bool] = Field(..., description="Individual component health checks")
    message: str = Field(..., description="Health status message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Authentication Models
# ============================================================================

class ClientIdentity(BaseModel):
    """Authenticated client identity."""
    client_id: str = Field(..., description="Unique client identifier")
    permissions: List[Permission] = Field(..., description="Granted permissions")
    rate_limit: int = Field(..., description="Rate limit (requests per minute)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional client metadata")


class AuthenticationRequest(BaseModel):
    """Authentication request."""
    api_key: Optional[str] = Field(default=None, description="API key for authentication")
    jwt_token: Optional[str] = Field(default=None, description="JWT token for authentication")


# ============================================================================
# Log Models
# ============================================================================

class LogEntry(BaseModel):
    """Operation log entry."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    log_id: str = Field(default_factory=lambda: f"log_{uuid.uuid4().hex[:12]}")
    command_id: str
    client_id: str
    session_id: Optional[str] = None
    command_type: str
    parameters: Dict[str, Any]
    status: CommandStatus
    duration_ms: int
    error: Optional[str] = None
    modified_files: List[str] = Field(default_factory=list)


class LogFilters(BaseModel):
    """Filters for querying logs."""
    start_time: Optional[datetime] = Field(default=None, description="Start time filter")
    end_time: Optional[datetime] = Field(default=None, description="End time filter")
    client_id: Optional[str] = Field(default=None, description="Client ID filter")
    command_type: Optional[str] = Field(default=None, description="Command type filter")
    status: Optional[CommandStatus] = Field(default=None, description="Status filter")
    limit: int = Field(default=100, description="Maximum number of results")


# ============================================================================
# Validation Models
# ============================================================================

class ValidationResult(BaseModel):
    """Result of input validation."""
    valid: bool = Field(..., description="Whether input is valid")
    error_message: Optional[str] = Field(default=None, description="Error message if invalid")
    sanitized_value: Optional[str] = Field(default=None, description="Sanitized input value")


# ============================================================================
# Command Schema Models
# ============================================================================

class CommandSchema(BaseModel):
    """Schema definition for a command type."""
    command_type: str = Field(..., description="Command type identifier")
    description: str = Field(..., description="Command description")
    parameters: Dict[str, Any] = Field(..., description="Parameter schema")
    required_permissions: List[Permission] = Field(..., description="Required permissions")
    example: Dict[str, Any] = Field(..., description="Example usage")


class CommandSchemaResponse(BaseModel):
    """Response containing command schemas."""
    schemas: Dict[str, CommandSchema] = Field(..., description="Command schemas by type")
    version: str = Field(default="1.0", description="Schema version")

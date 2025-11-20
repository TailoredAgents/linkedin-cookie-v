import logging
import uuid
from enum import Enum
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class AuditEventType(Enum):
    """Minimal audit event types used by the verifier."""

    AUTHENTICATION = "authentication"


class AuditSeverity(Enum):
    """Severity levels for audit events."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class _AuditLogger:
    """Lightweight async logger used to stub the monorepo audit service."""

    async def log_event(
        self,
        *,
        event_type: Optional[AuditEventType] = None,
        actor_type: Optional[str] = None,
        actor_id: Optional[str] = None,
        target_type: Optional[str] = None,
        target_id: Optional[str] = None,
        organization_id: Optional[Any] = None,
        details: Optional[Dict[str, Any]] = None,
        severity: AuditSeverity = AuditSeverity.INFO,
        **_: Any,
    ) -> str:
        """Record an audit event to the application logger."""
        log_details = {
            "event_type": event_type.value if event_type else None,
            "actor_type": actor_type,
            "actor_id": actor_id,
            "target_type": target_type,
            "target_id": target_id,
            "organization_id": organization_id,
            "details": details or {},
            "severity": severity.value if isinstance(severity, AuditSeverity) else str(severity),
        }
        logger.info("AUDIT_EVENT %s", log_details)
        return str(uuid.uuid4())


# Instance used by the verifier module
audit_logger = _AuditLogger()


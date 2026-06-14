"""Error types for persistence operations."""

from __future__ import annotations


class PersistenceError(Exception):
    """Base class for persistence-layer failures."""


class BackendConfigurationError(PersistenceError, ValueError):
    """Raised when a persistence backend is not configured correctly."""


class PersistenceCorruptionError(PersistenceError):
    """Raised when a persistence artifact appears corrupt."""


class PersistenceBackupError(PersistenceError):
    """Raised when backup or restore operations fail."""

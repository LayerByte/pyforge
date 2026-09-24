class PyForgeError(Exception):
    """Base exception for user-facing toolkit failures."""


class ValidationError(PyForgeError):
    """Raised when a utility receives invalid input."""


class ToolExecutionError(PyForgeError):
    """Raised when a utility cannot complete an external operation."""

from typing import List, Optional


class ApplicationException(Exception):
    """Base class for application exceptions"""
    pass


class ApiException(ApplicationException):
    """Exception thrown from endpoint errors"""

    DEFAULT_EXCEPTION_CODE = 400

    def __init__(self, error_message: str, code: Optional[int] = None, errors: Optional[List] = None):
        self.status = error_message
        self.errors = errors or [{"message": error_message}]
        self.code = code or self.DEFAULT_EXCEPTION_CODE


class EntityNotFoundException(ApplicationException):
    """Base class for not found exceptions."""
    pass


class DomainException(ApplicationException):
    """Base class for domain exceptions"""
    pass


class ModelException(ApplicationException):
    """Base exception for errors while trying to load models"""
    pass

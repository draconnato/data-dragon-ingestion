"""Exceptions for data dragon ingestion errors."""


class BronzeRequiredFieldsError(Exception):
    """Raised when required fields are missing during Bronze ingestion initialization."""

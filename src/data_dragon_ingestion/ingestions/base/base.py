"""Base classes and abstract interfaces for Bronze layer data ingestion.

This module defines the abstract base class for implementing Bronze layer
ingestion processes in the data pipeline.
"""
from abc import ABCMeta, abstractmethod
from typing import Any

from data_dragon_ingestion.errors.ingestion import BronzeRequiredFieldsError


class BronzeMetaclass(ABCMeta):
    """Metaclass that automatically validates required fields after instance creation."""

    def __call__(cls, *args: str, **kwargs: str) -> type:
        """Create instance and validate required fields.

        Args:
            *args: Positional arguments passed to __init__.
            **kwargs: Keyword arguments passed to __init__.

        Returns:
            The newly created instance.

        Raises:
            BronzeRequiredFieldsError: If validation fails.
        """
        instance = super().__call__(*args, **kwargs)
        instance.check_required_fields()
        return instance


class BronzeBaseIngestion(metaclass=BronzeMetaclass):
    """Abstract base class for Bronze layer data ingestion.

    Defines the interface for implementing ingestion processes that extract
    raw data from external sources and store it in the Bronze layer of the
    data warehouse.

    Attributes:
        ingestion_timestamp: The timestamp when the ingestion process started.
        endpoint: The source endpoint from which data is being ingested.
    """
    ingestion_timestamp: str

    def check_required_fields(self) -> None:
        """Validate that required fields exist.

        Raises:
            BronzeRequiredFieldsError: If ingestion_timestamp or endpoint is None
                or empty.
        """
        fields = ["ingestion_timestamp", "endpoint"]

        for field in fields:
            if not hasattr(self, field) or getattr(self, field) is None or getattr(self, field) == "":
                raise BronzeRequiredFieldsError("Ingestion timestamp and Endpoint fields are mandatory.")

    @abstractmethod
    def run_ingestion(self) -> None:
        """Execute the data ingestion process.

        This method should implement the core logic for extracting data from
        the source endpoint and storing it in the Bronze layer.
        """

    def add_ingestion_watermark(self, payload_respose: dict[str, Any]) -> dict[str, Any]:
        """Add ingestion timestamp watermark to the payload.

        Args:
            payload_respose: The JSON payload dictionary to be enriched.

        Returns:
            dict: The payload with the 'timestamp' field added.
        """
        return {
            "response": payload_respose,
            "timestamp": self.ingestion_timestamp
        }

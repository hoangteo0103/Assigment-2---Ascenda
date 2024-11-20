import requests
from abc import ABC, abstractmethod
from config.config import SUPPLIER_CONFIG, AMENITIES_CONFIG
from .parser import *
from typing import List
from ..models.hotel import Hotel

class BaseSupplier(ABC):
    supplier_key = None  # Subclass must define this

    def endpoint(self) -> str:
        """Return the supplier's endpoint from the config."""
        return SUPPLIER_CONFIG[self.supplier_key]["endpoint"]

    def fetch(self) -> List[Hotel]:
        """Fetch data from the supplier's endpoint and parse it."""
        response = requests.get(self.endpoint())
        response.raise_for_status()
        raw_data = response.json()
        return [self.parse(dto) for dto in raw_data]

    def parse(self, dto) -> Hotel:
        """Parse a single data object using the supplier's configuration."""
        config = SUPPLIER_CONFIG[self.supplier_key]["fields"]

        # Parse fields using the Parser
        parsed_data = Parser.parse(dto, config)

        # Group nested fields dynamically
        grouped_data = self._group_nested_fields(parsed_data)

        # Parse amenities
        grouped_data["amenities"] = Parser.parse_amenities(grouped_data["amenities"], AMENITIES_CONFIG)

        # Create and return the Hotel object
        return Hotel(**grouped_data)

    def _group_nested_fields(self, flat_data: dict, sep: str = ".") -> dict:
        """
        Convert flattened keys into nested dictionaries.

        Args:
        - flat_data: A dictionary with flattened keys (e.g., "location.lat").
        - sep: The separator used in flattened keys (default is ".").

        Returns:
        - A nested dictionary.
        """
        nested_data = {}
        for key, value in flat_data.items():
            keys = key.split(sep)
            d = nested_data
            for part in keys[:-1]:
                d = d.setdefault(part, {})
            d[keys[-1]] = value
        return nested_data



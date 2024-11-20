import requests
from abc import ABC, abstractmethod
from config.config import SUPPLIER_CONFIG
from ..utils import *
from typing import List
from ..models.hotel import Hotel

class BaseSupplier(ABC):
    supplier_key = None  # Set in subclass

    def endpoint(self) -> str:
        """Return the endpoint URL from configuration."""
        return SUPPLIER_CONFIG[self.supplier_key]['endpoint']

    def fetch(self) -> List[Hotel]:
        """Fetch data from the endpoint and parse it."""
        response = requests.get(self.endpoint())
        response.raise_for_status()  # Handle possible HTTP errors
        return [self.parse(dto) for dto in response.json()]

    def parse(self, dto) -> Hotel:
        """Generic parse method using configurations."""
        config = SUPPLIER_CONFIG[self.supplier_key]['fields']
        
        # Parse location and amenities using helper functions
        location = parse_generic_field(dto, config['location'])
        amenities = parse_amenities(dto.get(config['amenities'], {}))

        # Handle images, checking for existence in DTO
        image_data = dto.get('images', {})
        images = parse_images(image_data, config['images'])

        # Safely handle and strip description or use an empty string if None
        description = (dto.get(config['description']) or '').strip()

        return Hotel(
            id=dto[config['id']],
            destination_id=int(dto[config['destination_id']]),
            name=dto[config['name']],
            description=description,
            location=location,
            amenities=amenities,
            images=images,
            booking_conditions=dto.get('booking_conditions', [])
        )

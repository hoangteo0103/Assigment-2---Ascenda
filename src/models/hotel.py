# models/hotel.py
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Location:
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    postal_code: Optional[str] = None

@dataclass
class Amenities:
    general: List[str] = field(default_factory=list)
    room: List[str] = field(default_factory=list)
    
@dataclass
class Image:
    link: str
    description: str

@dataclass
class ImageCategory:
    rooms: List[Image] = field(default_factory=list)
    site: List[Image] = field(default_factory=list)
    amenities: List[Image] = field(default_factory=list)

@dataclass
class Hotel:
    id: str
    destination_id: int
    name: str
    description: str
    location: Location
    amenities: Amenities
    images: ImageCategory
    booking_conditions: Optional[List[str]] = field(default_factory=list)

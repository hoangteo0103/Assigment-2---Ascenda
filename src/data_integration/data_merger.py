from typing import List, Dict
from ..models.hotel import Hotel, Image, Amenities

class DataMerger:
    def merge_hotels(self, hotel_data: List[Hotel]) -> List[Hotel]:
        """Consolidate hotel data from multiple sources into the most comprehensive entries possible."""
        merged_hotels = {}
        for hotel in hotel_data:
            if hotel.id not in merged_hotels:
                merged_hotels[hotel.id] = hotel
            else:
                merged_hotels[hotel.id] = self.merge_two_hotels(merged_hotels[hotel.id], hotel)
        return list(merged_hotels.values())

    def merge_two_hotels(self, existing: Hotel, new: Hotel) -> Hotel:
        """Merge two hotel records into a single, more comprehensive record."""
        # Use a comprehensive method to merge each field thoughtfully.

        existing.name = self.get_preferable_value(existing.name, new.name)
        existing.description = self.concatenate_descriptions(existing.description, new.description)
        existing.location = self.merge_locations(existing.location, new.location)
        existing.amenities = self.merge_amenities(existing.amenities, new.amenities)
        existing.images.rooms = self.merge_images(existing.images.rooms, new.images.rooms)
        existing.images.site = self.merge_images(existing.images.site, new.images.site)
        existing.images.amenities = self.merge_images(existing.images.amenities, new.images.amenities)
        existing.booking_conditions = self.merge_lists_unique(existing.booking_conditions, new.booking_conditions)
        return existing

    def get_preferable_value(self, val1, val2):
        """Return the more preferable of two values, handling different data types appropriately."""
        if isinstance(val1, str) and isinstance(val2, str):
            # Prefer the longer string, or either if lengths are equal
            return val1 if len(val1) >= len(val2) else val2
        elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            # For numerical values, prefer the larger one
            return val1 if val1 >= val2 else val2
        else:
            # Return the first non-None value
            return val1 if val1 is not None else val2

    def concatenate_descriptions(self, desc1, desc2):
        """Concatenate two descriptions, ensuring they are separated by a newline if both are non-empty."""
        if not desc1.strip():
            return desc2.strip()
        if not desc2.strip():
            return desc1.strip()
        return f"{desc1.strip()} {desc2.strip()}"

    def merge_locations(self, loc1, loc2):
        """Merge two location dictionaries, preferring non-null and more detailed attributes."""
        merged_location = {}
        attributes = ['address', 'city', 'country', 'lat', 'lng', 'postal_code']
        for attribute in attributes:
            # Use a helper function or direct comparison to choose the best value
            value1 = loc1.get(attribute, '')
            value2 = loc2.get(attribute, '')
            merged_location[attribute] = self.get_preferable_value(value1, value2)
        return merged_location

    def merge_amenities(self, amenities1: Amenities, amenities2: Amenities) -> Amenities:
        """Merge two Amenities instances, combining and deduplicating their lists."""

        combined_general = list(set(amenities1.general + amenities2.general))
        combined_room = list(set(amenities1.room + amenities2.room))
        return Amenities(general=combined_general, room=combined_room)

    def merge_lists_unique(self, list1: List, list2: List) -> List:
        """Merge two lists, removing duplicate entries."""
        return list(set(list1 + list2))

    def merge_images(self, images1: List[Image], images2: List[Image]) -> List[Image]:
        """Merge two lists of images, removing duplicates based on image link."""
        unique_links = set()
        merged_images = []
        for image in images1 + images2:
            if image.link not in unique_links:
                unique_links.add(image.link)
                merged_images.append(image)
        return merged_images


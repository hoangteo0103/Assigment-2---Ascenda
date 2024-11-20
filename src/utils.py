from .models.hotel import Image, ImageCategory, Amenities
from typing import List, Dict
from config.config import GENERAL_AMENITIES, ROOM_AMENITIES

def parse_amenities(amenities):
    """
    Parses a list of amenities into a structured object with general and room amenities.
    """

    categorized = Amenities()
    if isinstance(amenities, list):
        for item in amenities:
            item_clean = item.lower().strip()
            if any(keyword in item_clean for keyword in GENERAL_AMENITIES):
                categorized.general.append(item_clean)
            if any(keyword in item_clean for keyword in ROOM_AMENITIES):
                categorized.room.append(item_clean)
    elif isinstance(amenities, dict):
        for key, items in amenities.items():
            for item in items:
                item_clean = item.lower().strip()
                if key == 'general' and any(keyword in item_clean for keyword in GENERAL_AMENITIES):
                    categorized.general.append(item_clean)
                elif key == 'room' and any(keyword in item_clean for keyword in ROOM_AMENITIES):
                    categorized.room.append(item_clean)

    # Convert sets to sorted lists to ensure consistency and remove duplicates
    categorized.general = sorted(categorized.general)
    categorized.room = sorted(categorized.room)
    return categorized


def parse_generic_field(data, field_config):
    """
    Parses fields from the data based on a given field configuration.
    Handles nested fields and returns a structured object based on the config.

    Args:
        data (dict): The source data dictionary from which to extract values.
        field_config (dict or str): The configuration for extracting the field.
            This can be a simple string pointing to a direct field or a dictionary
            describing paths to fields or transformations needed.

    Returns:
        dict or object: The parsed data structured according to the field_config.
    """
    if isinstance(field_config, str):
        # Direct field access
        return data.get(field_config)

    if isinstance(field_config, dict):
        # Complex structure with potential nested fields
        result = {}
        for key, path in field_config.items():
            if isinstance(path, str):
                # Simple path, directly accessible
                result[key] = get_from_path(data, path.split('.'))
            elif isinstance(path, dict):
                # Nested structure or need for more complex processing
                result[key] = parse_generic_field(data, path)
        return result

    return None

def get_from_path(data, path):
    """
    Helper function to navigate through a nested dictionary using a list of keys.

    Args:
        data (dict): The dictionary to navigate.
        path (list of str): The path through the dictionary as a list of keys.

    Returns:
        The value found at the path, or None if the path does not exist.
    """
    for key in path:
        if data and key in data:
            data = data[key]
        else:
            return None
    return data

def parse_images(image_data, config):
    """Parse image data from a dictionary using a configuration dictionary."""
    images = ImageCategory()
    for category, details in config.items():
        image_list = []
        if details['key'] in image_data:
            for img in image_data[details['key']]:
                image_list.append(Image(
                    link=img[details['url_field']],
                    description=img.get(details['desc_field'], 'No description')
                ))
        setattr(images, category, image_list)
    return images
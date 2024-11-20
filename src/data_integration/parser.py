class Parser:
    @staticmethod
    def parse(dto: dict, config: dict) -> dict:
        """
        Parse raw JSON data using the flattened configuration.

        Args:
        - dto: The raw data from the supplier.
        - config: The flattened configuration for the supplier.

        Returns:
        - A dictionary representing the parsed data.
        """
        parsed_data = {}

        for field, rules in config.items():
            parsed_data[field] = Parser._parse_field(dto, rules)

        return parsed_data

    @staticmethod
    def _parse_field(dto: dict, rules: dict):
        """
        Parse a single field based on its rules.

        Args:
        - dto: The raw data from the supplier.
        - rules: Field rules from the configuration.

        Returns:
        - The parsed field value.
        """
        # Retrieve the source value using dot notation
        value = Parser.get_nested_value(dto, rules["source"]) if rules["source"] else None

        # Apply default if the value is None
        if value is None and "default" in rules:
            value = rules["default"]

        # Apply type transformations
        if "type" in rules and value is not None:
            value = Parser._transform_value(value, rules["type"])

        # Handle structured fields (e.g., images with subfields)
        if "fields" in rules and isinstance(value, list):
            value = [
                {sub_field: item.get(sub_source, "")
                 for sub_field, sub_source in rules["fields"].items()}
                for item in value
            ]

        return value

    @staticmethod
    def get_nested_value(data: dict, path: str, sep: str = ".") -> any:
        """
        Retrieve a nested value from a dictionary using dot-separated keys.

        Args:
        - data: The dictionary to retrieve the value from.
        - path: The dot-separated path to the value.
        - sep: The separator for nested keys (default is ".").

        Returns:
        - The value at the specified path, or None if not found.
        """
        keys = path.split(sep)
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key)
            else:
                return None
        return data

    @staticmethod
    def _transform_value(value: any, value_type: str) -> any:
        """
        Transform the value to the specified type.

        Args:
        - value: The value to transform.
        - value_type: The target type (e.g., "integer", "float", "list", etc.).

        Returns:
        - The transformed value.
        """
        try:
            if value_type == "integer":
                return int(value)
            elif value_type == "float":
                return float(value)
            elif value_type == "string":
                return str(value)
            elif value_type == "list" and not isinstance(value, list):
                return [value]
        except (ValueError, TypeError):
            return None
        return value

    @staticmethod
    def parse_amenities(amenities_dict: dict, config: dict) -> dict:
        """
        Categorize amenities into 'general' and 'room', using a set for matching.

        Args:
        - amenities_dict: A dictionary containing 'general' and 'room' amenities.
        - config: Configuration defining 'general' and 'room' amenities.

        Returns:
        - A dictionary with categorized amenities.
        """
        categorized_amenities = {"general": [], "room": []}

        # Combine all amenities from input
        amenities = amenities_dict.get("general", []) + amenities_dict.get("room", [])

        # Create sets for normalized general and room amenities
        general_set = {g.replace(" ", "").lower() for g in config["general"]}
        room_set = {r.replace(" ", "").lower() for r in config["room"]}

        for amenity in amenities:
            # Normalize the amenity (remove spaces, lowercase)
            normalized = amenity.replace(" ", "").lower()

            if normalized in general_set:
                # Use the readable version from config
                readable = next(g for g in config["general"] if g.replace(" ", "").lower() == normalized)
                categorized_amenities["general"].append(readable)
            elif normalized in room_set:
                # Use the readable version from config
                readable = next(r for r in config["room"] if r.replace(" ", "").lower() == normalized)
                categorized_amenities["room"].append(readable)
            else:
                # Default to general category
                categorized_amenities["general"].append(amenity)

        return categorized_amenities


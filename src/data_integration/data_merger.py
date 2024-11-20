import json
from typing import List, Dict, Any
from ..models.hotel import Hotel, Image, Amenities


class DataMerger:
    def __init__(self, config_path: str = "config/merge_strategy.json"):
        # Load merge strategies from the configuration file
        with open(config_path, "r") as file:
            self.merge_strategy = json.load(file)["fields"]

    def merge_hotels(self, hotel_data: List[Hotel]) -> List[Hotel]:
        """Merge hotel data from multiple sources into comprehensive entries."""
        merged_hotels = {}
        for hotel in hotel_data:
            if hotel.id not in merged_hotels:
                merged_hotels[hotel.id] = hotel
            else:
                merged_hotels[hotel.id] = self._merge_two_hotels(merged_hotels[hotel.id], hotel)
        return list(merged_hotels.values())

    def _merge_two_hotels(self, existing: Hotel, new: Hotel) -> Hotel:
        """Merge two hotel records based on defined strategies."""
        for field, strategy_config in self.merge_strategy.items():
            strategy = strategy_config.get("strategy", "default_merge")
            merge_function = getattr(self, strategy, self._default_merge)
            key = strategy_config.get("key", None)
            subfield_strategies = strategy_config.get("subfield_strategies", {})
            # Retrieve existing and new field values
            existing_value = self._get_nested_field(existing, field)
            new_value = self._get_nested_field(new, field)
            # Merge the values
            merged_value = merge_function(existing_value, new_value, key, subfield_strategies)
            self._set_nested_field(existing, field, merged_value)
        return existing

    # ===============================
    # Merge Strategies
    # ===============================

    def _default_merge(self, val1, val2, *args, **kwargs):
        """Default merge strategy: choose the first non-null value."""
        return val1 if val1 is not None else val2
    
    def first_non_null(self, val1, val2, *args, **kwargs):
        """Choose the first non-null value."""
        return val1 if val1 is not None else val2

    def choose_best(self, val1, val2, *args, **kwargs):
        """Choose the better value based on predefined criteria."""
        if isinstance(val1, str) and isinstance(val2, str):
            return val1 if len(val1) >= len(val2) else val2
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            return max(val1, val2)
        return val1 if val1 is not None else val2

    def concatenate(self, val1, val2, *args, **kwargs):
        """Concatenate two strings if they are different."""
        if not val1:
            return val2
        if not val2:
            return val1
        val1, val2 = val1.strip(), val2.strip()
        if val2 in val1:
            return val1
        if val1 in val2:
            return val2
        return f"{val1} {val2}"

    def merge_list(self, list1: List[Any], list2: List[Any], key: str = None, subfield_strategies: Dict[str, str] = None):
        """Merge two lists, deduplicating by a key and applying subfield strategies."""
        if not list1:
            return list2 or []
        if not list2:
            return list1 or []

        if key:  # Deduplicate based on a key field
            combined = {}
            for item in list1 + list2:
                item_key = item.get(key) if isinstance(item, dict) else item
                if item_key in combined:
                    # Merge subfields if applicable
                    for subfield, strategy in (subfield_strategies or {}).items():
                        existing_value = combined[item_key].get(subfield, "")
                        new_value = item.get(subfield, "")
                        combined[item_key][subfield] = self._apply_strategy(existing_value, new_value, strategy)
                else:
                    combined[item_key] = item
            return list(combined.values())

        # Default behavior for non-dictionary lists
        return list(set(list1 + list2))

    # ===============================
    # Helper Methods
    # ===============================

    def _apply_strategy(self, val1: Any, val2: Any, strategy: str) -> Any:
        """Apply a strategy dynamically to two values."""
        strategy_function = getattr(self, strategy, self._default_merge)
        return strategy_function(val1, val2)

    def _get_nested_field(self, obj: Any, field: str) -> Any:
        """Retrieve the value of a nested field using dot notation."""
        keys = field.split(".")
        for key in keys:
            if isinstance(obj, dict):
                obj = obj.get(key)
            elif hasattr(obj, key):
                obj = getattr(obj, key)
            else:
                return None
        return obj

    def _set_nested_field(self, obj: Any, field: str, value: Any):
        """Set the value of a nested field using dot notation."""
        keys = field.split(".")
        for key in keys[:-1]:
            if isinstance(obj, dict):
                obj = obj.setdefault(key, {})
            elif hasattr(obj, key):
                obj = getattr(obj, key)
            else:
                return
        if isinstance(obj, dict):
            obj[keys[-1]] = value
        elif hasattr(obj, keys[-1]):
            setattr(obj, keys[-1], value)

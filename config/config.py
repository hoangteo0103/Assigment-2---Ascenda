import json

def load_config(path):
    with open(path, 'r') as file:
        return json.load(file)

SUPPLIER_CONFIG = load_config('config/suppliers_config.json')
AMENITIES_CONFIG = load_config('config/amenities_config.json')
GENERAL_AMENITIES = AMENITIES_CONFIG['general']
ROOM_AMENITIES = AMENITIES_CONFIG['room']
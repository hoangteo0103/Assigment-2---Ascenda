import argparse
from src.data_integration.acme_supplier import AcmeSupplier
from src.data_integration.patagonia_supplier import PatagoniaSupplier
from src.data_integration.paperflies_supplier import PaperfliesSupplier
from src.data_integration.supplier_manager import SupplierManager
import json
from dataclasses import asdict

def fetch_hotels(hotel_ids, destination_ids):
    # Setup suppliers
    suppliers = [AcmeSupplier(), PatagoniaSupplier(), PaperfliesSupplier()]
    manager = SupplierManager(suppliers)

    # Fetch, merge, and filter data from all suppliers
    merged_hotels = manager.fetch_and_merge_data()
    hotel_ids = hotel_ids.split(',') if (hotel_ids and hotel_ids != "none")  else []
    destination_ids = destination_ids.split(',') if (destination_ids and destination_ids != "none") else []
    filtered_hotels = manager.filter_hotels(merged_hotels, hotel_ids, destination_ids)

    # Convert filtered hotels to JSON
    dict_result = [asdict(hotel) for hotel in filtered_hotels]
    json_output = json.dumps(dict_result, indent=2)

    with open("output.json", "w") as f:
        f.write(json_output)
    print(json_output)

def main():
    parser = argparse.ArgumentParser(description="Hotel Data Merger")
    parser.add_argument("hotel_ids", type=str, help="Comma-separated hotel IDs", default="")
    parser.add_argument("destination_ids", type=str, help="Comma-separated destination IDs", default="")
    args = parser.parse_args()

    fetch_hotels(args.hotel_ids, args.destination_ids)

if __name__ == "__main__":
    main()

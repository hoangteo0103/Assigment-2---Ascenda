from typing import List, Optional
from .base_supplier import BaseSupplier
from .data_merger import DataMerger
from ..models.hotel import Hotel


class SupplierManager:
    def __init__(self, suppliers: List[BaseSupplier]):
        self.suppliers = suppliers
        self.merger = DataMerger()

    def fetch_and_merge_data(self) -> List[Hotel]:
        all_hotels = []
        for supplier in self.suppliers:
            all_hotels.extend(supplier.fetch())
        return self.merger.merge_hotels(all_hotels)

    def filter_hotels(self, hotels: List[Hotel], hotel_ids: Optional[List[str]], destination_ids: Optional[List[str]]) -> List[Hotel]:
        return [
            hotel for hotel in hotels
            if (not hotel_ids or hotel.id in hotel_ids) and
               (not destination_ids or str(hotel.destination_id) in destination_ids)
        ]


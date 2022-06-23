from collections import defaultdict
from typing import Dict, Tuple, List, Iterator


from api.product.repositories.base import AbstractRepository


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.storage_pk: Dict[Tuple[str, str], Dict] = {}
        self.storage_soft_key: Dict[Tuple[str, str], List[Dict]] = defaultdict(list)

    def get(self, product_code: str, product_type: str) -> dict:
        data = self.storage_pk[(product_code, product_type)]
        return data

    def get_all_by_code_and_type(self, product_code: str, product_type: str) -> Iterator[dict]:
        return self.storage_soft_key[(product_code, product_type)]

    def get_all(self):
        return self.storage_pk.values()

    def put(self, product_code: str, product_type: str, data: dict):
        key = (product_code, product_type)
        self.storage_pk[key] = data
        stripped_key = (product_code.lstrip("0"), product_type)
        self.storage_soft_key[stripped_key].append(data)

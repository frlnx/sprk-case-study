from collections import defaultdict
from functools import reduce
from typing import List, Iterable

from injector import inject

from api.product.models import ProductModel
from api.product.repositories.base import AbstractRepository


class ProductService:

    @inject
    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository

    def get(self, product_code, product_type) -> ProductModel:
        """
        Get the product with exactly this product code and type
        :param product_code: May have leading zeroes.
        :param product_type:
        :return: ProductModel
        """
        try:
            data = self.repository.get(product_code, product_type)
        except KeyError:
            raise KeyNotFound
        data = self.data_migrations(data)
        return ProductModel(data['amount'], product_code, product_type, data)

    def get_aggregated(self, product_code, product_type) -> ProductModel:
        """
        Get the product with this product code and type. Leading zeros are ignored
        :param product_code: Leading zeros will lead to nothing being returned
        :param product_type:
        :return: ProductModel
        """
        return self._deduplicate(self.repository.get_all_by_code_and_type(product_code, product_type))

    def get_all(self) -> List[ProductModel]:
        """
        Fetches all data in an aggregated form
        :return: List[ProductModel]
        """
        mapped = defaultdict(list)
        for data in self.repository.get_all():
            mapped[(data['item']['code'].lstrip("0"), data['item'].get('type', ''))].append(data)
        return list(map(self._deduplicate, mapped.values()))

    def put(self, product_code, product_type, product: ProductModel) -> None:
        self.repository.put(product_code, product_type, product.data)

    def data_migrations(self, data):
        """
        On the fly migrations that should be run every time product data is fetched.
        :param data: Raw data dict
        :return: migrated data dict
        """
        data['item']['code'] = data['item']['code'].lstrip('0')
        if 'trade_item_descriptor' in data['item']:
            data['item']['trade_item_unit_descriptor'] = data['item']['trade_item_descriptor']
            del data['item']['trade_item_descriptor']
        return data

    def aggregate(self, a: dict, b: dict) -> dict:
        """
        Reduction function that merges values from b into a, and takes care that values in
        b that are None does not overwrite.

        Also runs data migrations
        :param a: primary dict
        :param b: new dict
        :return: merged dict
        """
        if not b:
            return a
        b['amount'] = b['amount'] + a.get('amount', 0)
        empty_keys = []
        for key in b.keys():
            if b[key] is None and key in a:
                empty_keys.append(key)
        for key_to_remove in empty_keys:
            del b[key_to_remove]
        a.update(b)
        return a

    def _deduplicate(self, duplicates: Iterable[dict]) -> ProductModel:
        """
        Reduces a list of dicts into a ProductModel
        :param duplicates: A list of dicts with product model data
        :return: the reduced product model
        """
        data = reduce(self.aggregate, duplicates)
        data = self.data_migrations(data)
        return ProductModel(data['amount'], data['item']['code'], data['item'].get('type', ""), data)


class KeyNotFound(BaseException):
    pass

from typing import Dict, List, Any

from api.dependency_injection import injector
from api.serializers import serialize_product_model, deserialize_product_model
from api.product.service import ProductService


class SprkApi:
    storage: ProductService
    def __init__(self):
        self.service = injector.get(ProductService)

    def load_data(self, objects: List[Dict[str, Any]]) -> None:
        """
        Ingests data and saves to the storage
        :param objects: a list of objects that looks like products
        :return: None
        """
        products = []
        for data in objects:
            product = deserialize_product_model(data)
            products.append(product)
        for product in products:
            self.service.put(product.code, product.type, product)

    def list_data(self) -> List[Dict[str, Any]]:
        """
        Fetches all data from the data storage and returns them as a list of objects
        :return: a list of dict representations of a products
        """
        products = self.service.get_all()
        serialized_data = []
        for product in products:
            serialized_data.append(serialize_product_model(product))
        return serialized_data

    def get_product(self, product_code, product_type) -> Dict[str, Any]:
        """
        Gets a product based on its product code and type
        :param product_code: str
        :param product_type: str
        :return: a dict representation of a product
        """
        product = self.service.get_aggregated(product_code, product_type)
        serialized_data = serialize_product_model(product)
        return serialized_data

    def get_original_product(self, product_code, product_type) -> Dict[str, Any]:
        """
        Products that were ingested with 0s before their code are saved as is. This method lets you access original data
        :param product_code: a code with leading zeros
        :param product_type: the product type
        :return: a dict representation of a product
        """
        product = self.service.get(product_code, product_type)
        serialized_data = serialize_product_model(product)
        return serialized_data

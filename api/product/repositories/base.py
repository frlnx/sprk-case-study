from collections import Iterator


class AbstractRepository:

    def get(self, product_code: str, product_type: str) -> dict:
        """Get a product as a dict from the repository based on its code and type. Zero padded versions are aggregated
        and a single object is returned"""
        raise NotImplementedError()

    def get_all_by_code_and_type(self, product_code: str, product_type: str) -> Iterator[dict]:
        """Get a list of products based on their product code and type. Zero padded codes are also returned"""
        raise NotImplementedError()

    def get_all(self):
        """Returns all products in the repository"""
        raise NotImplementedError()

    def put(self, product_code: str, product_type: str, data: dict):
        """Puts a product into the repository or updates an existing one."""
        raise NotImplementedError()

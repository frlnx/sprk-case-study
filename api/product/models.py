import dataclasses


@dataclasses.dataclass
class ProductModel:
    """
    A primitive yet efficient representation of a product, for internal use only.
    """
    amount: int
    code: str
    type: str
    data: dict

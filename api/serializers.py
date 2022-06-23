from api.product.models import ProductModel


def serialize_product_model(product: ProductModel):
    return product.data

def deserialize_product_model(data: dict):
    try:
        product = ProductModel(data['amount'], data['item']['code'], data['item'].get('type', ''), data)
    except KeyError:
        print(data['item']['code'])
        raise
    return product

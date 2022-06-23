from api.product.models import ProductModel


class ItemDataFactory:
    def __call__(self, amount=None, product_code=None, product_type=None, data=None, item_data=None, **kwargs):
        base_data = {
            "amount": amount,
            "bbd": None,
            "comment": "",
            "country_of_disassembly": None,
            "country_of_rearing": None,
            "country_of_slaughter": None,
            "cutting_plant_registration": None,
            "item": {
                "amount_multiplier": 0,
                "brand": "Missing brand",
                "categ_id": 266,
                "category_id": "10006014",
                "code": product_code,
                "description": "Gurke - Alle - Mini",
                "edeka_article_number": False,
                "gross_weight": 1,
                "id": "5084",
                "net_weight": 1,
                "notes": False,
                "packaging": "NE",
                "related_products": [

                ],
                "requires_best_before_date": False,
                "requires_meat_info": False,
                "trade_item_unit_descriptor": "BASE_UNIT_OR_EACH",
                "trade_item_unit_descriptor_name": "Basiseinheit",
                "type": product_type,
                "unit_name": "kg",
                "validation_status": "validated"
            },
            "lot_number": None,
            "slaughterhouse_registration": None
        }
        if data:
            base_data.update(data)
        data = base_data
        if item_data:
            data['item'].update(item_data)
        return data

class ProductModelFactory:
    """
    Create a Product Model that looks correct
    """
    def __call__(self, amount=None, product_code=None, product_type=None, data=None, item_data=None):
        if not amount:
            amount = 13
        if not product_code:
            product_code = "168"
        if not product_type:
            product_type = "whitelisted_plu"
        data = ItemDataFactory()(
            amount=amount,
            product_code=product_code,
            product_type=product_type,
            data=data,
            item_data=item_data
        )
        return ProductModel(amount, product_code, product_type, data)

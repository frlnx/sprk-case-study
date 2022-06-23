import pytest

from api.dependency_injection import injector
from api.product.service import ProductService, KeyNotFound
from tests.factories import ProductModelFactory


class TestProductServices:

    def test_get_nonexistent_fails(self):
        target = injector.get(ProductService)
        with pytest.raises(KeyNotFound):
            target.get("Not There", "My Type")
        assert True

    def test_put_nonexistent_works(self):
        target =  injector.get(ProductService)
        product = ProductModelFactory()()
        target.put(product.code, product.type, product)
        actual = target.get(product.code, product.type)
        assert actual == product

    def test_put_existent_works(self):
        target =  injector.get(ProductService)
        product = ProductModelFactory()()
        target.put(product.code, product.type, product)
        target.put(product.code, product.type, product)
        actual = target.get(product.code, product.type)
        assert actual == product

    def test_put_existent_with_zeroed_key_works(self):
        target =  injector.get(ProductService)
        factory = ProductModelFactory()
        product = factory(amount=1, product_code="test_put_existent_with_zeroed_key_works")
        target.put(product.code, product.type, product)
        product_with_zeros = factory(amount=1, product_code=f"0000{product.code}")
        target.put(product_with_zeros.code, product_with_zeros.type, product_with_zeros)
        actual = target.get_aggregated(product.code, product.type)
        expected = factory(amount=2, product_code=product.code)
        assert actual.amount == 2
        assert actual.code == expected.code
        assert actual.type == expected.type
        for key in actual.data.keys():
            assert actual.data[key] == expected.data[key]
        assert actual.data['item'] == expected.data['item']
        assert actual.data == expected.data
        assert actual == expected

    def test_trade_item_descriptor_migration(self):
        target =  injector.get(ProductService)
        factory = ProductModelFactory()
        product = factory(
            item_data={"trade_item_descriptor": "FOOBAR"},
            product_code="test_trade_item_descriptor_migration"
        )
        target.put(product.code, product.type, product)
        actual = target.get(product.code, product.type)
        assert 'trade_item_descriptor' not in actual.data['item']
        assert 'trade_item_unit_descriptor' in actual.data['item']
        assert actual.data['item']['trade_item_unit_descriptor'] == "FOOBAR"

    def test_get_all_unique(self):
        target =  injector.get(ProductService)
        factory = ProductModelFactory()
        for product_code in map(lambda n: f"test_get_all_unique_{n}", range(1000, 1009)):
            product = factory(product_code=product_code)
            target.put(product.code, product.type, product)
        actual = target.get_all()
        actual = list(filter(lambda product: "test_get_all_unique_" in product.code, actual))
        assert len(actual) == 9

    def test_get_all_with_duplicates(self):
        target =  injector.get(ProductService)
        factory = ProductModelFactory()

        for product_code in map(lambda n: f"test_get_all_with_duplicates{n}", range(1000, 1009)):
            product = factory(product_code=product_code)
            target.put(product.code, product.type, product)
            duplicate_product = factory(product_code=f"00{product_code}")
            target.put(duplicate_product.code, duplicate_product.type, duplicate_product)

        actual = target.get_all()
        actual = list(filter(lambda product: "test_get_all_with_duplicates" in product.code, actual))
        assert len(actual) == 9

    def test_get_all_with_triplicates(self):
        target =  injector.get(ProductService)
        factory = ProductModelFactory()

        for product_code in map(lambda n: f"test_get_all_with_triplicates{n}", range(1000, 1009)):
            product = factory(product_code=product_code)
            target.put(product.code, product.type, product)
            duplicate_product = factory(product_code=f"00{product_code}")
            target.put(duplicate_product.code, duplicate_product.type, duplicate_product)
            triplicate_product = factory(product_code=f"000{product_code}")
            target.put(triplicate_product.code, triplicate_product.type, triplicate_product)

        actual = target.get_all()
        actual = list(filter(lambda product: "test_get_all_with_triplicates" in product.code, actual))
        assert len(actual) == 9

import json

from api.sprk_api import SprkApi


class TestIntegration:

    def setup(cls):
        with open('products.json', 'r') as f:
            data = json.load(f)
        assert len(data['amounts']) == 25
        cls.sprk_api = SprkApi()
        cls.sprk_api.load_data(data['amounts'])

    def test_deduplicating_data(self):
        returned_data = self.sprk_api.list_data()
        assert len(returned_data) == 22

    def test_field_renaming(self):
        returned_data = self.sprk_api.list_data()
        for data in returned_data:
            assert 'trade_item_descriptor' not in data['item']
            assert 'trade_item_unit_descriptor' in data['item']

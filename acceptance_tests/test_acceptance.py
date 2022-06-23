import json
import os

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

hostname = os.getenv('TARGET', 'localhost')

s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
s.mount('http://', HTTPAdapter(max_retries=retries))

def test_list():
    resp = s.get(f'http://{hostname}:5000/products/')
    assert resp.status_code == 200

def test_session():
    with open('products.json', 'r') as f:
        data = json.load(f)
    resp = s.post(f'http://{hostname}:5000/sessions/', json=data, headers={"mimetype": 'application/json'})
    assert resp.status_code == 201

    resp = s.get(f'http://{hostname}:5000/products/')
    assert resp.status_code == 200

    resp_data = resp.json()
    assert len(resp_data) == 22
    for row in resp_data:
        assert 'trade_item_descriptor' not in row['item']
        assert 'trade_item_unit_descriptor' in row['item']

    for row in resp_data:
        if "type" not in row["item"]:
            continue
        url = f'http://{hostname}:5000/products/type/{row["item"]["type"]}/code/{row["item"]["code"]}/'
        resp = s.get(url)
        assert resp.status_code == 200, url

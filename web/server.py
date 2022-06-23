import json

from flask import Flask, request, Response

from api.sprk_api import SprkApi


app = Flask(__name__)
api = SprkApi()

@app.route('/products/', methods=['GET'])
def products():
    """
    Lists all products available
    :return: a json encoded list of all products
    """
    data = api.list_data()
    return Response(json.dumps(data))

@app.route('/products/type/<product_type>/code/<product_code>/', methods=['GET'])
def get_product(product_type: str , product_code: str):
    """
    Gets a single product
    :param product_type:
    :param product_code:
    :return: a json encoded object of the product
    """
    data = api.get_product(product_code, product_type)
    return Response(json.dumps(data))

@app.route('/sessions/', methods=['POST'])
def post_session():
    """
    Ingests a session and saves it to the database
    :return: 201 with no content
    """
    api.load_data(request.json['amounts'])
    return Response("", status=201)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
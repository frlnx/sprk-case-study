from injector import Injector

from api.dependency_injection import configure_for_pytest
from api.product.service import ProductService

injector = Injector([configure_for_pytest, ProductService()])

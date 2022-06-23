from injector import Injector, singleton

from api.config import config
from api.product.provider import RepositoryProvider
from api.product.repositories.base import AbstractRepository
from api.product.repositories.memory import MemoryRepository
from api.product.repositories.postgresql import PostgresqlRepository
from api.product.service import ProductService


def configure_for_pytest(binder):
    repository = MemoryRepository()
    binder.bind(AbstractRepository, to=repository)

def configure_for_web(binder):
    repository = PostgresqlRepository(config=config)
    binder.bind(AbstractRepository, to=repository, scope=singleton)

if config.stage == "test":
    injector = Injector([configure_for_pytest, RepositoryProvider()])

if config.stage == "web":
    injector = Injector([configure_for_web, RepositoryProvider()])

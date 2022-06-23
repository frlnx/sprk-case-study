from injector import provider, singleton, Module

from api.config import Config
from api.product.repositories.base import AbstractRepository
from api.product.repositories.memory import MemoryRepository
from api.product.repositories.postgresql import PostgresqlRepository


class RepositoryProvider(Module):

    @singleton
    @provider
    def provide_repository(self, config: Config=None) -> AbstractRepository:
        """
        Part of the Service - Provider pattern. This method is not meant to be called directly.
        :param config:
        :return:
        """
        if not config.pg_hostname:
            return MemoryRepository()
        else:
            return PostgresqlRepository(config)

import dataclasses
import os

@dataclasses.dataclass
class Config:
    pg_hostname = os.getenv('POSTGRES_HOSTNAME')
    pg_username = os.getenv('POSTGRES_USERNAME')
    pg_password = os.getenv('POSTGRES_PASSWORD')
    pg_database = os.getenv('POSTGRES_DB')
    pg_port = os.getenv('POSTGRES_PORT')
    pg_scheme = os.getenv('POSTGRES_SCHEME')
    stage = os.getenv('stage', 'test')

config = Config()
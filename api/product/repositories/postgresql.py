import json
from collections import Iterator
from hashlib import sha256

import psycopg2.errors
from psycopg2 import connect, extras, Error
from psycopg2.errorcodes import UNIQUE_VIOLATION

from api.config import Config
from api.product.repositories.base import AbstractRepository


class PostgresqlRepository(AbstractRepository):

    cur: extras.DictCursor

    def __init__(self, config: Config):
        pg_connection_dict = {
            'user': config.pg_username,
            'password': config.pg_password,
            'port': config.pg_port,
            'host': config.pg_hostname
        }
        if config.pg_scheme:
            pg_connection_dict['options'] = f'-c search_path={config.pg_scheme}'

        connection = connect(**pg_connection_dict)
        self.cur: extras.DictCursor = connection.cursor(cursor_factory=extras.DictCursor)
        self.execute("SELECT current_database();")
        print(self.cur.fetchone())

    def execute(self, *args, **kwargs):
        self.cur.execute(*args, **kwargs)

    def get(self, product_code: str, product_type: str) -> dict:
        pk = self.make_pk(product_code, product_type)
        self.execute("""SELECT data FROM "product_record" WHERE pk=%s;""", (pk, ))
        return json.loads(self.cur.fetchone()['data'])

    def get_all_by_code_and_type(self, product_code: str, product_type: str) -> Iterator[dict]:
        self.execute("""SELECT data FROM "product_record" WHERE code=%s AND type=%s;""", (product_code, product_type))
        for row in self.cur:
            yield json.loads(row['data'])

    def get_all(self):
        self.execute("""SELECT data FROM "product_record";""")
        for row in self.cur:
            yield json.loads(row['data'])

    def put(self, product_code: str, product_type: str, data: dict):
        pk = self.make_pk(product_code, product_type)
        product_code = product_code.lstrip("0")
        data_str = json.dumps(data)
        try:
            self.execute(
                """INSERT INTO "product_record" (pk, code, type, data) VALUES (%s, %s, %s, %s);""",
                (pk, product_code, product_type, data_str)
            )
            self.cur.connection.commit()
        except psycopg2.errors.lookup(UNIQUE_VIOLATION):
            self.cur.connection.rollback()
            self.execute(
                """UPDATE "product_record" SET data = %s WHERE pk = %s;""",
                (data_str, pk)
            )
            self.cur.connection.commit()

    def make_pk(self, product_code: str, product_type: str) -> str:
        pk = sha256(f"{product_code}|{product_type}".encode()).hexdigest()
        return pk

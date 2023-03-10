from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = None

DB_USERNAME = os.getenv('DB_USERNAME', default="root")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="root")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_NAME = os.getenv('DB_NAME', default="edadb")
DB_READ_HOSTNAME = os.getenv('DB_READ_HOSTNAME', default="localhost")
DB_READ_NAME = os.getenv('DB_READ_NAME', default="localhost")


class DatabaseConfigException(Exception):
    def __init__(self, message='Configuration file is Null or malformed'):
        self.message = message
        super().__init__(self.message)


def database_connection(config, basedir=os.path.abspath(os.path.dirname(__file__))) -> str:
    if not isinstance(config, dict):
        raise DatabaseConfigException

    if config.get('TESTING', False):
        return f'sqlite:///{os.path.join(basedir, "database.db")}'
    else:
        return f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}'


def read_database_connection(config, basedir=os.path.abspath(os.path.dirname(__file__))) -> str:
    if not isinstance(config, dict):
        raise DatabaseConfigException

    if config.get('TESTING', False):
        return f'sqlite:///{os.path.join(basedir, "database.db")}'
    else:
        return f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_READ_HOSTNAME}/{DB_NAME}'


def init_db(app: Flask):
    global db
    global read_db
    db = SQLAlchemy(app)

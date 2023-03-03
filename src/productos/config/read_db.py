from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from productos.config.db import DatabaseConfigException
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

DB_USERNAME = os.getenv('DB_USERNAME', default="root")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="root")
DB_READ_HOSTNAME = os.getenv('DB_READ_HOSTNAME', default="localhost")
DB_READ_NAME = os.getenv('DB_READ_NAME', default="localhost")

base = declarative_base()
engine = sa.create_engine(f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_READ_HOSTNAME}/{DB_READ_NAME}')
base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)
base.metadata.create_all()

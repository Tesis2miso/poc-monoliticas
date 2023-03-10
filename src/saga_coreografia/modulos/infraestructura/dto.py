from saga_coreografia.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table
import uuid

Base = db.declarative_base()


class SagaLog(db.Model):
    __tablename__ = "sagalog"
    transaction_id = db.Column(db.String(250), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.String(250), nullable=False)
    detalle = db.Column(db.String(250), nullable=False)

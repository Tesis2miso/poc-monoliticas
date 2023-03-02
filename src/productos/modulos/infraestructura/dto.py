from productos.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table
import uuid

Base = db.declarative_base()

class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.String(40), primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    nombre = db.Column(db.String(250), nullable=False)
    stock = db.Column(db.Integer, primary_key=True, nullable=False)
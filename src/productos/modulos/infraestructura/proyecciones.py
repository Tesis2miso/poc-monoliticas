from productos.seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from productos.seedwork.infraestructura.proyecciones import ejecutar_proyeccion as proyeccion
from productos.modulos.infraestructura.dto import Producto as ProductoDTO
from productos.config.read_db import session
import datetime
import logging
import traceback
from abc import ABC, abstractmethod

class ProyeccionProducto(Proyeccion, ABC):
    @abstractmethod
    def ejecutar(self):
        ...

class ProyeccionModificacionProducto(ProyeccionProducto):
    def __init__(self, id, nombre, stock, fecha_creacion, fecha_actualizacion):
        self.id = id
        self.nombre = nombre
        self.stock = stock
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion

    def ejecutar(self, session=None):
        if not session:
            logging.error('ERROR: DB del app no puede ser nula')
            return

        record = session.query(ProductoDTO).filter_by(id=self.id).one_or_none()
        if record != None:
            record.nombre = self.nombre
            record.stock = self.stock
            record.fecha_actualizacion = self.fecha_actualizacion
        else:
            new_record = ProductoDTO()
            new_record.fecha_creacion = self.fecha_creacion
            new_record.fecha_actualizacion = self.fecha_actualizacion
            new_record.id = self.id
            new_record.nombre = self.nombre
            new_record.stock = self.stock
            session.add(new_record)
        session.commit()

class ProyeccionEliminarProducto(ProyeccionProducto):
    def __init__(self, id):
        self.id = id

    def ejecutar(self, session=None):
        if not session:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        session.query(ProductoDTO).filter_by(id=str(self.id)).delete()
        session.commit()


class ProyeccionProductoHandler(ProyeccionHandler):
    def handle(self, proyeccion: ProyeccionProducto):
        proyeccion.ejecutar(session=session)

@proyeccion.register(ProyeccionModificacionProducto)
@proyeccion.register(ProyeccionEliminarProducto)
def ejecutar_proyeccion_producto(proyeccion, app=None):
    handler = ProyeccionProductoHandler()
    handler.handle(proyeccion)
    
from productos.config.db import db
from productos.modulos.dominio.entidades import Producto
from uuid import UUID
from pulsar.schema import *
from productos.modulos.dominio.repositorios import RepositorioProductos
from productos.modulos.infraestructura.mapeadores import MapeadorProducto
from productos.modulos.dominio.fabricas import FabricaProductos

class RepositorioProductosSQLAlchemy(RepositorioProductos):
    def __init__(self):
        self._fabrica_productos: FabricaProductos = FabricaProductos()

    @property
    def fabrica_productos(self):
        return self._fabrica_productos

    def obtener_por_id(self, id: UUID) -> Producto:
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> list[Producto]:
        # TODO
        raise NotImplementedError

    def agregar(self, entity: Producto):
        producto_dto = self.fabrica_productos.crear_objeto(entity, MapeadorProducto())
        db.session.add(producto_dto)

    def actualizar(self, entity: Producto):
        # TODO
        raise NotImplementedError

    def eliminar(self, entity_id: UUID):
        # TODO
        raise NotImplementedError

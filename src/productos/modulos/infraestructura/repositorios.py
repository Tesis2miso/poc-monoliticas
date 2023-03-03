from productos.config.db import db
from productos.modulos.dominio.entidades import Producto
from uuid import UUID
from pulsar.schema import *
from productos.modulos.dominio.repositorios import RepositorioProductos
from productos.modulos.infraestructura.mapeadores import MapeadorProducto
from productos.modulos.dominio.fabricas import FabricaProductos
from productos.modulos.infraestructura.dto import Producto as ProductoDTO
from productos.config.read_db import engine
from sqlalchemy import orm

class RepositorioProductosSQLAlchemy(RepositorioProductos):
    def __init__(self):
        self._fabrica_productos: FabricaProductos = FabricaProductos()

    @property
    def fabrica_productos(self):
        return self._fabrica_productos

    def obtener_por_id(self, id: UUID) -> Producto:
        self.verification()
        read_session = orm.scoped_session(orm.sessionmaker())(bind=engine)
        producto_dto = read_session.query(ProductoDTO).filter_by(id=str(id)).one()
        read_session.close()
        return self.fabrica_productos.crear_objeto(producto_dto, MapeadorProducto())

    def obtener_todos(self) -> list[Producto]:
        self.verification()
        read_session = orm.scoped_session(orm.sessionmaker())(bind=engine)
        productos_dto = read_session.query(ProductoDTO).all()
        read_session.close()
        productos = []
        for producto_dto in productos_dto:
            productos.append(
                self.fabrica_productos.crear_objeto(producto_dto, MapeadorProducto()) 
            )
        return productos

    def agregar(self, entity: Producto):
        producto_dto = self.fabrica_productos.crear_objeto(entity, MapeadorProducto())
        db.session.add(producto_dto)

    def actualizar(self, entity: Producto):
        updated_producto_dto = self.fabrica_productos.crear_objeto(entity, MapeadorProducto())
        producto_dto = db.session.query(ProductoDTO).filter_by(id=str(entity.id)).one()
        producto_dto.nombre = updated_producto_dto.nombre
        producto_dto.stock = updated_producto_dto.stock

    def eliminar(self, id: UUID):
        db.session.query(ProductoDTO).filter_by(id=str(id)).delete()

    def verification(self):
        try:
            read_session.commit()
        except:
            read_session.rollback()

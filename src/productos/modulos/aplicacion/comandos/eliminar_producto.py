from productos.seedwork.aplicacion.comandos import Comando
from .base import ProductoBaseHandler
from dataclasses import dataclass
from productos.seedwork.aplicacion.comandos import ejecutar_commando as comando
from productos.modulos.aplicacion.dto import ProductoDTO
from productos.modulos.dominio.entidades import Producto
from pydispatch import dispatcher
from productos.modulos.aplicacion.mapeadores import MapeadorProducto
from productos.modulos.infraestructura.repositorios import RepositorioProductos
from productos.config.db import db
from productos.seedwork.infraestructura.uow import UnidadTrabajoPuerto

@dataclass
class EliminarProducto(Comando):
  id: str

class EliminarProductoHandler(ProductoBaseHandler):    
    def handle(self, comando: EliminarProducto):
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioProductos)
        repositorio.eliminar(comando.id)
        db.session.commit()


@comando.register(EliminarProducto)
def ejecutar_comando_eliminar_producto(comando: EliminarProducto):
    handler = EliminarProductoHandler()
    handler.handle(comando)

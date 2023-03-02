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
class ListarProductos(Comando):
  ...

class ListarProductosHandler(ProductoBaseHandler):    
    def handle(self, comando: ListarProductos) -> list[Producto]:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioProductos)
        productos: list[Producto] = repositorio.obtener_todos()
        return productos


@comando.register(ListarProductos)
def ejecutar_comando_listar_productos(comando: ListarProductos) -> list[Producto]:
    handler = ListarProductosHandler()
    return handler.handle(comando)
    
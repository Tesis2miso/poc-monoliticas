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
class ObtenerProducto(Comando):
  id: str

class ObtenerProductoHandler(ProductoBaseHandler):    
    def handle(self, comando: ObtenerProducto) -> Producto:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioProductos)
        producto: Producto = repositorio.obtener_por_id(comando.id)
        return producto


@comando.register(ObtenerProducto)
def ejecutar_comando_obtener_producto(comando: ObtenerProducto) -> Producto:
    handler = ObtenerProductoHandler()
    return handler.handle(comando)
    
from productos.seedwork.aplicacion.comandos import Comando
from .base import CrearProductoBaseHandler
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
class CrearProducto(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    nombre: str
    stock: int = 0

class CrearProductoHandler(CrearProductoBaseHandler):    
    def handle(self, comando: CrearProducto):
        producto_dto = ProductoDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   nombre=comando.nombre
            ,   stock=comando.stock)
        producto: Producto = self.fabrica_productos.crear_objeto(producto_dto, MapeadorProducto())
        producto.crear_producto(producto)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioProductos)
        repositorio.agregar(producto)
        for evento in producto.eventos:
            dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)
        db.session.commit()


@comando.register(CrearProducto)
def ejecutar_comando_crear_producto(comando: CrearProducto):
    handler = CrearProductoHandler()
    handler.handle(comando)
    
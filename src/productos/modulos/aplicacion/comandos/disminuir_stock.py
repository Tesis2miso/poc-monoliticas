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
from productos.modulos.infraestructura.schema.v1.comandos import ComandoAsignarConductor, ComandoAsignarConductorPayload
from productos.seedwork.infraestructura import utils
from productos.modulos.infraestructura.despachadores import Despachador

@dataclass
class DisminuirStock(Comando):
    id_producto: str
    id_orden: str
    cantidad: int
    direccion_entrega: str

class DisminuirStockHandler(ProductoBaseHandler):    
    def handle(self, comando: DisminuirStock):
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioProductos)
        producto: Producto = repositorio.obtener_por_id(comando.id_producto)
        producto.disminuir_stock(comando.cantidad)
        repositorio.actualizar(producto)
        for evento in producto.eventos:
            dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)
        db.session.commit()

@comando.register(DisminuirStock)
def ejecutar_comando_disminuir_stock(comando: DisminuirStock):
    handler = DisminuirStockHandler()
    handler.handle(comando)
    
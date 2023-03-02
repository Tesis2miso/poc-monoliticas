from productos.seedwork.dominio.repositorios import Mapeador
from productos.seedwork.infraestructura.utils import unix_time_millis
from productos.modulos.dominio.entidades import Producto
from .dto import Producto as ProductoDTO
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapeadorProducto(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Producto.__class__

    def entidad_a_dto(self, entidad: Producto) -> ProductoDTO:
        producto_dto = ProductoDTO()
        producto_dto.fecha_creacion = entidad.fecha_creacion
        producto_dto.fecha_actualizacion = entidad.fecha_actualizacion
        producto_dto.nombre = entidad.nombre
        producto_dto.stock = entidad.stock
        producto_dto.id = str(entidad.id)
        return producto_dto

    def dto_a_entidad(self, dto: ProductoDTO) -> Producto:
        producto = Producto(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        producto.nombre = dto.nombre
        producto.stock = dto.stock        
        return producto
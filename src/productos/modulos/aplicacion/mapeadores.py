from productos.seedwork.aplicacion.dto import Mapeador as AppMap
from productos.seedwork.dominio.repositorios import Mapeador as RepMap
from productos.modulos.dominio.entidades import Producto
from .dto import ProductoDTO
from datetime import datetime

class MapeadorProductoDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> ProductoDTO:
        reserva_dto = ProductoDTO(
            externo.get('nombre', None), externo.get('stock', None)
        )
        return reserva_dto

    def dto_a_externo(self, dto: ProductoDTO) -> dict:
        return dto.__dict__    

class MapeadorProducto(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Producto.__class__

    def entidad_a_dto(self, entidad: Producto) -> ProductoDTO:
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        nombre = entidad.nombre
        stock = entidad.stock
        return ProductoDTO(
            fecha_creacion, fecha_actualizacion, _id, nombre, stock
        )

    def dto_a_entidad(self, dto: ProductoDTO) -> Producto:
        producto = Producto()
        producto.nombre = dto.nombre
        producto.stock = dto.stock
        return producto




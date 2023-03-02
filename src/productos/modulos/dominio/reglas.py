from productos.seedwork.dominio.reglas import ReglaNegocio
from .entidades import Producto

class StockNoPuedeSerNegativo(ReglaNegocio):
    producto: Producto

    def __init__(self, producto, mensaje='Stock no puede ser menor a cero'):
        super().__init__(mensaje)
        self.producto = producto

    def es_valido(self) -> bool:
        return self.producto != None and self.producto.stock >= 0
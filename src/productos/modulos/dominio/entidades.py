from __future__ import annotations
from dataclasses import dataclass
from productos.seedwork.dominio.entidades import AgregacionRaiz
from datetime import datetime
from productos.modulos.dominio.eventos.productos import StockDisminuido

@dataclass
class Producto(AgregacionRaiz):
    nombre: str = ""
    stock: int = 0

    def crear_producto(self, producto: Producto):
        self.nombre = producto.nombre
        self.stock = producto.stock
        self.fecha_creacion = datetime.now()
        self.fecha_actualizacion = datetime.now()
    
    def disminuir_stock(self, cantidad: int):
        self.stock = self.stock - cantidad
        self.agregar_evento(
            StockDisminuido(self.id, datetime.now())
        )
from __future__ import annotations
from dataclasses import dataclass
from productos.seedwork.dominio.entidades import AgregacionRaiz
from datetime import datetime
from productos.modulos.dominio.eventos.productos import ProductoCreado

@dataclass
class Producto(AgregacionRaiz):
    nombre: str = ""
    stock: int = 0

    def crear_producto(self, producto: Producto):
        self.nombre = producto.nombre
        self.stock = producto.stock
        self.fecha_creacion = datetime.now()
        self.fecha_actualizacion = datetime.now()

        self.agregar_evento(
            ProductoCreado(self.id, self.fecha_creacion)
        )
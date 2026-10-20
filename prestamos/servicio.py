"""ServicioPrestamos: prestar, devolver con multa e historial por usuario. (T06, T15–T17)"""
from datetime import date

from materiales.catalogo import Catalogo
from prestamos.modelos import Prestamo
from usuarios.padron import Padron


class ServicioPrestamos:
    """Guarda los préstamos (activos e históricos) y usa el catálogo y el padrón."""

    def __init__(self, catalogo: Catalogo, padron: Padron):
        self._catalogo = catalogo
        self._padron = padron
        self._prestamos: list[Prestamo] = []

    def prestar(self, id_usuario: int, id_material: int, hoy: date) -> Prestamo:
        # Checa disponibilidad y límite de préstamos, y calcula el vencimiento (T15)
        raise NotImplementedError

    def devolver(self, id_prestamo: int, hoy: date) -> float:
        # Libera el material, calcula la multa si hubo retraso y la regresa (T16)
        raise NotImplementedError

    def historial(self, id_usuario: int) -> list[Prestamo]:
        # Préstamos del usuario, del más reciente al más antiguo (T17)
        raise NotImplementedError

    def todos(self) -> list[Prestamo]:
        # Todos los préstamos que hay, activos y ya devueltos
        raise NotImplementedError

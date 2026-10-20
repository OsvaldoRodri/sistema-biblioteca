"""Reportes: materiales más prestados, usuarios con préstamos vencidos y multas acumuladas. (T06, T19–T21)"""
from datetime import date

from prestamos.servicio import ServicioPrestamos


class Reportes:
    """Saca reportes a partir de los préstamos que lleva ServicioPrestamos."""

    def __init__(self, servicio: ServicioPrestamos):
        self._servicio = servicio

    def mas_prestados(self, n: int) -> list[tuple[str, int]]:
        # Los n materiales más prestados: (titulo, veces_prestado), de mayor a menor (T19)
        raise NotImplementedError

    def usuarios_con_vencidos(self, hoy: date) -> list[tuple[str, str, int]]:
        # Usuarios con algún préstamo activo vencido: (usuario, material, dias_retraso) (T20)
        raise NotImplementedError

    def multas_acumuladas(self) -> tuple[dict[str, float], float]:
        # Multas ya cobradas por usuario, y el total de todas juntas (T21)
        raise NotImplementedError

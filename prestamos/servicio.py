"""ServicioPrestamos: prestar, devolver con multa e historial por usuario. (T06, T15–T17)"""
from datetime import date, timedelta

from comun import config
from comun.excepciones import (
    DatoInvalido,
    LimiteExcedido,
    MaterialNoDisponible,
    NoEncontrado,
)
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
        """Presta un material si está libre y el usuario no ha llegado a su límite (T15)."""
        # 1. Que existan los dos (obtener() lanza NoEncontrado si no).
        usuario = self._padron.obtener(id_usuario)
        material = self._catalogo.obtener(id_material)

        # 2. Que el material no esté prestado.
        if not material.esta_disponible():
            raise MaterialNoDisponible(f'"{material.titulo}" ya está prestado')

        # 3. Que el usuario no tenga ya tantos préstamos activos como su límite.
        activos = len(self._activos_de(id_usuario))
        if activos >= usuario.limite_prestamos:
            raise LimiteExcedido(
                f"{usuario.nombre} ya tiene {activos} préstamos activos "
                f"(su límite es {usuario.limite_prestamos})"
            )

        # 4. Se crea el préstamo; el vencimiento depende del tipo de usuario.
        vencimiento = hoy + timedelta(days=usuario.dias_vigencia)
        prestamo = Prestamo(self._siguiente_id(), usuario, material, hoy, vencimiento)
        material.marcar_prestado()
        self._prestamos.append(prestamo)
        return prestamo

    def devolver(self, id_prestamo: int, hoy: date) -> float:
        """Libera el material, calcula la multa si hubo retraso y la regresa (T16)."""
        prestamo = self._obtener(id_prestamo)
        if not prestamo.esta_activo():
            raise DatoInvalido(f"El préstamo {id_prestamo} ya se había devuelto")

        prestamo.multa = prestamo.dias_retraso(hoy) * config.MULTA_POR_DIA
        prestamo.fecha_devolucion = hoy
        prestamo.material.marcar_devuelto()
        return prestamo.multa

    def historial(self, id_usuario: int) -> list[Prestamo]:
        """Préstamos del usuario, del más reciente al más antiguo (T17)."""
        del_usuario = [p for p in self._prestamos if p.usuario.id == id_usuario]
        # Mismo día: el de id mayor se hizo después.
        return sorted(del_usuario, key=lambda p: (p.fecha_prestamo, p.id), reverse=True)

    def todos(self) -> list[Prestamo]:
        """Todos los préstamos, activos y ya devueltos (lo usa Reportes)."""
        return list(self._prestamos)

    def _activos_de(self, id_usuario: int) -> list[Prestamo]:
        return [p for p in self._prestamos if p.usuario.id == id_usuario and p.esta_activo()]

    def _obtener(self, id_prestamo: int) -> Prestamo:
        for prestamo in self._prestamos:
            if prestamo.id == id_prestamo:
                return prestamo
        raise NoEncontrado(f"No existe el préstamo con id {id_prestamo}")

    def _siguiente_id(self) -> int:
        return max((p.id for p in self._prestamos), default=0) + 1

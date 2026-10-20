"""Pruebas de la clase Prestamo (T05)."""

from datetime import date

import pytest

from materiales.modelos import Libro
from prestamos.modelos import Prestamo
from usuarios.modelos import Estudiante


@pytest.fixture
def prestamo():
    """Préstamo del 3 de octubre que vence el 10 de octubre de 2026."""
    libro = Libro(1, "Pedro Páramo", "Juan Rulfo", 1955, "978-607-16-0293-6", "FCE")
    estudiante = Estudiante(1, "Ana López", "ana@ejemplo.com")
    return Prestamo(1, estudiante, libro, date(2026, 10, 3), date(2026, 10, 10))


def test_prestamo_nuevo_esta_activo(prestamo):
    assert prestamo.esta_activo() is True
    assert prestamo.fecha_devolucion is None
    assert prestamo.multa == 0


def test_tres_dias_despues_del_vencimiento(prestamo):
    hoy = date(2026, 10, 13)

    assert prestamo.dias_retraso(hoy) == 3
    assert prestamo.esta_vencido(hoy) is True


def test_el_mismo_dia_del_vencimiento_no_esta_vencido(prestamo):
    hoy = date(2026, 10, 10)

    assert prestamo.dias_retraso(hoy) == 0
    assert prestamo.esta_vencido(hoy) is False


def test_antes_del_vencimiento_no_hay_retraso_negativo(prestamo):
    assert prestamo.dias_retraso(date(2026, 10, 5)) == 0


def test_prestamo_devuelto_nunca_esta_vencido(prestamo):
    prestamo.fecha_devolucion = date(2026, 10, 12)

    assert prestamo.esta_activo() is False
    assert prestamo.esta_vencido(date(2026, 12, 1)) is False

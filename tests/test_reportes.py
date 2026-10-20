"""Pruebas de Reportes (T19-T21). Los prestamos se arman a mano, no se
necesita que ServicioPrestamos (T15-T17) ya funcione."""

from datetime import date

import pytest

from materiales.modelos import Libro
from usuarios.modelos import Estudiante
from prestamos.modelos import Prestamo
from reportes.reportes import Reportes


class ServicioFalso:
    """Nada más regresa la lista de prestamos que le demos, como haria ServicioPrestamos.todos()."""

    def __init__(self, prestamos):
        self._prestamos = prestamos

    def todos(self):
        return self._prestamos


def hacer_prestamo(id_prestamo, usuario, material, fecha_prestamo, fecha_vencimiento,
                    fecha_devolucion=None, multa=0):
    prestamo = Prestamo(id_prestamo, usuario, material, fecha_prestamo, fecha_vencimiento)
    prestamo.fecha_devolucion = fecha_devolucion
    prestamo.multa = multa
    return prestamo


# Usuarios y materiales de prueba, reusados en varios tests
ana = Estudiante(1, "Ana López", "ana@ejemplo.com")
beto = Estudiante(2, "Beto Ruiz", "beto@ejemplo.com")
libro1 = Libro(1, "Pedro Páramo", "Juan Rulfo", 1955, "978-0", "FCE")
libro2 = Libro(2, "Rayuela", "Julio Cortázar", 1963, "978-1", "Sudamericana")
libro3 = Libro(3, "Nunca prestado", "Nadie", 2000, "978-2", "X")


def test_mas_prestados_cuenta_y_ordena():
    prestamos = [
        hacer_prestamo(1, ana, libro1, date(2026, 1, 1), date(2026, 1, 8)),
        hacer_prestamo(2, beto, libro1, date(2026, 1, 10), date(2026, 1, 17)),
        hacer_prestamo(3, ana, libro2, date(2026, 1, 1), date(2026, 1, 8)),
    ]
    reportes = Reportes(ServicioFalso(prestamos))

    resultado = reportes.mas_prestados(5)

    assert resultado[0] == ("Pedro Páramo", 2)
    assert resultado[1] == ("Rayuela", 1)


def test_mas_prestados_respeta_el_limite_n():
    prestamos = [
        hacer_prestamo(1, ana, libro1, date(2026, 1, 1), date(2026, 1, 8)),
        hacer_prestamo(2, ana, libro2, date(2026, 1, 1), date(2026, 1, 8)),
    ]
    reportes = Reportes(ServicioFalso(prestamos))

    resultado = reportes.mas_prestados(1)

    assert len(resultado) == 1


def test_material_nunca_prestado_no_aparece():
    prestamos = [hacer_prestamo(1, ana, libro1, date(2026, 1, 1), date(2026, 1, 8))]
    reportes = Reportes(ServicioFalso(prestamos))

    titulos = [titulo for titulo, _ in reportes.mas_prestados(10)]

    assert libro3.titulo not in titulos


def test_usuarios_con_vencidos_solo_cuenta_activos_y_vencidos():
    hoy = date(2026, 1, 20)
    prestamos = [
        # vencido desde hace 3 dias, sigue activo
        hacer_prestamo(1, ana, libro1, date(2026, 1, 1), date(2026, 1, 17)),
        # vence justo hoy, no deberia contar como vencido
        hacer_prestamo(2, beto, libro2, date(2026, 1, 1), date(2026, 1, 20)),
    ]
    reportes = Reportes(ServicioFalso(prestamos))

    resultado = reportes.usuarios_con_vencidos(hoy)

    assert resultado == [("Ana López", "Pedro Páramo", 3)]


def test_prestamo_devuelto_no_aparece_aunque_se_devolvio_tarde():
    hoy = date(2026, 1, 20)
    prestamos = [
        hacer_prestamo(
            1, ana, libro1, date(2026, 1, 1), date(2026, 1, 8),
            fecha_devolucion=date(2026, 1, 15), multa=70,
        ),
    ]
    reportes = Reportes(ServicioFalso(prestamos))

    assert reportes.usuarios_con_vencidos(hoy) == []


def test_multas_acumuladas_suma_por_usuario_y_total():
    prestamos = [
        hacer_prestamo(1, ana, libro1, date(2026, 1, 1), date(2026, 1, 8),
                       fecha_devolucion=date(2026, 1, 11), multa=30),
        hacer_prestamo(2, ana, libro2, date(2026, 1, 1), date(2026, 1, 8),
                       fecha_devolucion=date(2026, 1, 10), multa=20),
        hacer_prestamo(3, beto, libro1, date(2026, 1, 1), date(2026, 1, 8),
                       fecha_devolucion=date(2026, 1, 8), multa=0),
    ]
    reportes = Reportes(ServicioFalso(prestamos))

    por_usuario, total = reportes.multas_acumuladas()

    assert por_usuario == {"Ana López (ID 1)": 50}
    assert total == 50


def test_multas_acumuladas_no_junta_a_usuarios_con_el_mismo_nombre():
    # Dos "Ana López" distintas (ids diferentes); sus multas no se deben mezclar
    otra_ana = Estudiante(99, "Ana López", "otra.ana@ejemplo.com")
    prestamos = [
        hacer_prestamo(1, ana, libro1, date(2026, 1, 1), date(2026, 1, 8),
                       fecha_devolucion=date(2026, 1, 11), multa=30),
        hacer_prestamo(2, otra_ana, libro2, date(2026, 1, 1), date(2026, 1, 8),
                       fecha_devolucion=date(2026, 1, 10), multa=20),
    ]
    reportes = Reportes(ServicioFalso(prestamos))

    por_usuario, total = reportes.multas_acumuladas()

    assert por_usuario == {"Ana López (ID 1)": 30, "Ana López (ID 99)": 20}
    assert total == 50

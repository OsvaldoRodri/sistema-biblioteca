"""Pruebas de ServicioPrestamos (T15-T17).

Usan un catálogo y un padrón falsos para no depender de que Materiales (T08)
y Usuarios (T12) ya estén en main: lo único que el servicio les pide es obtener().
"""
from datetime import date

import pytest

from comun.excepciones import (
    DatoInvalido,
    LimiteExcedido,
    MaterialNoDisponible,
    NoEncontrado,
)
from materiales.modelos import Libro
from prestamos.servicio import ServicioPrestamos
from usuarios.modelos import Estudiante, Profesor


class RepositorioFalso:
    """Hace de Catalogo o de Padron: guarda objetos por id y los regresa con obtener()."""

    def __init__(self, *objetos):
        self._por_id = {o.id: o for o in objetos}

    def obtener(self, id_):
        if id_ not in self._por_id:
            raise NoEncontrado(f"No existe el id {id_}")
        return self._por_id[id_]


def libro(id_material, titulo="Pedro Páramo"):
    return Libro(id_material, titulo, "Juan Rulfo", 1955, f"isbn-{id_material}", "FCE")


ANA = 1    # estudiante: 3 préstamos, 7 días
LUIS = 2   # profesor: 5 préstamos, 15 días
OCT_1 = date(2026, 10, 1)


@pytest.fixture
def servicio():
    catalogo = RepositorioFalso(*(libro(i, f"Libro {i}") for i in range(1, 6)))
    padron = RepositorioFalso(
        Estudiante(ANA, "Ana López", "ana@ejemplo.com"),
        Profesor(LUIS, "Luis Pérez", "luis@ejemplo.com"),
    )
    return ServicioPrestamos(catalogo, padron)


# --- T15: prestar ---------------------------------------------------------

def test_prestar_marca_el_material_y_calcula_vencimiento(servicio):
    prestamo = servicio.prestar(ANA, 1, OCT_1)

    assert prestamo.fecha_vencimiento == date(2026, 10, 8)  # 7 días de estudiante
    assert prestamo.material.esta_disponible() is False
    assert prestamo.esta_activo() is True


def test_profesor_que_pide_el_1_de_noviembre_vence_el_16(servicio):
    prestamo = servicio.prestar(LUIS, 1, date(2026, 11, 1))

    assert prestamo.fecha_vencimiento == date(2026, 11, 16)


def test_estudiante_puede_llevarse_3_y_el_cuarto_falla(servicio):
    for id_material in (1, 2, 3):
        servicio.prestar(ANA, id_material, OCT_1)

    with pytest.raises(LimiteExcedido):
        servicio.prestar(ANA, 4, OCT_1)
    assert servicio.todos()[-1].material.id == 3  # el cuarto no se guardó


def test_al_devolver_uno_vuelve_a_tener_lugar(servicio):
    p1 = servicio.prestar(ANA, 1, OCT_1)
    servicio.prestar(ANA, 2, OCT_1)
    servicio.prestar(ANA, 3, OCT_1)
    servicio.devolver(p1.id, OCT_1)

    assert servicio.prestar(ANA, 4, OCT_1).material.id == 4


def test_material_ya_prestado_lanza_no_disponible(servicio):
    servicio.prestar(ANA, 1, OCT_1)

    with pytest.raises(MaterialNoDisponible):
        servicio.prestar(LUIS, 1, OCT_1)


@pytest.mark.parametrize("id_usuario, id_material", [(99, 1), (ANA, 99)])
def test_usuario_o_material_inexistente_lanza_no_encontrado(servicio, id_usuario, id_material):
    with pytest.raises(NoEncontrado):
        servicio.prestar(id_usuario, id_material, OCT_1)


# --- T16: devolver --------------------------------------------------------

def test_devolver_a_tiempo_no_cobra_y_libera_el_material(servicio):
    prestamo = servicio.prestar(ANA, 1, OCT_1)

    multa = servicio.devolver(prestamo.id, date(2026, 10, 8))  # el mismo día que vence

    assert multa == 0
    assert prestamo.esta_activo() is False
    assert prestamo.material.esta_disponible() is True


def test_devolver_3_dias_tarde_cobra_30(servicio):
    prestamo = servicio.prestar(ANA, 1, OCT_1)  # vence el 8

    assert servicio.devolver(prestamo.id, date(2026, 10, 11)) == 30
    assert prestamo.multa == 30


def test_devolver_dos_veces_falla_la_segunda(servicio):
    prestamo = servicio.prestar(ANA, 1, OCT_1)
    servicio.devolver(prestamo.id, OCT_1)

    with pytest.raises(DatoInvalido):
        servicio.devolver(prestamo.id, OCT_1)


def test_devolver_prestamo_inexistente_lanza_no_encontrado(servicio):
    with pytest.raises(NoEncontrado):
        servicio.devolver(99, OCT_1)


# --- T17: historial -------------------------------------------------------

def test_historial_de_usuario_sin_prestamos_es_vacio(servicio):
    assert servicio.historial(LUIS) == []


def test_historial_va_del_mas_reciente_al_mas_antiguo(servicio):
    servicio.prestar(ANA, 1, date(2026, 10, 1))
    servicio.prestar(ANA, 2, date(2026, 10, 5))
    servicio.prestar(LUIS, 3, date(2026, 10, 3))  # de otro usuario, no debe salir

    titulos = [p.material.titulo for p in servicio.historial(ANA)]

    assert titulos == ["Libro 2", "Libro 1"]


def test_todos_regresa_una_copia(servicio):
    servicio.prestar(ANA, 1, OCT_1)

    servicio.todos().clear()

    assert len(servicio.todos()) == 1

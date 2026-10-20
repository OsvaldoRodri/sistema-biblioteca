"""Pruebas para los modelos de usuarios (T04)."""

from usuarios.modelos import Estudiante, Profesor, Administrativo


def test_limite_prestamos_por_tipo():
    """Cada tipo de usuario debe tener su límite correspondiente."""
    estudiante = Estudiante(1, "Ana López", "ana@ejemplo.com")
    profesor = Profesor(2, "Luis Pérez", "luis@ejemplo.com")
    administrativo = Administrativo(3, "Marta Ruiz", "marta@ejemplo.com")

    assert estudiante.limite_prestamos == 3
    assert profesor.limite_prestamos == 4
    assert administrativo.limite_prestamos == 5


def test_dias_vigencia_por_tipo():
    """Cada tipo de usuario debe tener sus días de vigencia."""
    estudiante = Estudiante(1, "Ana López", "ana@ejemplo.com")
    profesor = Profesor(2, "Luis Pérez", "luis@ejemplo.com")
    administrativo = Administrativo(3, "Marta Ruiz", "marta@ejemplo.com")

    assert estudiante.dias_vigencia == 7
    assert profesor.dias_vigencia == 14
    assert administrativo.dias_vigencia == 10


import pytest

from usuarios.padron import Padron
from comun.excepciones import DatoInvalido, NoEncontrado


def test_registrar_y_obtener_usuario():
    padron = Padron()
    usuario = Estudiante(1, "Ana López", "ana@ejemplo.com")

    padron.registrar(usuario)

    assert padron.obtener(1) is usuario


def test_rechazar_nombre_vacio():
    padron = Padron()
    usuario = Estudiante(1, "   ", "ana@ejemplo.com")

    with pytest.raises(DatoInvalido):
        padron.registrar(usuario)


def test_rechazar_correo_sin_arroba():
    padron = Padron()
    usuario = Estudiante(1, "Ana López", "ana.ejemplo.com")

    with pytest.raises(DatoInvalido):
        padron.registrar(usuario)


def test_rechazar_id_duplicado():
    padron = Padron()
    primero = Estudiante(1, "Ana López", "ana@ejemplo.com")
    segundo = Profesor(1, "Luis Pérez", "luis@ejemplo.com")

    padron.registrar(primero)

    with pytest.raises(DatoInvalido):
        padron.registrar(segundo)


def test_usuario_no_encontrado():
    padron = Padron()

    with pytest.raises(NoEncontrado):
        padron.obtener(999)

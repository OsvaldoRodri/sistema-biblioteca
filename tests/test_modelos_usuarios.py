"""Pruebas de los modelos de usuarios (T04)."""

import pytest

from comun import config
from usuarios.modelos import Administrativo, Estudiante, Profesor, Usuario


def test_usuario_es_abstracta():
    with pytest.raises(TypeError):
        Usuario(1, "Ana López", "ana@ejemplo.com")


def test_limite_prestamos_por_tipo():
    estudiante = Estudiante(1, "Ana López", "ana@ejemplo.com")
    administrativo = Administrativo(2, "Marta Ruiz", "marta@ejemplo.com")
    profesor = Profesor(3, "Luis Pérez", "luis@ejemplo.com")

    assert estudiante.limite_prestamos == 3
    assert administrativo.limite_prestamos == 4
    assert profesor.limite_prestamos == 5


def test_dias_vigencia_por_tipo():
    estudiante = Estudiante(1, "Ana López", "ana@ejemplo.com")
    administrativo = Administrativo(2, "Marta Ruiz", "marta@ejemplo.com")
    profesor = Profesor(3, "Luis Pérez", "luis@ejemplo.com")

    assert estudiante.dias_vigencia == 7
    assert administrativo.dias_vigencia == 10
    assert profesor.dias_vigencia == 15


def test_valores_salen_de_config(monkeypatch):
    """Cambiar config.py cambia el comportamiento sin tocar las clases."""
    monkeypatch.setattr(config, "LIMITE_PRESTAMOS_ESTUDIANTE", 9)
    monkeypatch.setattr(config, "DIAS_VIGENCIA_ESTUDIANTE", 30)

    estudiante = Estudiante(1, "Ana López", "ana@ejemplo.com")

    assert estudiante.limite_prestamos == 9
    assert estudiante.dias_vigencia == 30

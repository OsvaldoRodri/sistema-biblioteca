"""Pruebas de los modelos de usuarios (T04)."""

from usuarios.modelos import Estudiante, Profesor, Administrativo


def test_limite_prestamos_por_tipo():
    estudiante = Estudiante(1, "Ana López", "ana@ejemplo.com")
    profesor = Profesor(2, "Luis Pérez", "luis@ejemplo.com")
    administrativo = Administrativo(3, "Marta Ruiz", "marta@ejemplo.com")

    assert estudiante.limite_prestamos == 3
    assert profesor.limite_prestamos == 4
    assert administrativo.limite_prestamos == 5


def test_dias_vigencia_por_tipo():
    estudiante = Estudiante(1, "Ana López", "ana@ejemplo.com")
    profesor = Profesor(2, "Luis Pérez", "luis@ejemplo.com")
    administrativo = Administrativo(3, "Marta Ruiz", "marta@ejemplo.com")

    assert estudiante.dias_vigencia == 7
    assert profesor.dias_vigencia == 14
    assert administrativo.dias_vigencia == 10

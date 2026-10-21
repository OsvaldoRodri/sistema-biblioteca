"""Pruebas del menú de préstamos (T18): se simula el teclado con monkeypatch."""
from prestamos.menu import menu_prestamos
from prestamos.servicio import ServicioPrestamos
from tests.test_servicio_prestamos import ANA, RepositorioFalso, libro
from usuarios.modelos import Estudiante


def correr_menu(monkeypatch, respuestas, servicio=None):
    entradas = iter(respuestas)
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    if servicio is None:
        servicio = ServicioPrestamos(
            RepositorioFalso(libro(1, "Pedro Páramo")),
            RepositorioFalso(Estudiante(ANA, "Ana López", "ana@ejemplo.com")),
        )
    menu_prestamos(servicio)
    return servicio


def test_prestar_y_devolver_desde_el_menu(monkeypatch, capsys):
    servicio = correr_menu(monkeypatch, ["1", "1", "1", "2", "1", "4"])

    salida = capsys.readouterr().out
    assert 'Préstamo 1: "Pedro Páramo" para Ana López' in salida
    assert "Devuelto a tiempo, sin multa." in salida
    assert servicio.todos()[0].esta_activo() is False


def test_historial_desde_el_menu(monkeypatch, capsys):
    correr_menu(monkeypatch, ["1", "1", "1", "3", "1", "4"])

    salida = capsys.readouterr().out
    assert "Pedro Páramo" in salida
    assert "Activo" in salida


def test_errores_del_sistema_no_truenan_el_menu(monkeypatch, capsys):
    # Préstamo de un material que no existe y luego prestar el mismo dos veces.
    correr_menu(monkeypatch, ["1", "1", "99", "1", "1", "1", "1", "1", "1", "4"])

    salida = capsys.readouterr().out
    assert "Error: No existe el id 99" in salida
    assert "ya está prestado" in salida


def test_letras_donde_va_numero_y_opcion_invalida(monkeypatch, capsys):
    correr_menu(monkeypatch, ["1", "abc", "7", "4"])

    salida = capsys.readouterr().out
    assert "Pon un número, por favor." in salida
    assert "Opción inválida" in salida

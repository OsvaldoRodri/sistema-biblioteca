
from usuarios.modelos import Estudiante, Profesor, Administrativo
from usuarios.padron import Padron
from usuarios.consultas import consultar_usuario


def test_consultar_estudiante(capsys):
    padron = Padron()
    padron.registrar(Estudiante(1, "Ana Lopez", "ana@ejemplo.com"))

    consultar_usuario(padron, 1)
    salida = capsys.readouterr().out

    assert "Tipo: Estudiante" in salida
    assert "Nombre: Ana Lopez" in salida
    assert "Correo: ana@ejemplo.com" in salida
    assert "Límite de préstamos: 3" in salida
    assert "Días de vigencia: 7" in salida


def test_consultar_profesor(capsys):
    padron = Padron()
    padron.registrar(Profesor(2, "Luis Perez", "luis@ejemplo.com"))

    consultar_usuario(padron, 2)
    salida = capsys.readouterr().out

    assert "Tipo: Profesor" in salida
    assert "Límite de préstamos: 5" in salida
    assert "Días de vigencia: 15" in salida


def test_consultar_administrativo(capsys):
    padron = Padron()
    padron.registrar(
        Administrativo(3, "Marta Ruiz", "marta@ejemplo.com")
    )

    consultar_usuario(padron, 3)
    salida = capsys.readouterr().out

    assert "Tipo: Administrativo" in salida
    assert "Límite de préstamos: 4" in salida
    assert "Días de vigencia: 10" in salida


def test_consultar_usuario_inexistente(capsys):
    padron = Padron()

    consultar_usuario(padron, 999)
    salida = capsys.readouterr().out

    assert "Error:" in salida
    assert "999" in salida

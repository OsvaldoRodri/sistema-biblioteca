
from comun.datos_ejemplo import (
    crear_materiales_ejemplo,
    crear_usuarios_ejemplo,
)
from materiales.modelos import Libro, Revista, Tesis
from usuarios.modelos import Estudiante, Profesor, Administrativo


def test_crear_materiales_ejemplo():
    """Verifica que se creen diez materiales de ejemplo."""
    materiales = crear_materiales_ejemplo()

    assert len(materiales) == 10
    assert sum(isinstance(m, Libro) for m in materiales) == 5
    assert sum(isinstance(m, Revista) for m in materiales) == 3
    assert sum(isinstance(m, Tesis) for m in materiales) == 2


def test_ids_de_materiales_son_unicos():
    """Verifica que cada material tenga un ID diferente."""
    materiales = crear_materiales_ejemplo()
    ids = [material.id for material in materiales]

    assert len(ids) == len(set(ids))


def test_crear_usuarios_ejemplo():
    """Verifica que se cree un usuario de cada tipo."""
    usuarios = crear_usuarios_ejemplo()

    assert len(usuarios) == 3
    assert sum(isinstance(u, Estudiante) for u in usuarios) == 1
    assert sum(isinstance(u, Profesor) for u in usuarios) == 1
    assert sum(isinstance(u, Administrativo) for u in usuarios) == 1


def test_ids_de_usuarios_son_unicos():
    """Verifica que cada usuario tenga un ID diferente."""
    usuarios = crear_usuarios_ejemplo()
    ids = [usuario.id for usuario in usuarios]

    assert len(ids) == len(set(ids))


def test_datos_de_ejemplo_se_crean_nuevamente():
    """Verifica que cada llamada genere listas independientes."""
    materiales1 = crear_materiales_ejemplo()
    materiales2 = crear_materiales_ejemplo()
    usuarios1 = crear_usuarios_ejemplo()
    usuarios2 = crear_usuarios_ejemplo()

    assert materiales1 is not materiales2
    assert usuarios1 is not usuarios2

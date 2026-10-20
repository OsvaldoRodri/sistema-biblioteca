"""Padron: registrar y consultar usuarios. (T06, T12–T13)"""
from usuarios.modelos import Usuario


class Padron:
    """Guarda todos los usuarios que se van registrando."""

    def __init__(self):
        self._usuarios: list[Usuario] = []

    def registrar(self, usuario: Usuario) -> None:
        # Rechaza nombre vacío, correo sin @ o id repetido (T12)
        raise NotImplementedError

    def obtener(self, id_usuario: int) -> Usuario:
        # Regresa el usuario con ese id, o lanza NoEncontrado (T13)
        raise NotImplementedError

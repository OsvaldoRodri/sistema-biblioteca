"""Catalogo: registrar, buscar por título/autor/ISBN y consultar disponibilidad. (T06, T08–T10)"""
from materiales.modelos import Material


class Catalogo:
    """Guarda todos los materiales que se van registrando."""

    def __init__(self):
        self._materiales: list[Material] = []

    def registrar(self, material: Material) -> None:
        # Guarda el material; si es libro con ISBN repetido, falla (T08)
        raise NotImplementedError

    def obtener(self, id_material: int) -> Material:
        # Regresa el material con ese id, o lanza NoEncontrado (T08)
        raise NotImplementedError

    def buscar(self, texto: str, campo: str) -> list[Material]:
        # campo puede ser "titulo", "autor" o "isbn"; busca parcial y sin mayúsculas (T09)
        raise NotImplementedError

    def disponibilidad(self, id_material: int) -> str:
        # Dice si el material está "Disponible" o "Prestado" (T10)
        raise NotImplementedError

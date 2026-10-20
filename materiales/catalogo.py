"""Catalogo: registrar, buscar por título/autor/ISBN y consultar disponibilidad. (T06, T08–T10)"""
from materiales.modelos import Material, Libro
from comun.excepciones import DatoInvalido, NoEncontrado


class Catalogo:
    """Guarda todos los materiales que se van registrando."""

    def __init__(self):
        self._materiales: list[Material] = []

    def registrar(self, material: Material) -> None:
        """
        Primero comprueba que realmente el material sea un Libro
        para posteriormente recorrer la lista y comprobar que el elemento en
        la lista que estamos recorriendo sea de igual forma un Libro y así
        poder verificar que el ISBN sea el mismo, y si es el caso, entonces mandamos una
        excepcion (DatoInvalido) de que el ISBN ya se encuentra registrado.
        """
        if isinstance(material, Libro):
            for m in self._materiales:
                if isinstance(m, Libro) and m.isbn == material.isbn:
                    raise DatoInvalido(f"ISBN repetido: {material.isbn}")
                
        """Verifica si el id está vacío para asignar uno automaticamente."""
        if material.id is None:
            material.id = len(self._materiales) + 1
        
        """Guardar el material en la lista"""
        self._materiales.append(material)

    def obtener(self, id_material: int) -> Material:
        """
        Recorre la lista para encontrar el material que coincida con el id.
        Si coincide retorna el Material. Si al finalizar el for no lo devuelve,
        manda una excepcion (NoEncontrado).
        """
        for m in self._materiales:
            if m.id == id_material:
                return m

        raise NoEncontrado(f"Material con el id {id_material} no encontrado")

    def buscar(self, texto: str, campo: str) -> list[Material]:
        # campo puede ser "titulo", "autor" o "isbn"; busca parcial y sin mayúsculas (T09)
        raise NotImplementedError

    def disponibilidad(self, id_material: int) -> str:
        # Dice si el material está "Disponible" o "Prestado" (T10)
        raise NotImplementedError

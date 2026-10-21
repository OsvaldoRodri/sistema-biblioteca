"""Catalogo: registrar, buscar por título/autor/ISBN y consultar disponibilidad. (T06, T08–T10)"""
from materiales.modelos import Material, Libro
from comun.excepciones import DatoInvalido, NoEncontrado

import unicodedata

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
                
        # Verifica si el id está vacío para asignar uno automaticamente.
        # Se usa max() para obtener el id más alto e incrementarle +1.
        if material.id is None:
            material.id = max((m.id for m in self._materiales), default=0) + 1
        
        # Guardar el material en la lista
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
        # Valida que el campo ingresado sea únicamente uno de los tres permitidos
        if campo not in ("titulo", "autor", "isbn"):
            raise DatoInvalido(f"Campo inválido: {campo}")

        resultados = []

        for material in self._materiales:
            # Obtiene el valor del atributo de forma dinámica (ej: material.titulo o material.autor)
            # Si el atributo no existe, asigna un texto vacío "" para evitar que el programa falle
            valor = getattr(material, campo, "")

            # Compara el texto buscado con el valor del material
            # .lower() convierte ambos textos a minúsculas para ignorar las diferencias de mayúsculas
            # El operador 'in' verifica si el texto ingresado está contenido de forma parcial en el valor
            if self._sin_acentos(texto.lower()) in self._sin_acentos(valor.lower()):
                # Si hay coincidencia, agrega el objeto material a la lista de resultados
                resultados.append(material)

        # Devuelve la lista con los resultados encontrados
        return resultados
        

    def disponibilidad(self, id_material: int) -> str:
        # Devolvemos el etado al obtener el material con obtener() usando el id
        material = self.obtener(id_material)
        
        estado = "Disponible"
        if not material.esta_disponible():
            estado = "Prestado"
        
        return estado



    @staticmethod
    def _sin_acentos(texto: str) -> str:
        """Quita acentos"""
        # Descompone el texto en formato NFD. Esto separa las letras de sus acentos
        # Por ejemplo, la 'á' se convierte en una 'a' normal más un carácter de acento independiente
        nfd = unicodedata.normalize("NFD", texto)
        
        # Recorre cada carácter en el texto descompuesto y evalúa su categoría
        # 'Mn' representa a los acentos e indicaciones flotantes (Mark, Nonspacing)
        # Filtra el texto guardando solo las letras que NO sean acentos y las une con .join()
        return "".join(c for c in nfd if unicodedata.category(c) != "Mn")
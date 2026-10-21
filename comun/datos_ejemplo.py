"""Materiales y usuarios precargados al arrancar el programa. (T07)"""

from materiales.modelos import Libro, Revista, Tesis
from usuarios.modelos import Estudiante, Profesor, Administrativo


def crear_materiales_ejemplo():
    """Crea cinco libros, tres revistas y dos tesis."""
    materiales = [
        Libro(
            1, "Cien años de soledad", "Gabriel García Márquez", 1967,
            "9780307474728", "Editorial Sudamericana"
        ),
        Libro(
            2, "Don Quijote de la Mancha", "Miguel de Cervantes", 1605,
            "9788420412146", "Alfaguara"
        ),
        Libro(
            3, "El principito", "Antoine de Saint-Exupéry", 1943,
            "9780156012195", "Reynal & Hitchcock"
        ),
        Libro(
            4, "1984", "George Orwell", 1949,
            "9780451524935", "Secker & Warburg"
        ),
        Libro(
            5, "Pedro Páramo", "Juan Rulfo", 1955,
            "9786070728792", "Fondo de Cultura Económica"
        ),
        Revista(
            6, "Investigación y Ciencia", "Varios autores", 2024,
            "0210136X", 580, 48
        ),
        Revista(
            7, "National Geographic", "Varios autores", 2023,
            "00279358", 12, 224
        ),
        Revista(
            8, "Muy Interesante", "Varios autores", 2024,
            "11301920", 6, 43
        ),
        Tesis(
            9, "Sistema de gestión bibliotecaria",
            "María López", 2024, "Licenciatura",
            "Dr. Juan Pérez", "Universidad de México"
        ),
        Tesis(
            10, "Aplicación de inteligencia artificial en educación",
            "Carlos Hernández", 2023, "Maestría",
            "Dra. Laura Gómez", "Universidad de México"
        ),
    ]

    return materiales


def crear_usuarios_ejemplo():
    """Crea un estudiante, un profesor y un administrativo."""
    usuarios = [
        Estudiante(1, "Ana López", "ana@ejemplo.com"),
        Profesor(2, "Luis Pérez", "luis@ejemplo.com"),
        Administrativo(3, "Marta Ruiz", "marta@ejemplo.com"),
    ]

    return usuarios

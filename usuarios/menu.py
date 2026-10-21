"""Menú de consola de usuarios. (T14)"""

from comun.excepciones import ErrorBiblioteca
from usuarios.consultas import consultar_usuario
from usuarios.modelos import Estudiante, Profesor, Administrativo


def menu_usuarios(padron) -> None:
    """Permite registrar y consultar usuarios de la biblioteca."""

    while True:
        print("\n=== Usuarios ===")
        print("1. Registrar estudiante")
        print("2. Registrar profesor")
        print("3. Registrar administrativo")
        print("4. Consultar usuario")
        print("5. Regresar")

        opcion = input("Opción: ")

        try:
            if opcion == "1":
                id_usuario = int(input("ID del usuario: "))
                nombre = input("Nombre: ")
                correo = input("Correo: ")
                usuario = Estudiante(id_usuario, nombre, correo)
                padron.registrar(usuario)
                print(f"Estudiante registrado con id {usuario.id}")

            elif opcion == "2":
                id_usuario = int(input("ID del usuario: "))
                nombre = input("Nombre: ")
                correo = input("Correo: ")
                usuario = Profesor(id_usuario, nombre, correo)
                padron.registrar(usuario)
                print(f"Profesor registrado con id {usuario.id}")

            elif opcion == "3":
                id_usuario = int(input("ID del usuario: "))
                nombre = input("Nombre: ")
                correo = input("Correo: ")
                usuario = Administrativo(id_usuario, nombre, correo)
                padron.registrar(usuario)
                print(f"Administrativo registrado con id {usuario.id}")

            elif opcion == "4":
                id_usuario = int(input("ID del usuario: "))
                consultar_usuario(padron, id_usuario)

            elif opcion == "5":
                break

            else:
                print("Opción no válida")

        except ErrorBiblioteca as error:
            print(f"Error: {error}")
        except ValueError:
            print("Dato numérico inválido")
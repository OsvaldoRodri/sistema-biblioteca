"""Punto de entrada del Sistema de Biblioteca. (T23)"""
from comun.datos_ejemplo import crear_materiales_ejemplo, crear_usuarios_ejemplo
from materiales.catalogo import Catalogo
from materiales.menu import menu_materiales
from prestamos.menu import menu_prestamos
from prestamos.servicio import ServicioPrestamos
from reportes.menu import menu_reportes
from reportes.reportes import Reportes
from usuarios.menu import menu_usuarios
from usuarios.padron import Padron


def main() -> None:
    catalogo = Catalogo()
    padron = Padron()
    servicio = ServicioPrestamos(catalogo, padron)
    reportes = Reportes(servicio)

    for material in crear_materiales_ejemplo():
        catalogo.registrar(material)
    for usuario in crear_usuarios_ejemplo():
        padron.registrar(usuario)

    while True:
        print("\n=== Sistema de Biblioteca ===")
        print("1. Materiales")
        print("2. Usuarios")
        print("3. Préstamos")
        print("4. Reportes")
        print("5. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            menu_materiales(catalogo)
        elif opcion == "2":
            menu_usuarios(padron)
        elif opcion == "3":
            menu_prestamos(servicio)
        elif opcion == "4":
            menu_reportes(reportes)
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()

"""Menú de consola de préstamos. (T18)"""
from datetime import date

from comun.excepciones import ErrorBiblioteca
from prestamos.servicio import ServicioPrestamos


def menu_prestamos(servicio: ServicioPrestamos) -> None:
    """Ciclo del menú de préstamos: prestar, devolver, historial y regresar.

    Este es el único lugar donde se lee la fecha real; el servicio la recibe como `hoy`.
    """
    while True:
        print("\n--- Préstamos ---")
        print("1. Prestar material")
        print("2. Devolver material")
        print("3. Historial de un usuario")
        print("4. Regresar")
        opcion = input("Elige una opción: ")

        try:
            if opcion == "1":
                _prestar(servicio)
            elif opcion == "2":
                _devolver(servicio)
            elif opcion == "3":
                _historial(servicio)
            elif opcion == "4":
                return
            else:
                print("Opción inválida, intenta de nuevo.")
        except ErrorBiblioteca as e:
            print(f"Error: {e}")
        except ValueError:
            print("Pon un número, por favor.")


def _prestar(servicio: ServicioPrestamos) -> None:
    id_usuario = int(input("Id del usuario: "))
    id_material = int(input("Id del material: "))
    prestamo = servicio.prestar(id_usuario, id_material, date.today())
    print(
        f'Préstamo {prestamo.id}: "{prestamo.material.titulo}" para '
        f"{prestamo.usuario.nombre}. Se devuelve a más tardar el "
        f"{prestamo.fecha_vencimiento:%d/%m/%Y}."
    )


def _devolver(servicio: ServicioPrestamos) -> None:
    id_prestamo = int(input("Id del préstamo: "))
    multa = servicio.devolver(id_prestamo, date.today())
    if multa > 0:
        print(f"Devuelto con retraso. Multa: ${multa:.2f}")
    else:
        print("Devuelto a tiempo, sin multa.")


def _historial(servicio: ServicioPrestamos) -> None:
    id_usuario = int(input("Id del usuario: "))
    prestamos = servicio.historial(id_usuario)
    if not prestamos:
        print("Ese usuario no tiene préstamos.")
        return

    print(f"\n{'Id':>4}  {'Material':<35} {'Prestado':<10}  {'Vence':<10}  {'Estado':<20}")
    for p in prestamos:
        if p.esta_activo():
            estado = "Activo"
        else:
            estado = f"Devuelto (${p.multa:.2f})" if p.multa else "Devuelto"
        print(
            f"{p.id:>4}  {p.material.titulo:<35} {p.fecha_prestamo:%d/%m/%Y}  "
            f"{p.fecha_vencimiento:%d/%m/%Y}  {estado:<20}"
        )

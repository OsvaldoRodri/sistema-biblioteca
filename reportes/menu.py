"""Menú de consola de reportes. (T22)"""
from datetime import date

from reportes.reportes import Reportes


def menu_reportes(reportes: Reportes) -> None:
    """Ciclo del menú de reportes: materiales más prestados, vencidos, multas, regresar."""
    while True:
        print("\n--- Reportes ---")
        print("1. Materiales más prestados")
        print("2. Usuarios con préstamos vencidos")
        print("3. Multas acumuladas")
        print("4. Regresar")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            _mostrar_mas_prestados(reportes)
        elif opcion == "2":
            _mostrar_vencidos(reportes)
        elif opcion == "3":
            _mostrar_multas(reportes)
        elif opcion == "4":
            return
        else:
            print("Opción inválida, intenta de nuevo.")


def _mostrar_mas_prestados(reportes: Reportes) -> None:
    entrada = input("¿Cuántos quieres ver (n)? ")
    try:
        n = int(entrada)
    except ValueError:
        print("Pon un número, por favor.")
        return

    resultado = reportes.mas_prestados(n)
    if not resultado:
        print("Todavía no hay préstamos registrados.")
        return

    print(f"\n{'Material':<40} {'Veces prestado':>15}")
    for titulo, veces in resultado:
        print(f"{titulo:<40} {veces:>15}")


def _mostrar_vencidos(reportes: Reportes) -> None:
    hoy = date.today()
    resultado = reportes.usuarios_con_vencidos(hoy)
    if not resultado:
        print("Nadie tiene préstamos vencidos ahorita.")
        return

    print(f"\n{'Usuario':<25} {'Material':<35} {'Días de retraso':>15}")
    for usuario, material, dias in resultado:
        print(f"{usuario:<25} {material:<35} {dias:>15}")


def _mostrar_multas(reportes: Reportes) -> None:
    por_usuario, total = reportes.multas_acumuladas()
    if not por_usuario:
        print("Nadie debe multas todavía.")
        return

    print(f"\n{'Usuario':<30} {'Multa':>10}")
    for usuario, multa in por_usuario.items():
        print(f"{usuario:<30} ${multa:>9.2f}")
    print(f"\nTotal general: ${total:.2f}")

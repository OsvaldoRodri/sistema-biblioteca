"""Menú de consola de materiales. (T11)"""

from materiales.catalogo import Catalogo
from materiales.modelos import Libro, Revista, Tesis
from comun.excepciones import ErrorBiblioteca

def menu_materiales(catalogo: Catalogo) -> None:
    """Menú de materiales: registrar libro/revista/tesis, buscar, disponibilidad y salir.
    """
    
    # El ciclo se repite hasta que el usuario elija la opción 6 (regresar).
    while True:
        print("\n=== Materiales ===")
        print("1. Registrar libro")
        print("2. Registrar revista")
        print("3. Registrar tesis")
        print("4. Buscar")
        print("5. Ver disponibilidad")
        print("6. Regresar")
        
        opcion = input("Opción: ")
        
        # El try cubre toda la acción elegida para atrapar errores sin salir del menú.
        try:
            if opcion == "1":
                # Pide los datos del libro; el id va en None para que el catálogo lo asigne.
                titulo = input("Título: ")
                autor = input("Autor: ")
                anio = int(input("Año: "))          # int() puede lanzar ValueError si escriben letras
                isbn = input("ISBN: ")
                editorial = input("Editorial: ")
                libro = Libro(None, titulo, autor, anio, isbn, editorial)
                catalogo.registrar(libro)            # Puede lanzar DatoInvalido si el ISBN ya existe
                print(f"Libro registrado con id {libro.id}")
            elif opcion == "2":
                # Igual que el libro, pero con los datos de una revista.
                titulo = input("Título: ")
                autor = input("Autor: ")
                anio = int(input("Año: "))
                issn = input("ISSN: ")
                numero = int(input("Número: "))
                volumen = int(input("Volumen: "))
                revista = Revista(None, titulo, autor, anio, issn, numero, volumen)
                catalogo.registrar(revista)
                print(f"Revista registrada con id {revista.id}")
            elif opcion == "3":
                # Datos de una tesis.
                titulo = input("Título: ")
                autor = input("Autor: ")
                anio = int(input("Año: "))
                grado = input("Grado: ")
                asesor = input("Asesor: ")
                institucion = input("Institución: ")
                tesis = Tesis(None, titulo, autor, anio, grado, asesor, institucion)
                catalogo.registrar(tesis)
                print(f"Tesis registrada con id {tesis.id}")
            elif opcion == "4":
                # Pide el campo (titulo/autor/isbn) y el texto; buscar() valida el campo.
                campo = input("Buscar por (titulo/autor/isbn): ")
                texto = input("Texto a buscar: ")
                resultados = catalogo.buscar(texto, campo)

                # Si hay resultados, los imprime con su descripción; si no, avisa.
                if resultados:
                    for material in resultados:
                        print(material.descripcion())
                else:
                    print("Sin resultados")
            elif opcion == "5":
                # Pide el id y muestra si está Disponible o Prestado.
                id_material = int(input("Id del material: "))
                print(f"Estado: {catalogo.disponibilidad(id_material)}")
            elif opcion == "6":
                # Sale del ciclo y termina el menú.
                break
            else:
                print("Opción no válida")

        except ErrorBiblioteca as e:
            # Atrapa los errores del sistema: ISBN repetido (DatoInvalido),
            # material no encontrado (NoEncontrado), etc. Muestra el mensaje y sigue.
            print(f"Error: {e}")
        except ValueError:
            # Atrapa el error cuando int(input(...)) recibe letras en vez de números
            # (año, número, volumen o id mal escritos).
            print("Dato numérico inválido")


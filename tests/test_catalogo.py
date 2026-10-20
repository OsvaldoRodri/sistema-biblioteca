import pytest

from materiales.modelos import Libro
from materiales.catalogo import Catalogo
from comun.excepciones import DatoInvalido, NoEncontrado

def libro(isbn="978-607-16-0293-6", titulo="Pedro Páramo"):
    return Libro(None, titulo=titulo, autor="Juan Rulfo", anio=1955, isbn=isbn, editorial="FCE")


def test_registrar_dos_libros_mismo_isbn_falla_el_segundo():
    # Un catálogo vacío recibe bien el primer libro con cierto ISBN.
    cat = Catalogo()
    cat.registrar(libro())
    
    # El segundo libro trae el MISMO ISBN: debe lanzar DatoInvalido.
    with pytest.raises(DatoInvalido):
        cat.registrar(libro(titulo="Otro título"))
    
    # Como falló antes de guardar, el catálogo sigue con UN solo material
    # y el primero se puede consultar normalmente con su id (1).
    assert len(cat._materiales) == 1
    assert cat.obtener(1).titulo == "Pedro Páramo"

def test_libros_con_isbn_distintito_si_se_registran():
    # Dos ISBN diferentes NO deben chocar: ambos se guardan sin error.
    cat = Catalogo()
    cat.registrar(libro(isbn="978-607-16-0293-6"))
    cat.registrar(libro(isbn="978-030-747472-8"))
    
    assert len(cat._materiales) == 2

def test_obtener_regresa_el_material():
    # Guardamos un material y obtener() debe devolver ESE mismo objeto.
    cat = Catalogo()
    material = libro()
    cat.registrar(material)
    
    assert cat.obtener(1) is material

def test_obtener_id_inexistente_lanza_no_encontrado():
    # Solo existe el id 1; pedir el 99 no debe regresar nada, sino fallar
    # con NoEncontrado (el error que atrapan los menús).
    cat = Catalogo()
    cat.registrar(libro())
    
    with pytest.raises(NoEncontrado):
        cat.obtener(99)

def test_registrar_asigna_id_si_no_trae():
    # Los dos libros llegaron con id = None; el catálogo les asigna
    # ids consecutivos empezando en 1, en orden de registro.
    cat = Catalogo()
    cat.registrar(libro())
    cat.registrar(libro(isbn="978-030-747472-8"))

    assert cat._materiales[0].id == 1
    assert cat._materiales[1].id == 2
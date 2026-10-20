import pytest

from materiales.modelos import Libro, Revista
from materiales.catalogo import Catalogo
from comun.excepciones import DatoInvalido, NoEncontrado

def libro(isbn="978-607-16-0293-6", titulo="Pedro Páramo"):
    return Libro(None, titulo=titulo, autor="Juan Rulfo", anio=1955, isbn=isbn, editorial="FCE")


# T08: registrar y obtener

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
    

# T09: buscar

@pytest.fixture
def catalogo_con_datos():
    """Crea un catálogo ya con datos

    pytest.fixture significa que este catálogo se crea una sola vez
    y se lo "presta" a cada test que ponga `catalogo_con_datos` en sus
    parámetros; no hay que crearlo manualmente dentro de cada test.
    """
    cat = Catalogo()
    # Un libro con acentos en el autor, para probar que "garcia" sí lo encuentra.
    cat.registrar(libro(autor="Gabriel García Márquez", titulo="Cien años de soledad"))
    # Una revista, para tener más de un material en el catálogo.
    cat.registrar(Revista(None, "National Geographic", "Varios", 2024, "0027-9358", 5, 244))
    return cat

def test_buscar_por_titulo_parcial(catalogo_con_datos):
    # Búsqueda parcial: solo con "cien" (no el título completo)
    # debe encontrar el libro "Cien años de soledad".
    assert len(catalogo_con_datos.buscar("cien", "titulo")) == 1


def test_buscar_por_autor_en_mayusculas(catalogo_con_datos):
    # Las mayúsculas no importan: "GARCIA" debe encontrar "García".
    assert len(catalogo_con_datos.buscar("GARCIA", "autor")) == 1


def test_buscar_sin_acentos_encuentra_con_acento(catalogo_con_datos):
    # "garcia" escrito SIN acento debe encontrar "García" escrito CON acento.
    assert len(catalogo_con_datos.buscar("garcia", "autor")) == 1


def test_buscar_por_isbn(catalogo_con_datos):
    # Búsqueda parcial por ISBN: "978-607" es solo una parte del ISBN completo.
    assert len(catalogo_con_datos.buscar("978-607", "isbn")) == 1


def test_buscar_inexistente_regresa_lista_vacia(catalogo_con_datos):
    # Si no hay coincidencias, buscar() regresa una lista vacía [],
    # nunca None ni un error.
    assert catalogo_con_datos.buscar("zzz", "titulo") == []


def test_buscar_campo_invalido_lanza_value_error(catalogo_con_datos):
    # Solo se permite "titulo", "autor" o "isbn"; cualquier otro campo
    # (como "editorial") debe lanzar DatoInvalido.
    with pytest.raises(DatoInvalido):
        catalogo_con_datos.buscar("algo", "editorial")

# T10: disponibilidad de un material

def test_disponibilidad_recien_registrado_esta_disponible():
    # Un material recién registrado siempre está "Disponible".
    cat = Catalogo()
    cat.registrar(libro())

    assert cat.disponibilidad(1) == "Disponible"


def test_disponibilidad_prestado_y_devuelto():
    # Al prestar el material, disponibilidad cambia a "Prestado";
    # al devolverlo, vuelve a decir "Disponible".
    cat = Catalogo()
    material = libro()
    cat.registrar(material)

    material.marcar_prestado()
    assert cat.disponibilidad(1) == "Prestado"

    material.marcar_devuelto()
    assert cat.disponibilidad(1) == "Disponible"


def test_disponibilidad_id_inexistente_lanza_no_encontrado():
    # Como disponibilidad() usa obtener(), un id que no existe
    # también lanza NoEncontrado.
    cat = Catalogo()
    cat.registrar(libro())

    with pytest.raises(NoEncontrado):
        cat.disponibilidad(99)

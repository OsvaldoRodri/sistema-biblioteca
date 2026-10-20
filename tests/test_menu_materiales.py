from materiales.menu import menu_materiales
from materiales.catalogo import Catalogo
from materiales.modelos import Libro

def libro(isbn="978-607-16-0293-6", titulo="Pedro Páramo"):
    return Libro(None, titulo=titulo, autor="Juan Rulfo", anio=1955, isbn=isbn, editorial="FCE")



def test_menu_registra_libro_y_sale(monkeypatch, capsys):
    """Prueba el menú simulando el teclado.

    - monkeypatch reemplaza input() por una función que devuelve
      las respuestas de la lista `respuestas`, en orden, una por cada pregunta.
    - capsys captura todo lo que el menú imprime con print(), para poder
      revisarlo después con capsys.readouterr().out.
    """
    # Secuencia: opción 1 (registrar libro), sus 5 datos, y opción 6 (regresar).
    respuestas = iter([
        "1",
        "El llano en llamas", "Juan Rulfo", "1953", "978-84-376-0494-7", "FCE",
        "6",
    ])
    # Cada vez que el menú llame a input(), obtendrá la siguiente respuesta.
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

    cat = Catalogo()
    menu_materiales(cat)

    # El libro quedó guardado en el catálogo con su id asignado,
    # y el menú imprimió el mensaje de confirmación.
    assert len(cat._materiales) == 1
    assert cat.obtener(1).titulo == "El llano en llamas"
    assert "registrado con id 1" in capsys.readouterr().out


def test_menu_isbn_repetido_no_truena(monkeypatch, capsys):
    # Intenta registrar dos libros con el MISMO ISBN ("111").
    # El menú debe atrapar el DatoInvalido, mostrar "Error" y seguir
    # en el menú sin errores de Python; solo queda UN libro guardado.
    respuestas = iter([
        "1", "Libro A", "Autor", "2000", "111", "Ed1",
        "1", "Libro B", "Autor", "2001", "111", "Ed2",   # ISBN repetido: falla
        "6",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

    cat = Catalogo()
    menu_materiales(cat)

    assert len(cat._materiales) == 1
    assert "Error" in capsys.readouterr().out


def test_menu_buscar_y_disponibilidad(monkeypatch, capsys):
    # Recorre el menú: busca por título (encuentra), busca con campo
    # inválido (lo atrapa), y consulta disponibilidad del id 1.
    respuestas = iter([
        "4", "titulo", "pedro",    # buscar "pedro" en títulos: encuentra "Pedro Páramo"
        "4", "mal_campo", "x",     # campo inválido: muestra Error y sigue
        "5", "1",                  # disponibilidad del id 1: "Disponible"
        "6",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

    cat = Catalogo()
    cat.registrar(libro())          # Registra "Pedro Páramo" con id 1
    menu_materiales(cat)

    salida = capsys.readouterr().out
    assert "Pedro Páramo" in salida   # Aparece en los resultados de búsqueda
    assert "Error" in salida          # Aparece el error del campo inválido
    assert "Disponible" in salida     # Aparece la disponibilidad del id 1
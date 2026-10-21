
from usuarios.modelos import Estudiante, Profesor, Administrativo
from usuarios.padron import Padron
from comun.excepciones import DatoInvalido, NoEncontrado


def test_limite_prestamos_por_tipo():
    """Cada tipo de usuario debe tener su límite correspondiente."""
    estudiante = Estudiante(1, "Ana López", "ana@ejemplo.com")
    profesor = Profesor(2, "Luis Pérez", "luis@ejemplo.com")
    administrativo = Administrativo(3, "Marta Ruiz", "marta@ejemplo.com")

    assert estudiante.limite_prestamos == 3
    assert profesor.limite_prestamos == 5
    assert administrativo.limite_prestamos == 4


def test_dias_vigencia_por_tipo():
    """Cada tipo de usuario debe tener sus días de vigencia."""
    estudiante = Estudiante(1, "Ana López", "ana@ejemplo.com")
    profesor = Profesor(2, "Luis Pérez", "luis@ejemplo.com")
    administrativo = Administrativo(3, "Marta Ruiz", "marta@ejemplo.com")

    assert estudiante.dias_vigencia == 7
    assert profesor.dias_vigencia == 15
    assert administrativo.dias_vigencia == 10


def test_registrar_y_obtener_usuario():
    padron = Padron()
    usuario = Estudiante(1, "Ana López", "ana@ejemplo.com")

    padron.registrar(usuario)

    assert padron.obtener(1) is usuario


def test_rechazar_nombre_vacio():
    padron = Padron()
    usuario = Estudiante(1, "   ", "ana@ejemplo.com")

    try:
        padron.registrar(usuario)
        assert False, "Debió rechazar el nombre vacío."
    except DatoInvalido:
        pass


def test_rechazar_correo_sin_arroba():
    padron = Padron()
    usuario = Estudiante(1, "Ana López", "anaejemplo.com")

    try:
        padron.registrar(usuario)
        assert False, "Debió rechazar el correo inválido."
    except DatoInvalido:
        pass


def test_rechazar_id_duplicado():
    padron = Padron()
    usuario1 = Estudiante(1, "Ana López", "ana@ejemplo.com")
    usuario2 = Profesor(1, "Luis Pérez", "luis@ejemplo.com")

    padron.registrar(usuario1)

    try:
        padron.registrar(usuario2)
        assert False, "Debió rechazar el ID duplicado."
    except DatoInvalido:
        pass


def test_usuario_no_encontrado():
    padron = Padron()

    try:
        padron.obtener(999)
        assert False, "Debió indicar que el usuario no existe."
    except NoEncontrado:
        pass


from usuarios.menu import menu_usuarios


def test_menu_registra_estudiante_y_sale(monkeypatch, capsys):
    respuestas = iter([
        "1", "10", "Ana Lopez", "ana@ejemplo.com",
        "5",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

    padron = Padron()
    menu_usuarios(padron)

    assert padron.obtener(10).nombre == "Ana Lopez"
    assert "Estudiante registrado con id 10" in capsys.readouterr().out


def test_menu_registra_los_tres_tipos(monkeypatch, capsys):
    respuestas = iter([
        "1", "10", "Ana Lopez", "ana@ejemplo.com",
        "2", "20", "Luis Perez", "luis@ejemplo.com",
        "3", "30", "Marta Ruiz", "marta@ejemplo.com",
        "5",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

    padron = Padron()
    menu_usuarios(padron)

    assert isinstance(padron.obtener(10), Estudiante)
    assert isinstance(padron.obtener(20), Profesor)
    assert isinstance(padron.obtener(30), Administrativo)


def test_menu_consulta_usuario(monkeypatch, capsys):
    respuestas = iter(["4", "1", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

    padron = Padron()
    padron.registrar(Estudiante(1, "Ana Lopez", "ana@ejemplo.com"))

    menu_usuarios(padron)
    salida = capsys.readouterr().out

    assert "Nombre: Ana Lopez" in salida
    assert "Límite de préstamos: 3" in salida


def test_menu_id_inexistente_no_truena(monkeypatch, capsys):
    respuestas = iter(["4", "999", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

    menu_usuarios(Padron())
    salida = capsys.readouterr().out

    assert "Error:" in salida
    assert "999" in salida


def test_menu_opcion_y_dato_numerico_invalidos(monkeypatch, capsys):
    respuestas = iter(["9", "1", "letras", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

    menu_usuarios(Padron())
    salida = capsys.readouterr().out

    assert "Opción no válida" in salida
    assert "Dato numérico inválido" in salida


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

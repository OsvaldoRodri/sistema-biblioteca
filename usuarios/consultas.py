
from comun.excepciones import NoEncontrado


def consultar_usuario(padron, id_usuario):
    """Muestra los datos principales de un usuario de la biblioteca."""
    try:
        usuario = padron.obtener(id_usuario)
    except NoEncontrado as error:
        print(f"Error: {error}")
        return

    if isinstance(usuario, type(None)):
        print("Error: no se encontró el usuario.")
        return

    if usuario.__class__.__name__ == "Estudiante":
        tipo = "Estudiante"
    elif usuario.__class__.__name__ == "Profesor":
        tipo = "Profesor"
    elif usuario.__class__.__name__ == "Administrativo":
        tipo = "Administrativo"
    else:
        tipo = usuario.__class__.__name__

    print(f"ID: {usuario.id}")
    print(f"Tipo: {tipo}")
    print(f"Nombre: {usuario.nombre}")
    print(f"Correo: {usuario.correo}")
    print(f"Límite de préstamos: {usuario.limite_prestamos}")
    print(f"Días de vigencia: {usuario.dias_vigencia}")

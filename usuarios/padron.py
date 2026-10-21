
"""Padrón para registrar y consultar usuarios."""

from comun.excepciones import DatoInvalido, NoEncontrado


class Padron:
    """Administra el registro de usuarios de la biblioteca."""

    def __init__(self):
        self._usuarios = {}

    def registrar(self, usuario):
        """Registra un usuario después de validar sus datos."""
        if not usuario.nombre or not usuario.nombre.strip():
            raise DatoInvalido("El nombre del usuario no puede estar vacío.")

        if not usuario.correo or "@" not in usuario.correo:
            raise DatoInvalido("El correo electrónico no es válido.")

        if usuario.id in self._usuarios:
            raise DatoInvalido(
                f"Ya existe un usuario con el ID {usuario.id}."
            )

        self._usuarios[usuario.id] = usuario

    def obtener(self, id_usuario):
        """Devuelve el usuario con el ID indicado."""
        if id_usuario not in self._usuarios:
            raise NoEncontrado(
                f"No existe un usuario con el ID {id_usuario}."
            )

        return self._usuarios[id_usuario]

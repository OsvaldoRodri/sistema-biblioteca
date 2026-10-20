"""Usuario (abstracta), Estudiante, Profesor y Administrativo. (T04)"""


"""Usuario abstracto y sus tipos concretos."""

from abc import ABC, abstractmethod

from comun import config


class Usuario(ABC):
    """Clase base abstracta para los usuarios de la biblioteca."""

    def __init__(self, id_usuario: int, nombre: str, correo: str):
        self.id = id_usuario
        self.nombre = nombre
        self.correo = correo

    @property
    @abstractmethod
    def limite_prestamos(self) -> int:
        """Máximo de préstamos activos permitidos."""
        pass

    @property
    @abstractmethod
    def dias_vigencia(self) -> int:
        """Días de vigencia de un préstamo."""
        pass


class Estudiante(Usuario):
    """Usuario con perfil de estudiante."""

    @property
    def limite_prestamos(self) -> int:
        return config.LIMITE_PRESTAMOS_ESTUDIANTE

    @property
    def dias_vigencia(self) -> int:
        return config.DIAS_VIGENCIA_ESTUDIANTE


class Profesor(Usuario):
    """Usuario con perfil de profesor."""

    @property
    def limite_prestamos(self) -> int:
        return config.LIMITE_PRESTAMOS_PROFESOR

    @property
    def dias_vigencia(self) -> int:
        return config.DIAS_VIGENCIA_PROFESOR


class Administrativo(Usuario):
    """Usuario con perfil administrativo."""

    @property
    def limite_prestamos(self) -> int:
        return config.LIMITE_PRESTAMOS_ADMINISTRATIVO

    @property
    def dias_vigencia(self) -> int:
        return config.DIAS_VIGENCIA_ADMINISTRATIVO

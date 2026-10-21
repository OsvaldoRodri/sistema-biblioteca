"""Prestamo. (T05)"""

from datetime import date

from materiales.modelos import Material
from usuarios.modelos import Usuario


class Prestamo:
    """Un material en manos de un usuario, desde que se presta hasta que se devuelve.

    La fecha de vencimiento la calcula ServicioPrestamos (T15) con los días de
    vigencia del usuario; aquí solo se guarda. Las fechas de consulta siempre
    llegan como parámetro `hoy` para poder probar retrasos sin esperar días.
    """

    def __init__(
        self,
        id_prestamo: int,
        usuario: Usuario,
        material: Material,
        fecha_prestamo: date,
        fecha_vencimiento: date,
        fecha_devolucion: date | None = None,
        multa: float = 0,
    ):
        self.id = id_prestamo
        self.usuario = usuario
        self.material = material
        self.fecha_prestamo = fecha_prestamo
        self.fecha_vencimiento = fecha_vencimiento
        self.fecha_devolucion = fecha_devolucion
        self.multa = multa

    def esta_activo(self) -> bool:
        """True mientras el material no se haya devuelto."""
        return self.fecha_devolucion is None

    def dias_retraso(self, hoy: date) -> int:
        """Días que han pasado después del vencimiento; nunca negativo."""
        return max(0, (hoy - self.fecha_vencimiento).days)

    def esta_vencido(self, hoy: date) -> bool:
        """True si sigue activo y `hoy` ya pasó la fecha de vencimiento."""
        return self.esta_activo() and hoy > self.fecha_vencimiento

"""Reportes: materiales más prestados, usuarios con préstamos vencidos y multas acumuladas. (T06, T19–T21)"""
from datetime import date

from prestamos.servicio import ServicioPrestamos


class Reportes:
    """Saca reportes a partir de los préstamos que lleva ServicioPrestamos."""

    def __init__(self, servicio: ServicioPrestamos):
        self._servicio = servicio

    def mas_prestados(self, n: int) -> list[tuple[str, int]]:
        # Cuenta cuántas veces se prestó cada material (T19)
        conteos: dict[int, list] = {}  # id_material -> [material, veces]
        for prestamo in self._servicio.todos():
            material = prestamo.material
            if material.id not in conteos:
                conteos[material.id] = [material, 0]
            conteos[material.id][1] += 1

        # de mayor a menor veces prestado; empates por título
        ordenados = sorted(conteos.values(), key=lambda par: (-par[1], par[0].titulo))
        return [(material.titulo, veces) for material, veces in ordenados[:n]]

    def usuarios_con_vencidos(self, hoy: date) -> list[tuple[str, str, int]]:
        # Solo los préstamos activos que ya vencieron a la fecha hoy (T20)
        resultado = []
        for prestamo in self._servicio.todos():
            if prestamo.esta_vencido(hoy):
                resultado.append((
                    prestamo.usuario.nombre,
                    prestamo.material.titulo,
                    prestamo.dias_retraso(hoy),
                ))
        return resultado

    def multas_acumuladas(self) -> tuple[dict[str, float], float]:
        # Suma las multas de los préstamos ya devueltos, por usuario (T21)
        # Se agrupa por id (no por nombre, por si dos usuarios se llaman igual)
        por_id: dict[int, list] = {}  # id_usuario -> [usuario, total]
        total = 0.0
        for prestamo in self._servicio.todos():
            if prestamo.fecha_devolucion is not None and prestamo.multa > 0:
                usuario = prestamo.usuario
                if usuario.id not in por_id:
                    por_id[usuario.id] = [usuario, 0.0]
                por_id[usuario.id][1] += prestamo.multa
                total += prestamo.multa

        por_usuario = {
            f"{usuario.nombre} (ID {usuario.id})": suma
            for usuario, suma in por_id.values()
        }
        return por_usuario, total

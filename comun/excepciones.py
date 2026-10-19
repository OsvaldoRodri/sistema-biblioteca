
"""Excepciones que se lanzan entre módulos del sistema de biblioteca."""


class ErrorBiblioteca(Exception):
    """Base de todos los errores del sistema; los menús atrapan esta."""


class NoEncontrado(ErrorBiblioteca):
    """Se buscó un material, usuario o préstamo con un id que no existe."""


class MaterialNoDisponible(ErrorBiblioteca):
    """Se intentó prestar un material que ya está prestado."""


class LimiteExcedido(ErrorBiblioteca):
    """El usuario ya tiene tantos préstamos activos como su límite."""


class DatoInvalido(ErrorBiblioteca):
    """Un dato no pasa la validación: ISBN repetido, correo sin @, nombre vacío."""
"""Prueba de humo: confirma que los paquetes del proyecto se pueden importar.

Cada módulo agrega su propio test_<modulo>.py junto a este archivo.
"""
import importlib

import pytest

MODULOS = [
    "comun.config",
    "comun.excepciones",
    "comun.datos_ejemplo",
    "materiales.modelos",
    "materiales.catalogo",
    "materiales.menu",
    "usuarios.modelos",
    "usuarios.padron",
    "usuarios.menu",
    "prestamos.modelos",
    "prestamos.servicio",
    "prestamos.menu",
    "reportes.reportes",
    "reportes.menu",
]


@pytest.mark.parametrize("nombre", MODULOS)
def test_modulo_se_importa(nombre):
    importlib.import_module(nombre)

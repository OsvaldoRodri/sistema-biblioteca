"""Confirma que todas las excepciones heredan de ErrorBiblioteca."""
# pyrefly: ignore[missing-import]
import pytest

from comun.excepciones import (
    DatoInvalido,
    ErrorBiblioteca,
    LimiteExcedido,
    MaterialNoDisponible,
    NoEncontrado,
)


@pytest.mark.parametrize(
    "excepcion",
    [NoEncontrado, MaterialNoDisponible, LimiteExcedido, DatoInvalido],
)
def test_hereda_de_error_biblioteca(excepcion):
    assert issubclass(excepcion, ErrorBiblioteca)
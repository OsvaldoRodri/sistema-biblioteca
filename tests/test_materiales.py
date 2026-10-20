

from abc import ABC
import pytest

from materiales.modelos import Libro, Revista, Tesis, Material


def test_material_es_clase_abstracta():
    """Verifica que Material no se pueda instanciar directamente y herede de ABC"""
    assert issubclass(Material, ABC)
    
    with pytest.raises(TypeError):
        Material(1, "Título", "Autor", 2026)
        
        
def test_libro_funcionalidad_y_descripcion():
    """Prueba la creación de un Libro, sus métodos de préstamo y descripción."""
    libro = Libro(
        id_material=101,
        titulo="Cien años de soledad",
        autor="Gabriel García Márquez",
        anio=1967,
        isbn="978-030-7474728",
        editorial="Sudamericana",
    )
    
    # Probar estado inicial (Debe ser True, ya que el valor por defecto se asigno que fuera True)
    assert libro.esta_disponible() is True
    
    # Probar que al marcar prestado realmente si se hizo el préstamo
    # y posteriormente se comprueba que no esté disponible.
    assert libro.marcar_prestado() is True
    assert libro.esta_disponible() is False
    
    # Prueba que nos muestra que no se puede volver a prestar (debería ser False ya que se prestó anteriormente)
    assert libro.marcar_prestado() is False
    
    # Ahora se marca como que se devolvió el libro
    libro.marcar_devuelto()
    assert libro.esta_disponible() is True
    
    # Probar método abstracto (descripcion)
    desc = libro.descripcion()
    assert "[Libro]" in desc
    assert "Sudamericana" in desc

def test_revista_funcionalidad_y_descripcion():
  """Prueba la creación de una Revista y su descripción única."""
  revista = Revista(
      id_material=202,
      titulo="National Geographic",
      autor="Varios",
      anio=2024,
      issn="0027-9358",
      numero=5,
      volumen=244,
  )

  assert revista.esta_disponible() is True
  desc = revista.descripcion()
  assert "[Revista]" in desc
  assert "Vol. 244, Nº 5" in desc
  
def test_tesis_funcionalidad_y_descripcion():
  """Prueba la creación de una Tesis y su descripción única."""
  tesis = Tesis(
      id_material=303,
      titulo="Inteligencia Artificial en Medicina",
      autor="Sofía Pérez",
      anio=2025,
      grado="Maestría",
      asesor="Dr. Gómez",
      institucion="UNAM",
  )

  assert tesis.esta_disponible() is True
  desc = tesis.descripcion()
  assert "[Tesis de Maestría]" in desc
  assert "Asesor: Dr. Gómez" in desc
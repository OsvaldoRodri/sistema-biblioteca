"""Material (abstracta), Libro, Revista y Tesis. (T03)"""
from abc import ABC, abstractmethod

class Material(ABC):
    def __init__(
        self,
        id_material: int,
        titulo: str,
        autor: str,
        anio: int,
        disponible: bool = True
    ):
        self.id = id_material
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self._disponible = disponible # ATributo privado / protegido
    
    
    def esta_disponible(self) -> bool:
        """
            Devuelve si el material se encuentra disponible para
            hacer un préstamo.
        """
        
        return self._disponible
    
    def marcar_prestado(self) -> bool:
        """
            Cambiar el estado del material a no disponible si estaba libre.
            
            Devuelve True si el préstamo se realizó y False si no.
        """
        
        if (self._disponible):
            self._disponible = False
            return True
        return False
    
    def marcar_devuelto(self):
        """Cambia el estado del material a disponible"""
        self._disponible = True
    
    @abstractmethod
    def descripcion(self):
        """Cada clase hija deberá implementar este método, el como se describe a sí misma"""
        pass
        
    
class Libro(Material):
    def __init__(        
        self,
        id_material: int,
        titulo: str,
        autor: str,
        anio: int,

        isbn: str,
        editorial: str,
        
        disponible: bool = True
        
    ):
        super().__init__(id_material, titulo, autor, anio, disponible)
        self.isbn = isbn
        self.editorial = editorial
        
    def descripcion(self) -> str:
        estado: str = "Disponible"
        
        if not self._disponible :
            estado = "Prestado"
            
        return (
            f"[Libro] {self.titulo} - {self.autor} ({self.anio}) | "
            f"Editorial: {self.editorial} | ISBN: {self.isbn} | Estado: {estado}"     
        )

class Revista(Material):
    def __init__(        
        self,
        id_material: int,
        titulo: str,
        autor: str,
        anio: int,
        
        issn: str,
        numero: int,
        volumen: int,
        
        disponible: bool = True
    ):
        super().__init__(id_material, titulo, autor, anio, disponible)
        self.issn = issn
        self.numero = numero
        self.volumen = volumen
    
    def descripcion(self) -> str:
        estado: str = "Disponible"
        
        if not self._disponible :
            estado = "Prestado"
            
        return (
            f"[Revista] {self.titulo} (Vol. {self.volumen}, Nº {self.numero}) - "
            f"{self.autor} ({self.anio}) | ISSN: {self.issn} | Estado: {estado}"     
        )

class Tesis(Material):

    def __init__(
        self,
        id_material: int,
        titulo: str,
        autor: str,
        anio: int,
        
        grado: str,
        asesor: str,
        institucion: str,
        
        disponible: bool = True,
    ):
        super().__init__(id_material, titulo, autor, anio, disponible)
        self.grado = grado
        self.asesor = asesor
        self.institucion = institucion

    def descripcion(self) -> str:
        estado: str = "Disponible"
        
        if not self._disponible :
            estado = "Prestado"
        
        return (
            f"[Tesis de {self.grado}] {self.titulo} por {self.autor} ({self.anio}) | "
            f"Asesor: {self.asesor} | Inst: {self.institucion} | Estado: {estado}"
        )
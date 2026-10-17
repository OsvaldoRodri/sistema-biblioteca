# Sistema de Biblioteca

Programa de consola en Python para gestionar materiales bibliográficos (libros, revistas y tesis), usuarios (estudiantes, profesores y administrativos), préstamos con multas y reportes.

Equipo: Osvaldo Rodríguez, Arturo Loera Esparza, Víctor Guillermo Muñoz Vázquez y Arturo Carlos Rodríguez Leyva.

## Cómo correrlo

Necesitas Python 3.11 o superior. Desde la carpeta del proyecto:

```bash
python main.py
```

## Cómo correr las pruebas

```bash
pip install -r requirements.txt
pytest
```

## Estructura

| Carpeta | Qué contiene |
| --- | --- |
| `comun/` | Configuración (límites y multa), excepciones y datos de ejemplo |
| `materiales/` | Material, Libro, Revista, Tesis y el catálogo |
| `usuarios/` | Usuario, Estudiante, Profesor, Administrativo y el padrón |
| `prestamos/` | Préstamo y el servicio de préstamos y devoluciones |
| `reportes/` | Más prestados, usuarios con vencidos y multas acumuladas |
| `tests/` | Un `test_<modulo>.py` por módulo |

## Cómo trabajamos

1. Nadie sube directo a `main`.
2. Cada tarea va en su rama, nombrada con el ID del plan: `git checkout -b T15-prestar`.
3. Commits chicos, en español, diciendo qué hace el cambio.
4. Se abre un pull request hacia `main`; otra persona lo revisa, corre `pytest` y lo aprueba.
5. Si hay un conflicto en una carpeta que no es la tuya, avisa en el chat antes de resolverlo.

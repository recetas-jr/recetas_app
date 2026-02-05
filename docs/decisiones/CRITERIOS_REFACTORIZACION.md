Refactorización R5 aplicada a recetas.py

- Se eliminaron funciones duplicadas de desactivación
- Se extrajeron funciones auxiliares internas:
  - obtener_recetas_activas
  - mostrar_listado_recetas
  - seleccionar_indice
- Se redujo duplicación de lógica en listados y selecciones
- Se mantuvo intacto el comportamiento funcional
- Se limpiaron advertencias de VS Code

Refactorización R5 aplicada a persistencia.py

- Se reforzó la función cargar_datos para manejar JSON inválido o archivos corruptos
- Se documentó explícitamente la responsabilidad del módulo de persistencia
- Persistencia no valida ni interpreta datos
- Se mantuvo intacto el comportamiento funcional del sistema
- No se alteraron rutas ni nombres de archivos



Refactorización R5 aplicada a nomencladores.py

- Se unificó la normalización de textos
- Se eliminaron duplicaciones en menús y validaciones
- Se añadieron utilidades comunes (pausar, seleccionar_indice)
- Se mejoró la legibilidad y el orden interno del módulo
- No se modificó el comportamiento funcional
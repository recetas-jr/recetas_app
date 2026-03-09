docs/START_HERE.md

Es la puerta de entrada al proyecto.
Explica rápidamente:
qué es el sistema
cómo ejecutarlo
qué partes tiene
qué es admin y qué es usuario
Es el documento que debe leer cualquier persona que abra el proyecto por primera vez.


docs/INDICE_DOCUMENTACION.md

Es el mapa de toda la documentación.
Sirve para encontrar rápidamente:
arquitectura
estructura del proyecto
bitácora
documentos técnicos
glosario


docs/MAPA_DEL_SISTEMA.md

Explica todo el sistema en una sola vista:
capas del sistema
componentes
estructura del proyecto
relación entre datos
Es el documento para entender el sistema rápidamente.


docs/ARQUITECTURA_DEL_SISTEMA.md

Explica cómo está construido realmente el sistema:
capas técnicas
lógica de aplicación
persistencia
base de datos
reglas del sistema
Este es el documento más técnico de los cuatro.

Commando para listar todos los documentos del Sistema Recetas:
dir /s /b *.md

Commando para listar solo documentos versionados en el proyecto. Solo muestra documentos que están en Git. Evita archivos temporales:
git ls-files *.md

Commando para generar una lista automática:

dir /s /b docs\*.md > lista_documentos.txt
Esto crea un archivo:
lista_documentos.txt con todos los documentos que se abre en CMD

Commandos generales:
dir      → listar archivos
/s       → buscar en todas las carpetas
/b       → formato simple
*.md     → solo archivos Markdown

Para limpiar la pantalla de CMD o POWERSHELL:
cls

PENDIENTE:
Si quieres, en el siguiente paso te puedo enseñar un pequeño truco que usan los desarrolladores veteranos para que cada respaldo USB quede ligado exactamente a un commit de Git.
Eso hace que restaurar el sistema sea casi instantáneo.

PENDIENTE:
Si quieres, en el siguiente paso puedo mostrarte una mejora muy pequeña del código que hace el cálculo aún más seguro (es solo una línea), pero muy elegante desde el punto de vista técnico.

PENDIENTE:
Confirmación matemática

Tu modelo sigue cumpliendo:

BASE + DECO = TOTAL

y el recalculo se hace siempre con:

factor = raciones_solicitadas / raciones_base

Si quieres, puedo mostrarte un detalle muy importante del código que tienes ahora mismo, porque el sistema no está usando exactamente este modelo, y hay una pequeña diferencia matemática que conviene aclarar antes de seguir avanzando.

PENDIENTE:
Si quieres, en el siguiente paso también puedo darte el mapa completo de rutas del sistema recetas_app para que lo tengas documentado. Es muy útil cuando el proyecto empieza a crecer.

PENDIENTE:
Colega, ahora que vemos la pantalla completa, aparece un detalle interesante de diseño:

La tabla ahora tiene 5 columnas, y eso cambia ligeramente el equilibrio visual de la hoja.

Hay una pequeña mejora de tipografía que puede hacer que esta tabla se vea mucho más elegante dentro de la página, sin cambiar nada del sistema.
Si quieres, te la muestro porque encaja muy bien con el estilo de recetario que estás construyendo.

PENDIENTE:
Si quieres, en el siguiente paso te muestro cómo quedaría esta tabla exactamente dentro de la hoja blanca del recetario con el fondo beige del sistema. Ahí es donde realmente empieza a verse elegante.

PENDIENTE:
Porque el siguiente ajuste que podemos hacer (si quieres) es convertir esa tabla en algo que parezca literalmente una página de libro de cocina antiguo. Y eso queda espectacular.

PENDIENTE:

>>> exit() <------- con esto se sale al prompt normal





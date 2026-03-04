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





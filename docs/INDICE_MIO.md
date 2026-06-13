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

1)TITULO: SALVA WEB_APP.PY: ----\modulo_web\web_app.py en web_app_backup.py ------

2)EJECUTA LA SALVA --> copy /Y modulo_webw\eb_app.py modulo_web\web_app_backup.py

1)TITULO: RESTAURA EN WEB_APP.PY----web_app_backup.py en web_app.py -------

2)EJECUTA LA RETAURACION --> copy /Y modulo_web/web_app_backup.py modulo_web\web_app.py

1)TITULO: SALVA ADMIN_RECETAS_EDITAR.HTML: -----modulo_web\templates\admin_recetas_editar.html en modulo_web\templates\admin_recetas_editar_backup.html -------

2)EJECUTA LA SALVA: --> copy /Y modulo_web\templates\admin_recetas_editar.html modulo_web\templates\admin_recetas_editar_backup.html

1)TITULO:RESTAURA: -----modulo_web\templates\admin_recetas_editar_backup.html en modulo_web\templates\admin_recetas_editar.html------

2)EJECUTA LA RESTAURACION:--> copy /Y modulo_web\templates\admin_recetas_editar_backup.html modulo_web\templates\admin_recetas_editar.html

1)TITULO: SALVA RECETAS_PREPARACION.HTML: ---- modulo_web\templatesr\eceta_preparacion.html en modulo_web\templates\receta_preparacion_backup.html

2)EJECUTA LA SALVA --> copy /Y modulo_web\templates\receta_preparacion.html modulo_web\templates\receta_preparacion_backup.html 

1)TITULO: RESTAURA: -----receta_preparacion_backup.html en modulo_web/templates/receta_preparacion.html

2)EJECUTA LA RESTAURACION: --> copy /Y modulo_web\templates\receta_preparacion_backup.html modulo_web\templates\receta_preparacion.html

1)TITULO: SALVA RECETA_DETALLE.HTML Y EJECUTA: --> copy /Y modulo_web\templates\receta_detalle.html modulo_web\templates\receta_detalle_backup.html

2)1)TITULO: RESTAURAR RECETA_DETALLE.HTML Y EJECUTA --> copy /Y modulo_web\templates\receta_detalle_backup.html modulo_web\templates\receta_detalle.html

git commit -am "checkpoint antes de modificar editor" <-- crea otra capa de seguridad 
                                                          con el git

Encabezado fijo mientras el contenido se desplaza
(lo que en web se llama sticky header). ----> SCROLL

PARA CREAR SUBCARPETAS DESDE LA TERMINAL DE VSC        <----------
-Apertura de la terminal en VS Code
-Abrir la terminal desde el menú superior:
... → Terminal → New Terminal
VS Code preguntó sobre editores de confianza.
Seleccionaste:
N
que significa:
No ejecutar nunca
para ese aviso.
6️⃣ Creación de carpetas desde la terminal (en PS-PowerShell)

commando----> mkdir 

Creación de archivos  crear_usb_captura.py

comando -----> New-Item archivo.txt ó .py

Si estás en CMD entonces usas ---> type nul >

Para volver a la carpeta anterior
Escribe:

cd ..
Regla fácil de recordar
..   = subir una carpeta
..\.. = subir dos carpetas

code <----- Pre-fijo en la consola para entrar a un archivo


PENDIENTE:
🔹 Nivel 1

Validaciones más estrictas

Evitar errores de entrada

🔹 Nivel 2

Backup automático antes de borrar

Papelera interna

🔹 Nivel 3
  
UI más amigable (menús más claros)

🔹 Nivel 4

Integración con tu sistema principal recetas_app

Para ir a configuración ---> (Ctrl + ,)

PENDIENTE:
Si quieres, en la siguiente fase te enseño comandos pro de consola para trabajar más rápido

copy modulo_web\templates\admin_recetas_nueva.html modulo_web\templates\admin_recetas_nueva_backup.html <-- guardar admin_recetas_nueva.html



==================================================|
CONVENCIÓN OFICIAL DE MENSAJES GIT — recetas_app  |  ==================================================| 
1. Cambios de recetas (datos)
Publicar o despublicar recetas
RECETAS: sincronizar catálogo web

Usar cuando:

visible_web = 1
visible_web = 0

o cualquier cambio de visibilidad.

Agregar nuevas recetas
RECETAS: publicar nuevas recetas

Usar cuando:

Se crean recetas nuevas
y se publican en catálogo
Modificar recetas existentes
RECETAS: actualizar datos del catálogo

Usar cuando:

Ingredientes
Preparación
Elaboración
Presentación
Nutrición
Fotos
Peso ración
Cambios masivos de recetas
RECETAS: actualización general del catálogo

Usar cuando:

Muchas recetas cambian
2. Cambios de nomencladores
Ingredientes
INGREDIENTES: actualización de nomenclador

Usar cuando:

Altas
Bajas
Modificaciones
Unidades de medida
UNIDADES: actualización de nomenclador
Tipos de plato
TIPOS: actualización de nomenclador
3. Cambios administrativos
Menú principal
MENU: ajustes navegación principal
Editor de recetas
EDITOR: mejoras editor de recetas
Catálogo administrativo
ADMIN: mejoras catálogo administrativo
4. Cambios del catálogo público
Visualización pública
CATALOGO: mejoras visualización pública
Diseño público
CATALOGO: ajustes visuales
5. Cambios de infraestructura
BAT de arranque
SISTEMA: mejoras arranque local
Deploy
SISTEMA: mejoras proceso de despliegue
Render
SISTEMA: ajustes despliegue Render
6. Base de datos
Estructura BD
BD: ajustes estructura de datos

Usar cuando:

Campos nuevos
Longitudes
Tipos de datos
Índices
7. Documentación
Manual técnico
DOCS: actualización manual técnico
Evolución del sistema
DOCS: actualización evolución del sistema
Informe de migración
DOCS: actualización informe de migración
8. Commits grandes de fase

Cuando cierres una fase completa:

FASE: menú principal administrativo
FASE: navegación global
FASE: estabilización editor master
FASE: separación administración y catálogo público
Los 5 mensajes que más vas a usar
RECETAS: sincronizar catálogo web
RECETAS: actualizar datos del catálogo
RECETAS: publicar nuevas recetas
SISTEMA: mejoras proceso de despliegue
DOCS: actualización manual técnico

Con esa convención, el historial Git de recetas_app queda prácticamente autodescriptivo y muy fácil de auditar cuando estemos trabajando también con ALLENDE. 🚀

BATS:

LEYENDA DE HERRAMIENTAS BAT

PROYECTO: recetas_app

UBICACIÓN

Todos los BAT administrativos del proyecto se encuentran en:

recetas_app\bats
OBJETIVO

Centralizar las tareas técnicas y administrativas del sistema en un único punto de acceso.

menu_administracion_tecnica.bat
FUNCIÓN

Centro de Administración Técnica.

RESPONSABILIDADES
Mostrar el menú principal.
Invocar las herramientas BAT del sistema.
Retornar al menú tras finalizar cada operación.
DEPENDENCIAS
arranca_recetas.bat
abrir_bd_recetas.bat
backup_proyecto.bat
backup_recetas.bat
git_push.bat
deploy_render.bat
nomenclador_commits.bat
arranca_recetas.bat
FUNCIÓN

Arranque del sistema web recetas_app.

RESPONSABILIDADES
Verificar si Flask ya está ejecutándose.
Iniciar Flask cuando sea necesario.
Esperar la disponibilidad del puerto 5000.
Abrir automáticamente el navegador.
DEPENDENCIAS
modulo_web.web_app
OBSERVACIÓN

El correcto funcionamiento depende del directorio de trabajo utilizado al lanzar Python.

abrir_bd_recetas.bat
FUNCIÓN

Abrir la base de datos principal del sistema.

RESPONSABILIDADES
Facilitar acceso rápido a la base SQLite.
Evitar búsquedas manuales del archivo.
backup_proyecto.bat
FUNCIÓN

Generar copia de seguridad completa del proyecto.

RESPONSABILIDADES
Respaldar código fuente.
Respaldar documentación.
Respaldar configuraciones.
Respaldar estructura de trabajo.
OBJETIVO

Recuperación rápida ante errores o pérdidas de información.

backup_recetas.bat
FUNCIÓN

Generar copia de seguridad de recetas.

RESPONSABILIDADES
Respaldar información culinaria.
Preservar recetas capturadas.
Facilitar restauraciones específicas.
git_push.bat
FUNCIÓN

Publicación controlada de cambios hacia GitHub.

RESPONSABILIDADES
Detectar commits pendientes de push.
Detectar cambios sin confirmar.
Permitir selección de mensajes desde nomenclador.
Permitir mensajes manuales.
Crear commits.
Ejecutar push.
Mostrar revisión previa del commit.
ESTADO

Estabilizado y validado.

deploy_render.bat
FUNCIÓN

Publicación para despliegue web.

RESPONSABILIDADES
Gestionar commit.
Gestionar push.
Integrarse con el nomenclador de commits.
Activar actualización de la aplicación en Render.
ESTADO

Estabilizado y validado.

nomenclador_commits.bat
FUNCIÓN

Administración del catálogo de mensajes de commit.

RESPONSABILIDADES
Mostrar mensajes disponibles.
Agregar nuevos mensajes.
Eliminar mensajes existentes.
Gestionar numeración automática.
DEPENDENCIA
nomenclador_commits.txt
nomenclador_commits.txt
FUNCIÓN

Repositorio centralizado de mensajes reutilizables de commit.

UTILIZADO POR
git_push.bat
deploy_render.bat
nomenclador_commits.bat
git_push_backup.bat
FUNCIÓN

Versión histórica de respaldo del proceso Git Push.

ESTADO

Archivo de respaldo.

No es utilizado por el menú principal.

Conservar únicamente como referencia histórica mientras sea necesario.

RELACIÓN ENTRE BATS
menu_administracion_tecnica.bat

├── arranca_recetas.bat
├── abrir_bd_recetas.bat
├── backup_proyecto.bat
├── backup_recetas.bat
├── git_push.bat
├── deploy_render.bat
└── nomenclador_commits.bat
ESTADO GENERAL
Fase BAT finalizada.
Herramientas administrativas estabilizadas.
GitHub sincronizado.
Repositorio limpio.
Infraestructura técnica lista para continuar el desarrollo funcional de recetas_app.


BLOQUE PARA LISTAR UN ARCHIVO VISUALIZANDO TODOS LOS NÚMEROS DE LINEAS DEL ARCHIVO:

$linea=1
Get-Content .\RUTA_DEL_ARCHIVO |
ForEach-Object {
    "{0,4}: {1}" -f $linea, $_
    $linea++
}
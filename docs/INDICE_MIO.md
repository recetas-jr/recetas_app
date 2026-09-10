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

Ó

 951: # ==================================================
 952: 
 953: @app.route("/admin/recetas/editar/<int:receta_id>", methods=["GET", "POST"])
 954: def admin_recetas_editar(receta_id):
 955: 
 956:     platos = db_cargar_platos()
 957:     ingredientes = cargar_ingredientes_con_unidad()
 958: 
 959:     # ==================================================
 960:     # GUARDAR CAMBIOS DE RECETA
 961:     # ==================================================
 962: 
 963:     if request.method == "POST":
 964: 
 965:         plato_id = request.form.get("plato_id", "").strip()
 966:         raciones_base = request.form.get("raciones_base", "").strip()
 967: 
 968:         # NUEVO: textos de la receta
 969:         preparacion = request.form.get("preparacion", "").strip()
 970:         elaboracion = request.form.get("elaboracion", "").strip()
 971:         presentacion = request.form.get("presentacion", "").strip()
 972:         nutricion = request.form.get("nutricion", "").strip()
 973: 
 974:         if not plato_id:
 975:             flash("Debe seleccionar un plato.", "error")
 976:             return redirect(f"/admin/recetas/editar/{receta_id}")
 977: 
 978:         try:
 979:             raciones_base_int = int(raciones_base)
 980:             if raciones_base_int <= 0:
 981:                 flash("RACIONES BASE debe ser mayor que 0.", "error")
 982:                 return redirect(f"/admin/recetas/editar/{receta_id}")
 983:         except:
 984:             flash("RACIONES BASE debe ser numérico.", "error")
 985:             return redirect(f"/admin/recetas/editar/{receta_id}")
 986: 
 987:         ingredientes_ids = request.form.getlist("ingrediente_id[]")
 988:         cantidades = request.form.getlist("cantidad[]")
 989:         roles = request.form.getlist("rol[]")
 990: 
 991:         vistos = set()
 992:         filas_validas = []
 993: 
 994:         for i in range(len(ingredientes_ids)):
 995: 
 996:             ing_id = (ingredientes_ids[i] or "").strip()
 997:             cant_txt = (cantidades[i] or "").strip()
 998:             rol_txt = (roles[i] or "").strip()
 999: 
1000:             if not ing_id:
1001:                 continue
1002: 
1003:             if ing_id in vistos:
1004:                 flash("No se permiten ingredientes duplicados.", "error")
1005:                 return redirect(f"/admin/recetas/editar/{receta_id}")
1006: 
1007:             vistos.add(ing_id)
1008: 
1009:             try:
1010:                 cant_f = float(cant_txt)
1011:             except:
1012:                 flash("La cantidad debe ser numérica.", "error")
1013:                 return redirect(f"/admin/recetas/editar/{receta_id}")
1014: 
1015:             if cant_f <= 0:
1016:                 flash("La cantidad debe ser mayor que 0.", "error")
1017:                 return redirect(f"/admin/recetas/editar/{receta_id}")
1018: 
1019:             if rol_txt == "":
1020:                 rol_f = 0.0
1021:             else:
1022:                 try:
1023:                     rol_f = float(rol_txt)
1024:                 except:
1025:                     flash("El rol debe ser numérico.", "error")
1026:                     return redirect(f"/admin/recetas/editar/{receta_id}")
1027: 
1028:                 if rol_f < 0:
1029:                     flash("El rol no puede ser negativo.", "error")
1030:                     return redirect(f"/admin/recetas/editar/{receta_id}")
1031: 
1032:                 if rol_f > cant_f:
1033:                     flash("El rol no puede ser mayor que la cantidad.", "error")
1034:                     return redirect(f"/admin/recetas/editar/{receta_id}")
1035: 
1036:             filas_validas.append((int(ing_id), cant_f, rol_f))
1037: 
1038:         if not filas_validas:
1039:             flash("La receta no puede quedar sin ingredientes.", "error")
1040:             return redirect(f"/admin/recetas/editar/{receta_id}")
1041: 
1042:         try:
1043: 
1044:             conn = get_connection()
1045: 
1046:             cur = conn.cursor()
1047: 
1048:             cur.execute(
1049:                 """
1050:                 UPDATE recetas_maestro
1051:                 SET plato_id=?,
1052:                     raciones_base=?,
1053:                     preparacion=?,
1054:                     elaboracion=?,
1055:                     presentacion=?,
1056:                     nutricion=?
1057:                 WHERE id=?
1058:                 """,
1059:                 (
1060:                     int(plato_id),
1061:                     raciones_base_int,
1062:                     preparacion,
1063:                     elaboracion,
1064:                     presentacion,
1065:                     nutricion,
1066:                     receta_id
1067:                 )
1068:             )
1069: 
1070:             cur.execute(
1071:                 "DELETE FROM recetas_ingredientes WHERE receta_id=?",
1072:                 (receta_id,)
1073:             )
1074: 
1075:             for ing_id, cant_f, rol_f in filas_validas:
1076: 
1077:                 cur.execute(
1078:                     """
1079:                     INSERT INTO recetas_ingredientes
1080:                     (receta_id, ingrediente_id, cantidad, rol)
1081:                     VALUES (?,?,?,?)
1082:                     """,
1083:                     (receta_id, ing_id, cant_f, rol_f)
1084:                 )
1085: 
1086:             print("ANTES DEL COMMIT")
1087: 
1088:             conn.commit()
1089: 
1090:             flash(
1091:                 "Receta actualizada correctamente.",
1092:                 "recetas"
1093:             )
1094: 
1095:             return redirect("/admin/recetas/listado")
1096: 
1097:         except Exception as e:
1098: 
1099:             print("ERROR actualizando receta:", e)
1100: 
1101:             try:
1102: 
1103:                 conn.rollback()
1104: 
1105:             except Exception as e2:
1106: 
1107:                 print("ERROR EN ROLLBACK:", e2)
1108: 
1109:             flash(
1110:                 "Error al actualizar la receta.",
1111:                 "error"
1112:             )
1113: 
1114:             return redirect(
1115:                 f"/admin/recetas/editar/{receta_id}"
1116:             )
1117: 
1118:         finally:
1119: 
1120:             try:
1121: 
1122:                 conn.close()
1123: 
1124:             except Exception as e:
1125: 
1126:                 print("ERROR CERRANDO CONEXION:", e)
1127: 
1128:     # ==================================================
1129:     # CARGAR RECETA PARA EDICIÓN
1130:     # ==================================================
1131: 
1132:     try:
1133:         conn = get_connection()
1134:         cur = conn.cursor()
1135: 
1136:         cur.execute("""
1137:             SELECT
1138:                 r.id,
1139:                 r.plato_id,
1140:                 r.raciones_base,
1141:                 r.preparacion,
1142:                 r.elaboracion,
1143:                 r.presentacion,
1144:                 r.nutricion,
1145:                 p.nombre as plato_nombre
1146:             FROM recetas_maestro r
1147:             JOIN platos p ON p.id = r.plato_id
1148:             WHERE r.id = ?
1149:         """, (receta_id,))
1150: 

EJEMPLO:


PARA RESTAURAR ARCHIVOS :

type archivo_backup.py > archivo_original.py <--- REATAURA

UNA FORMA DE GUARDAR UN ARCHIVO CON COPY:
C:\Users\jrmon\Documents\recetas_app>copy /Y "bats\arranca_recetas.bat" "bats\arranca_recetas_backup.bat"


SALIR DEL INTERPRETE DE PYTHON: exit()

simil de cls pero en python: os.system("cls")

py .\modulo_web\herramientas_forense\listar_archivo.py modulo_web\templates\admin_recetas_editar_nuevo.html

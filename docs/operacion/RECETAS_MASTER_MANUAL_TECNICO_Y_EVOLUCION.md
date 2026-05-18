AQUI: FECHA: Informe Git Y Recuperacion Recetas Master

ESTE ES EL MANUAL VIVO!!!!!!

Informe de Git y Recuperación — RECETAS MASTER
Objetivo

Dejar documentado:

cómo guardar los cambios actuales en Git
cómo recuperar versiones anteriores
cómo localizar los archivos importantes
cómo arrancar el sistema
cómo probar la pantalla de RECETAS MASTER
qué funcionalidades quedaron estabilizadas
1. Carpeta raíz del proyecto

Abrir consola en:

C:\Users\jrmon\Documents\recetas_app

Comprobar ubicación:

cd
2. Arrancar el servidor Flask

Desde la carpeta raíz:

python -m modulo_web.web_app
3. URL importantes
Nueva receta
http://127.0.0.1:5000/admin/recetas/nueva
Listado recetas
http://127.0.0.1:5000/admin/recetas/listado
4. Base de datos
Base SQLite principal

Archivo:

modulo_web/recetas.db
Verificar ruta real cargada por Flask

Al arrancar:

python -m modulo_web.web_app

el sistema imprime algo parecido a:

DEBUG DB_PATH en runtime: C:\Users\jrmon\Documents\recetas_app\modulo_web\recetas.db

Eso confirma:

qué base está usando realmente
que no se está usando otra base accidentalmente
5. Dónde encontrar las rutas Flask
Archivo principal de rutas
modulo_web/web_app.py
Cómo localizar una ruta rápidamente

Buscar:

@app.route(

Ejemplos:

@app.route("/admin/recetas/nueva")
@app.route("/admin/recetas/listado")
@app.route("/admin/recetas/editar/<int:receta_id>")
Cómo confirmar que Flask registró las rutas

Al arrancar el servidor pueden aparecer:

=== RUTAS REGISTRADAS ===

con el listado de endpoints activos.

6. Nomencladores y URLs importantes
Objetivo

Los nomencladores son tablas maestras auxiliares usadas por RECETAS MASTER.

Permiten mantener:

ingredientes
platos
unidades
tipos
estructuras auxiliares
Pantalla RECETAS MASTER
Nueva receta
http://127.0.0.1:5000/admin/recetas/nueva
Listado recetas
http://127.0.0.1:5000/admin/recetas/listado
Nomencladores principales
Ingredientes

Archivo template:

modulo_web/templates/admin_ingredientes.html

URL:

http://127.0.0.1:5000/admin/ingredientes
Platos

Archivo template:

modulo_web/templates/admin_platos.html

URL:

http://127.0.0.1:5000/admin/platos
Unidades

Archivo template:

modulo_web/templates/admin_unidades.html

URL:

http://127.0.0.1:5000/admin/unidades
Tipos de plato

Archivo template:

modulo_web/templates/admin_tipos_plato.html

URL:

http://127.0.0.1:5000/admin/tipos-plato
Dónde localizar rutas reales

Archivo principal:

modulo_web/web_app.py

Buscar:

@app.route(

para confirmar:

endpoints
métodos GET/POST
nombres reales
7. Archivo principal trabajado
Template principal
modulo_web/templates/admin_recetas_nueva.html
8. Funcionalidades estabilizadas
Navegación protegida

Se estabilizó:

botón “Ir al listado”
botón “Cancelar”
warning por cambios sin guardar
control beforeunload
Duplicidad de ingredientes

Ahora:

detecta ingrediente repetido inmediatamente
muestra mensaje visual grande
limpia fila inválida
mantiene foco correcto
Duplicidad de receta

Ahora:

detecta receta existente
mensaje desaparece al escoger otro plato
UX limpia sin refrescar
Mejoras visuales
mensajes más visibles
separación visual de errores
limpieza de mensajes dinámicos
9. Cómo guardar cambios en Git
Ver estado
git status
Agregar archivos
git add .
Crear commit
git commit -m "RECETAS MASTER: estabilizacion UX, control de duplicidades, navegacion protegida y mejoras visuales"
10. Cómo ver historial de commits
git log --oneline
11. Cómo recuperar una versión anterior
Ver commits
git log --oneline

Ejemplo:

983b22b RECETAS MASTER...
Restaurar archivo específico desde commit
git checkout 983b22b -- modulo_web/templates/admin_recetas_nueva.html
12. Cómo hacer backup manual antes de cambios grandes

Copiar:

admin_recetas_nueva.html

como:

admin_recetas_nueva_BACKUP.html

antes de modificaciones sensibles.

13. Lecciones importantes aprendidas
No borrar líneas durante pruebas rápidas

Preferir:

// línea comentada

antes que eliminar código.

Hacer cambios pequeños y reversibles

Estrategia usada:

un cambio por vez
probar
validar
continuar
Diferenciar problemas frontend/backend

Se separaron correctamente:

duplicidad de ingredientes (frontend JS)
duplicidad de recetas (backend Flask + frontend visual)
14. Estado actual

Pantalla RECETAS MASTER actualmente:

funcional
estable
con validaciones activas
protegida ante pérdidas accidentales
con UX mejorada
15. Recomendación futura

Más adelante:

Implementar selector inteligente/autocomplete de ingredientes.

No urgente.

El select HTML actual funciona correctamente como select nativo clásico.

ANEXO — CONTROL DE VERSIONES Y EVOLUCIÓN
Objetivo del anexo

Mantener un historial entendible del proyecto:

qué cambios importantes se hicieron
en qué orden ocurrieron
qué problemas resolvieron
cómo identificar versiones estables

Este anexo puede seguir creciendo con futuros commits.

Versión 1 — Base inicial RECETAS MASTER

Estado:

creación de pantalla nueva receta
estructura básica Flask/Jinja
guardado en SQLite
listado y edición inicial

Archivos principales:

modulo_web/web_app.py
modulo_web/templates/admin_recetas_nueva.html
Versión 2 — Navegación protegida

Se añadió:

detección de cambios sin guardar
beforeunload
confirmaciones al salir
protección botón cancelar
protección botón ir al listado

Problemas resueltos:

pérdidas accidentales de datos
navegación peligrosa
Versión 3 — Estabilización JS y recuperación

Se trabajó sobre:

errores de llaves JS
recuperación desde backups
restauración de estructura sana
separación de responsabilidades

Lección importante:

No borrar líneas durante pruebas rápidas.

Preferir comentar.

Versión 4 — Duplicidad de ingredientes

Se añadió:

detección inmediata de ingredientes repetidos
limpieza visual de fila inválida
mensajes dinámicos grandes
foco correcto en ingrediente inválido

Problemas resueltos:

filas incoherentes
duplicidades silenciosas
UX poco visible
Versión 5 — Duplicidad de recetas

Se añadió:

ocultación automática de mensajes flash antiguos
limpieza visual al seleccionar otro plato

Problemas resueltos:

mensajes pegados
confusión visual
Versión 6 — Mejoras visuales UX

Se añadió:

mensajes más grandes
separación visual entre alertas
posicionamiento de mensajes importantes
limpieza de interfaz
Versión 7 — Comprensión del select HTML nativo

Se investigó:

comportamiento real del select HTML
navegación por letras
diferencias entre select clásico y autocomplete moderno

Conclusión:

El select actual funciona correctamente como select HTML nativo.

Futuro posible:

Implementar autocomplete inteligente.

Cómo continuar el anexo en el futuro

Después de cada bloque importante:

Hacer commit Git
Añadir nueva versión al anexo
Explicar:
qué se cambió
qué se resolvió
qué archivos intervinieron
qué riesgos hubo
qué quedó pendiente
Recomendación general

Siempre mantener:

backup manual antes de cambios grandes
commits frecuentes
cambios pequeños y probados
documentación incremental

Eso permite:

recuperar versiones estables
entender la evolución del sistema
explicar rápidamente el proyecto a terceros
evitar pérdidas difíciles de revertir

FECHA 09-MAYO-2026 06:00
CONSOLIDACIÓN DEL FLUJO HÍBRIDO USUARIO / CLIENTE
Objetivo arquitectónico

Se consolidó oficialmente la separación funcional entre:

usuario → operador administrativo
cliente → consumidor final del catálogo público

Esto permitió estabilizar dos flujos independientes dentro del mismo sistema web.

FLUJOS DEFINIDOS
Flujo usuario (administración)
Listado MASTER
→ catálogo público preview
→ detalle receta
→ preparación
→ regreso reversible
→ retorno al MASTER

El usuario mantiene contexto administrativo completo durante toda la navegación.

Flujo cliente (público)
Catálogo público
→ detalle receta
→ preparación

El cliente NO visualiza:

herramientas administrativas
accesos MASTER
navegación interna de administración
controles editoriales
IMPLEMENTACIÓN TÉCNICA
Propagación administrativa

Se consolidó la propagación de:

?admin=1

como mecanismo oficial de persistencia del contexto administrativo.

La navegación reversible depende completamente de que este parámetro se preserve entre:

rutas Flask
templates Jinja
enlaces internos
navegación detalle/preparación/catálogo
CORRECCIÓN DE BUG DE CONTEXTO ADMIN
Problema detectado

El flujo:

detalle
→ preparación
→ volver receta
→ ver más recetas

perdía el contexto administrativo y regresaba al catálogo público cliente.

Causa raíz

La ruta:

/receta/<id>/preparacion

no propagaba:

desde_admin

hacia el template:

receta_preparacion.html
Solución aplicada

Se agregó:

desde_admin = request.args.get("admin") == "1"

y posteriormente:

desde_admin=desde_admin

al render_template() de preparación.

RESULTADO FINAL

Quedó estabilizado el flujo reversible completo:

MASTER
→ 👁️ preview
→ detalle
→ preparación
→ volver receta
→ ver más recetas
→ catálogo admin

manteniendo correctamente:

?admin=1

durante toda la navegación.

DECISIÓN ARQUITECTÓNICA CONSOLIDADA

El botón:

👁️

del listado MASTER representa oficialmente:

preview cliente rápida dentro del contexto administrativo

y NO acceso administrativo directo.

ESTADO DEL SISTEMA

Queda consolidado:

aislamiento usuario/cliente
navegación reversible administrativa
catálogo público estable
propagación contextual funcional
separación visual administrativa
arquitectura híbrida operativa
COMMIT DE CONSOLIDACIÓN
9dc9752
RECETAS WEB: correccion completa de navegacion reversible admin entre detalle, preparacion y catalogo
SIGUIENTE FASE

Implementación del sistema editorial:

visible_web

para:

publicar recetas
despublicar recetas
controlar visibilidad pública del catálogo.


09-MAYO-2026
HORA: 07:48 PM

SISTEMA: recetas_app
ACTUALIZACIÓN — IMPLEMENTACIÓN DEL SISTEMA EDITORIAL visible_web

FECHA: 09 Mayo 2026
RAMA: main

COMMIT DE CONSOLIDACIÓN EDITORIAL
30988c6
RECETAS WEB: implementacion completa del sistema editorial visible_web con publicar y despublicar recetas
OBJETIVO DE LA FASE

Se implementó oficialmente el sistema editorial de publicación para controlar qué recetas pueden visualizar los clientes en el catálogo público.

La solución se basó en la bandera persistente:

visible_web

integrada directamente en:

recetas_maestro
MIGRACIÓN SQLITE
Cambio estructural

Se agregó la columna:

visible_web INTEGER NOT NULL DEFAULT 1

a la tabla:

recetas_maestro
Compatibilidad con instalaciones existentes

Se implementó migración automática mediante:

ALTER TABLE recetas_maestro
ADD COLUMN visible_web INTEGER NOT NULL DEFAULT 1;

protegida con:

try / except sqlite3.OperationalError

para evitar errores en reinicios posteriores.

COMPORTAMIENTO DEL SISTEMA EDITORIAL
visible_web = 1
Receta publicada

La receta:

aparece en catálogo público
puede ser accedida por clientes
mantiene navegación pública funcional
visible_web = 0
Receta oculta

La receta:

desaparece del catálogo público
deja de mostrarse a clientes
permanece disponible para administración
FILTRADO DEL CATÁLOGO PÚBLICO

La función:

db_cargar_recetas_publicadas()

ahora utiliza:

WHERE r.visible_web = 1

garantizando que únicamente las recetas publicadas sean visibles para clientes.

MASTER ADMINISTRATIVO
Estado visual implementado

El listado MASTER ahora muestra:

🌐 Publicada
🚫 Oculta

según el estado editorial de cada receta.

ACCIONES EDITORIALES

Se implementó la nueva ruta Flask:

/admin/recetas/toggle-publicacion/<int:receta_id>
COMPORTAMIENTO TOGGLE

La acción alterna automáticamente:

1 → 0
0 → 1

mediante:

UPDATE recetas_maestro
SET visible_web =
    CASE
        WHEN visible_web = 1 THEN 0
        ELSE 1
    END
FRONTEND ADMINISTRATIVO
Nuevos controles

Se añadieron botones:

Publicar
Despublicar

directamente en:

admin_recetas_listado.html
VALIDACIÓN FUNCIONAL REALIZADA
Caso validado

La receta:

Arroz Frito Especial

fue despublicada correctamente y desapareció del catálogo público cliente.

RESULTADO DE LA FASE

El sistema dispone ahora de:

control editorial persistente
publicación selectiva
despublicación inmediata
filtrado automático del catálogo
separación completa usuario/cliente
administración editorial funcional
ESTADO ARQUITECTÓNICO ACTUAL

El proyecto cuenta actualmente con:

Backend

✅ SQLite consolidado
✅ persistencia editorial
✅ navegación híbrida
✅ propagación administrativa
✅ filtrado público

Frontend

✅ catálogo público funcional
✅ MASTER administrativo estable
✅ preview cliente
✅ control visual editorial
✅ botones publicar/despublicar

Arquitectura

✅ separación usuario/cliente
✅ flujo reversible administrativo
✅ sistema editorial operativo
✅ CMS culinario funcional

SIGUIENTE FASE POSIBLE

El sistema queda preparado para futuras extensiones:

publicación programada
borrador/editorial avanzada
categorías públicas
búsqueda cliente
imágenes culinarias
exportación web pública
autenticación administrativa
estadísticas de visualización
FIN DE ACTUALIZACIÓN DEL MANUAL TÉCNICO Y EVOLUCIÓN

SISTEMA: recetas_app
ACTUALIZACIÓN — IMPLEMENTACIÓN COMPLETA DE AUTENTICACIÓN ADMINISTRATIVA

FECHA: 10 Mayo 2026
HORA: 11:40 PM
RAMA: main

COMMIT DE CONSOLIDACIÓN
fb7215c
AUTH: implementacion completa de login admin, sesiones, timeout, logout y proteccion administrativa
OBJETIVO DE LA FASE

Se implementó el primer sistema formal de autenticación administrativa para proteger completamente el entorno MASTER del sistema.

La administración dejó de ser pública y pasó a operar mediante sesiones autenticadas.

ARQUITECTURA DE AUTENTICACIÓN
Sistema implementado

La autenticación se construyó utilizando:

Flask session
session cookies
secret_key
control de sesión persistente
timeout automático
protección de rutas administrativas
CONFIGURACIÓN BASE
Secret key

Se agregó:

app.secret_key

para habilitar persistencia de sesiones Flask.

CREDENCIALES MVP

Se implementó autenticación inicial mediante:

ADMIN_USER
ADMIN_PASS

como solución MVP temporal.

LOGIN ADMINISTRATIVO
Nueva ruta
/login
FUNCIONALIDADES

El login ahora permite:

autenticación administrativa
validación usuario/password
persistencia de sesión
redirección automática al MASTER
mensajes de error
bloqueo acceso administrativo no autenticado
TEMPLATE LOGIN
Nuevo archivo
modulo_web/templates/login.html
FUNCIONALIDADES VISUALES

La interfaz login incluye:

formulario estilizado
caja centrada
UX limpia
feedback visual errores
botón acceso
visualización opcional contraseña
VISUALIZACIÓN DE CONTRASEÑA

Se implementó:

👁️ mostrar/ocultar contraseña

mediante JavaScript frontend.

Esto mejora:

UX
validación visual
accesibilidad operativa
SESIONES PERSISTENTES
Configuración implementada
session.permanent = True
TIMEOUT AUTOMÁTICO

Se agregó:

app.permanent_session_lifetime = timedelta(hours=4)
RESULTADO

La sesión administrativa:

permanece activa durante navegación normal
evita login repetitivo
expira automáticamente
mejora seguridad operativa
PROTECCIÓN ADMINISTRATIVA
Middleware implementado

Se agregó:

@app.before_request

para proteger rutas administrativas.

COMPORTAMIENTO

Si un usuario NO autenticado intenta acceder a:

/admin/*

el sistema:

redirige automáticamente a /login
LOGOUT
Nueva ruta
/logout
FUNCIONALIDAD

Logout ahora:

destruye la sesión
elimina autenticación
retorna a login
impide acceso posterior al MASTER
REDIRECCIÓN INTELIGENTE

La ruta:

/login

ahora detecta si ya existe sesión activa.

RESULTADO

Usuarios autenticados:

NO vuelven a ver login innecesariamente

y son enviados directamente al:

Listado MASTER
SESIÓN DE USUARIO

Ahora el sistema almacena:

session["usuario"]

permitiendo conocer qué usuario inició sesión.

FRONTEND ADMINISTRATIVO
Barra superior MASTER

Se agregaron:

👤 usuario autenticado
🚪 Cerrar sesión
RESULTADO VISUAL

La interfaz administrativa ahora transmite claramente:

sesión activa
identidad autenticada
control administrativo real
VALIDACIONES REALIZADAS
Verificado exitosamente

✅ login correcto
✅ login incorrecto
✅ persistencia sesión
✅ logout
✅ expiración configurada
✅ protección rutas admin
✅ bloqueo acceso directo
✅ redirección automática
✅ visualización contraseña

ESTADO ACTUAL DEL SISTEMA
CLIENTE

✅ catálogo público
✅ detalle receta
✅ preparación

ADMINISTRACIÓN

✅ login
✅ logout
✅ timeout
✅ sesiones persistentes
✅ CRUD MASTER
✅ control editorial
✅ navegación reversible
✅ usuario autenticado visible

ARQUITECTURA

✅ SQLite consolidado
✅ separación usuario/cliente
✅ autenticación administrativa
✅ protección backend
✅ control editorial
✅ persistencia estable

IMPACTO ARQUITECTÓNICO

Este commit representa el paso oficial desde:

aplicación local abierta

hacia:

sistema administrativo autenticado real
PREPARACIÓN PARA PRODUCCIÓN

El sistema queda ahora preparado para:

deployment privado
publicación en internet
acceso remoto seguro
futuras capas de usuarios reales
permisos avanzados
autenticación escalable
SIGUIENTE FASE NATURAL
Deployment privado inicial

El sistema ya dispone de suficiente estabilidad para:

primer despliegue real en internet

mediante plataformas tipo:

Render
Railway
Fly.io
FIN DE ACTUALIZACIÓN DEL MANUAL TÉCNICO Y EVOLUCIÓN

AQUI: FECHA: 12-MAYO-2026

Estado actual general

El sistema recetas_app ya cuenta con:

Arquitectura híbrida:
Administración local con Flask (127.0.0.1:5000)
Catálogo público desplegado en Render
Flujo completo operativo:
nomencladores
master de recetas
listado master
catálogo público
detalle receta pública
guía de preparación pública
Publicación web funcional sin depender de Flask local.
Acceso desde PC y móvil mediante endpoint público Render.
URL pública actual

Catálogo público:

https://recetas-master.onrender.com/recetas

Funcionando desde:

PC
móvil
WhatsApp
navegador externo

Importante:

Google NO indexa automáticamente el sistema todavía.
Para acceder debe escribirse la URL completa o abrirse desde enlace directo.
Flujo operacional actual
Nomencladores
↓
Master de recetas
↓
Listado master
↓
Catálogo público
↓
Ver receta
↓
Receta de la abuela
↓
Guía de preparación
Estado Flask
REQUIERE Flask LOCAL
nomencladores
master recetas
listado master
edición
creación
publicación
administración
NO REQUIERE Flask LOCAL

Catálogo público Render:

https://recetas-master.onrender.com/recetas
Trabajo realizado en interfaz Master Recetas — Nueva

Archivo principal:

modulo_web/templates/admin_recetas_nueva.html
Mejoras estructurales realizadas
Eliminado entorno de prueba visual

Se eliminó:

ARCHIVO NUEVA REAL

y fondos de depuración.

Reestructuración visual completa

Se creó:

header-master
bloques visuales
separación por áreas funcionales
Nueva estructura visual
Bloque Datos generales

Contiene:

Plato
Buscar
Raciones base
Bloque Textos culinarios

Contiene:

Preparación
Elaboración
Presentación
Nutrición

Distribución:

Grid 2 columnas
Más compacto
Más profesional
Bloque Ingredientes

Separado visualmente.

Ahora:

aparece antes
mejor lectura
menos scroll
Mejoras UX realizadas
Botonera superior

Botones:

Guardar receta
Ir al listado
Cancelar

Integrados junto al título principal.

Reducción de scroll inicial

Se compactó:

encabezado
márgenes
separación vertical

Objetivo:
mostrar ingredientes desde el primer pantallazo.

Bloques visuales profesionales

Se añadieron:

bordes suaves
separaciones visuales
jerarquía visual
estilo más moderno
Sistema de validaciones ya operativo
Validaciones implementadas
raciones obligatorias
raciones > 0
solo numérico
ingrediente obligatorio
ingrediente duplicado
deco no mayor que cantidad
cálculo automático cocina
navegación Enter / Shift+Enter
Sistema de mensajes operativos

Tipos:

ok
error

Con:

colores
bloques visuales
HTML seguro
mensajes estilo nomencladores
Mejoras pendientes inmediatas
LISTADO MASTER — MENSAJE BORRADO

Detectado:

al borrar receta NO aparece mensaje visual.

Objetivo:
mostrar igual que nomencladores:

Ejemplo:

Receta "Arroz Frito Especial" eliminada correctamente.

Con:

texto verde
nombre receta rojo
mismo patrón nomencladores

Pendiente revisar:

Archivo:

modulo_web/web_app.py

Ruta probable:

admin_recetas_borrar()

Debe agregarse:

flash()
recuperación nombre receta
mensaje HTML colorizado
Sistema de backups implementado
1️⃣ Backup SQLite

Archivos:

backup_recetas.py
backup_recetas.bat

Función:

backup rápido de recetas.db

Destino:

backups/

Resultado:

backups históricos fechados
2️⃣ Snapshot completo proyecto

Archivos:

backup_proyecto.py
backup_proyecto.bat

Función:

snapshot completo del proyecto

Incluye:

Flask
templates
JS
CSS
SQLite
Render
scripts
todo el sistema

Destino:

backups_proyecto/

Características:

sin ZIP
rápido
ignora .git
ignora __pycache__
ignora backups previos
Sistema RESTORE implementado
Restore SQLite

Archivos:

restore_recetas.py
restore_recetas.bat

Características:

listado histórico backups
selección interactiva
restore automático
rollback seguro

MUY IMPORTANTE:
antes de restaurar:

crea backup automático del estado actual

Formato:

ANTES_RESTORE_YYYY-MM-DD_HH-MM-SS.db
Infraestructura de seguridad actual

El sistema ya cuenta con:

backup SQLite
restore SQLite
rollback automático
snapshot completo proyecto
backups históricos
recuperación temporal
protección previa restore
Próximos trabajos inmediatos
1️⃣ Finalizar mensaje borrado recetas

Pendiente.

2️⃣ Git completo

Debe hacerse commit de:

backups
restore
rediseño master nueva
mejoras UX
snapshot proyecto
rollback SQLite
3️⃣ Actualizar Manual Técnico

Actualizar:

backups
restore
snapshots
arquitectura híbrida
Render
flujo publicación
recuperación sistema
nuevos scripts .bat
seguridad operacional
4️⃣ Actualizar Evolución del Sistema

Registrar:

separación admin/publico
despliegue Render
acceso móvil
backups
rollback
snapshots
refactor visual master recetas
endurecimiento operacional
Archivos principales involucrados
Frontend
modulo_web/templates/admin_recetas_nueva.html
Backend Flask
modulo_web/web_app.py
Backups
backup_recetas.py
backup_recetas.bat

backup_proyecto.py
backup_proyecto.bat

restore_recetas.py
restore_recetas.bat
Estado general del proyecto

El sistema ya pasó de:

prototipo
a:
sistema operativo real con protección, rollback y publicación híbrida.

Infraestructura ya existente:

Render público
backups
restore
snapshots
rollback
publicación web
administración local
acceso móvil
protección operacional

AQUI:FECHA 14-MAYO-2026
CONTEXTO GENERAL

Se recuperó exitosamente el archivo:

modulo_web/templates/admin_recetas_nueva.html

desde commit estable funcional, luego de detectar que versiones posteriores habían roto:

navegación
validaciones
cálculo
flujo de captura
estabilidad JS

La recuperación se hizo desde commit estable:

ffb8932
ESTADO ACTUAL — RECETAS NUEVAS
ARCHIVO
modulo_web/templates/admin_recetas_nueva.html
FUNCIONALIDADES YA OPERATIVAS
UI / TABLA

✅ tabla compacta profesional
✅ columnas alineadas
✅ columnas:

Ingrediente
Cantidad
Deco
Cocina
UM
Acciones

✅ badges amarillos UM
✅ fila activa amarilla
✅ botones uniformes
✅ tabla visual estable

NAVEGACIÓN

✅ Enter:

ingrediente → cantidad
cantidad → deco

✅ Shift+Enter:

textos → siguiente bloque

✅ nutrición:

Shift+Enter → ingredientes

✅ Deco:

Enter → crea nueva fila
MOTOR DINÁMICO
IMPLEMENTADO

✅ fila plantilla dinámica
✅ creación automática filas
✅ navegación automática
✅ múltiples filas funcionales

VALIDACIONES IMPLEMENTADAS

✅ cantidad > 0
✅ deco ≥ 0
✅ deco ≤ cantidad
✅ ingredientes duplicados prohibidos
✅ receta no puede quedar vacía

CÁLCULOS IMPLEMENTADOS
Cocina automática
cocina = cantidad - deco

✅ tiempo real
✅ bloqueo negativos
✅ campo rojo si deco > cantidad

UM SINCRONIZADAS

✅ UM ingrediente
✅ UM deco
✅ UM cocina

TEXTOS RECETA
CAMPOS

✅ preparación
✅ elaboración
✅ presentación
✅ nutrición

BUG DETECTADO Y CORREGIDO
PROBLEMA

Los textos:

no aparecían en edición
ni en guía preparación
CAUSA REAL

En:

modulo_web/web_app.py

función:

def admin_recetas_nueva():

el INSERT original NO guardaba:

preparacion
elaboracion
presentacion
nutricion
CORRECCIÓN APLICADA
SE AGREGÓ:
preparacion = request.form.get(...)
elaboracion = ...
presentacion = ...
nutricion = ...
Y EL INSERT FUE AMPLIADO A:
INSERT INTO recetas_maestro
(
    plato_id,
    raciones_base,
    preparacion,
    elaboracion,
    presentacion,
    nutricion
)
RESULTADO

✅ textos se guardan correctamente
✅ textos aparecen en edición
✅ textos aparecen en guía preparación

RECETAS EDITAR — ESTADO ACTUAL
ARCHIVO
modulo_web/templates/admin_recetas_editar.html
FUNCIONALIDADES OPERATIVAS

✅ carga textos correctamente
✅ carga ingredientes
✅ cocina visible
✅ cálculo cocina operativo
✅ UM visibles
✅ navegación básica operativa

PROBLEMA ESTRUCTURAL DETECTADO

La arquitectura JS de edición es ANTIGUA.

Actualmente:

NUTRICIÓN
↓
primer ingrediente
↓
cantidad
↓
DECO
↓
GUARDAR CAMBIOS

❌ NO permite:

insertar nuevas filas correctamente
recorrer múltiples filas dinámicamente
navegación ERP completa
DISEÑO FUNCIONAL DEFINIDO PARA EDITAR
REGLAS APROBADAS
ENTER EN DECO
SI EXISTE FILA SIGUIENTE
focus → ingrediente siguiente fila
SI ES ÚLTIMA FILA
crear nueva fila
↓
focus ingrediente nueva fila
SI OPERADOR NO QUIERE MÁS INGREDIENTES

En ingrediente vacío de nueva fila:

Enter
↓
GUARDAR CAMBIOS
REGLAS DE INTEGRIDAD DEFINIDAS
PROHIBIDO

❌ borrar última fila real
❌ receta sin ingredientes
❌ duplicar ingredientes

CONCEPTO CLAVE
FILA VACÍA FINAL

La última fila vacía:

NO cuenta como ingrediente
solo representa:
¿desea continuar?
ESTRATEGIA TÉCNICA DECIDIDA
NO PARCHEAR EDITAR

Se decidió:

migrar arquitectura de NUEVA → EDITAR
RAZÓN

La arquitectura de:

admin_recetas_nueva.html

ya está:
✅ estable
✅ moderna
✅ robusta
✅ probada

PLAN SIGUIENTE EN NUEVA PESTAÑA
OBJETIVO

Unificar:

navegación
filas dinámicas
validaciones
cocina
UM
eventos
UX

entre:

admin_recetas_nueva.html

y

admin_recetas_editar.html
ARCHIVOS CLAVE
TEMPLATE NUEVA
modulo_web/templates/admin_recetas_nueva.html
TEMPLATE EDITAR
modulo_web/templates/admin_recetas_editar.html
BACKEND
modulo_web/web_app.py
ESTADO GENERAL DEL SISTEMA

🔥 Muy estable actualmente.

Las últimas correcciones:
✅ recuperaron funcionalidad crítica
✅ estabilizaron JS
✅ estabilizaron UI
✅ consolidaron lógica de negocio
✅ consolidaron textos recetas
✅ consolidaron cocina/deco

El sistema ya está entrando en fase:

ERP / UX profesional

AQUI:FECHA 17-MAYO-2026
HORA: 10:14 AM
Deploy Render Bat Recetas App
DEPLOY AUTOMÁTICO — recetas_app
OBJETIVO

Automatizar el flujo:

revisar estado git
agregar cambios
excluir backups
hacer commit
hacer push a GitHub
disparar redeploy automático en Render
ARCHIVO

Crear este archivo en:

C:\Users\jrmon\Documents\recetas_app\deploy_render.bat
CONTENIDO DEL .BAT
@echo off
cls
color 0A


echo =====================================
echo    RECETAS_APP - DEPLOY RENDER
 echo =====================================
echo.


cd /d C:\Users\jrmon\Documents\recetas_app


echo.
echo ===== ESTADO GIT =====
git status


echo.
set /p mensaje=Escriba mensaje del commit:


echo.
echo ===== AGREGANDO ARCHIVOS =====


git add modulo_web
git add docs


echo.
echo ===== COMMIT =====
git commit -m "%mensaje%"


echo.
echo ===== PUSH A GITHUB =====
git push origin main


echo.
echo =====================================
echo      DEPLOY ENVIADO A RENDER
 echo =====================================
echo.
pause
CÓMO USARLO
1.

Doble clic en:

deploy_render.bat
2.

El sistema mostrará:

git status

para revisar cambios.

3.

Escribir mensaje del commit.

Ejemplo:

RECETAS: mejoras UX nomencladores y estabilizacion editor recetas
4.

El .bat hará automáticamente:

git add
commit
push
5.

Render detectará automáticamente el push y hará:

redeploy
VENTAJAS

✅ evita olvidar comandos ✅ evita errores manuales ✅ flujo rápido ✅ despliegue consistente ✅ profesionaliza operación

IMPORTANTE

Este .bat:

✅ SÍ sube:

modulo_web
/docs

❌ NO sube:

backups_proyecto

por lo que los backups quedan protegidos automáticamente.

RECOMENDACIÓN FUTURA

Más adelante crear también:

run_local.bat
backup_proyecto.bat

para consolidar completamente la operación del sistema.

COMENTARIO:

Ya quedó preparado el .bat profesional para despliegue automático a GitHub + Render.

Incluye:

✅ git status
✅ git add controlado
✅ commit interactivo
✅ push automático
✅ exclusión implícita de backups
✅ estructura preparada para crecimiento futuro del sistema.

AQUI: ESTADO FINAL OFICIAL
FECHA: 18-MAYO
HORA: 00:23 AM
Git

✅ limpio
✅ saneado
✅ optimizado
✅ historial saludable

GitHub

✅ actualizado
✅ sincronizado
✅ pushes funcionando perfectamente

Render

✅ auto deploy operativo
✅ producción actualizada
✅ catálogo sincronizado

Sistema recetas_app

✅ editor estabilizado
✅ nomencladores corregidos
✅ UX recuperada
✅ navegación catálogo/admin restaurada

Operación

✅ deploy_render.bat oficializado
✅ protección anti doble ejecución
✅ backups desacoplados del repo
✅ documentación centralizada

Documentación

✅ Manual Técnico y Evolución actualizado
✅ arquitectura documentada
✅ saneamiento Git registrado
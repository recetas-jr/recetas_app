Informe Git Y Recuperacion Recetas Master
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
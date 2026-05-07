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
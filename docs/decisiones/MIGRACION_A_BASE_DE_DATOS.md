# Migración a Base de Datos (SQLite)

Se da por cerrada la Fase XX (versión web con persistencia en JSON).
Se inicia una nueva fase dedicada a la migración controlada del sistema a una base de datos SQLite.
El objetivo es reemplazar gradualmente la persistencia en JSON por una capa de acceso a datos en SQLite,
sin romper los flujos actuales ni afectar la operación del sistema.
La migración se realizará por etapas, manteniendo siempre un plan de retorno a JSON en caso de fallos.
Primero se definirá el esquema de tablas y se creará la base de datos.
Luego se migrarán los datos existentes y se validará que la web muestre la misma información.
Finalmente, se cambiarán una a una las funciones de persistencia para usar la base de datos.
Esta fase busca dejar el sistema más robusto, consistente y preparado para crecer.

COMIENZO DE DECISIONES
DIA: 15-FEB-2026 — HORA: 06:00 am

MIGRACIÓN A BASE DE DATOS — FASE LECTURA (SQLite)

Se establece que:

Se implementa infraestructura SQLite (recetas.db) con tablas:

tipos_plato

platos

unidades

ingredientes

recetas_maestro

recetas_ingredientes

Se crea capa de persistencia DB (modulo_web/persistencia_db.py) con funciones de lectura:

db_cargar_platos()

db_cargar_unidades()

db_cargar_ingredientes()

db_cargar_recetas_maestro_listado()

La aplicación web (modulo_web/web_app.py) pasa a:

Leer nomencladores desde SQLite con fallback a JSON.

Leer el listado del MASTER de recetas desde SQLite con fallback a JSON.

Ejecutar el borrado del MASTER usando datos provenientes de SQLite.

Durante esta fase:

JSON se mantiene como fuente secundaria temporal.

La creación/edición del MASTER aún escribe en JSON.

SQLite se usa como fuente principal de lectura para listado y nomencladores.

Se ignora modulo_web/recetas.db en Git mediante .gitignore.

Se considera cerrada y estable la fase de:

Lectura del MASTER desde SQLite

Listado del MASTER desde SQLite

Borrado del MASTER con datos de SQLite

Fallback seguro a JSON
DOCUMENTACIÓN COMPLETA DE RUTAS — SISTEMA recetas_app

Sistema: recetas_app
Documento: RUTAS_COMPLETAS_DEL_SISTEMA.md
Versión: 1.0

Propósito:
Registrar todas las rutas utilizadas por el sistema para facilitar mantenimiento, migración, depuración y comprensión de la arquitectura.

1. RUTAS DEL SISTEMA DE ARCHIVOS
Raíz del proyecto
C:\Users\jrmon\Documents\recetas_app

Contiene el proyecto completo.

Estructura principal del proyecto
recetas_app
│
├─ PC_DESARROLLO
├─ PC_LEJANIA
├─ USB_CAPTURA_REMOTA
│
├─ detectar_usb.py
│
├─ web_app.py
│
├─ modulo_web
│
└─ templates
2. SISTEMA DE CAPTURA REMOTA

Ruta:

C:\Users\jrmon\Documents\recetas_app\USB_CAPTURA_REMOTA

Contiene el sistema portable de captura de recetas.

Archivos fuente:

capturar_receta.py
listar_recetas.py
crear_usb_captura.py
sistema_captura_recetas.py
Carpeta de ejecutables

Ruta:

C:\Users\jrmon\Documents\recetas_app\USB_CAPTURA_REMOTA\dist

Generada por PyInstaller.

Contiene:

capturar_receta.exe
listar_recetas.exe
crear_usb_captura.exe
sistema_captura_recetas.exe

RECETAS
NOMENCLADORES
3. ESTRUCTURA DEL USB ENVIADO A LA LEJANÍA

Cuando el sistema prepara el USB la estructura final es:

USB:\

sistema_captura_recetas.exe
capturar_receta.exe
listar_recetas.exe
crear_usb_captura.exe

RECETAS
NOMENCLADORES

Ejemplo real:

E:\
4. SCRIPT DE PREPARACIÓN AUTOMÁTICA DEL USB

Archivo:

C:\Users\jrmon\Documents\recetas_app\detectar_usb.py

Funciones:

detectar automáticamente el USB

copiar ejecutables

copiar carpetas necesarias

5. RUTAS WEB DEL SISTEMA (FLASK)

Servidor local:

http://localhost:5000
6. RUTAS PÚBLICAS
Portada
/
Catálogo público de recetas
/recetas
Detalle de receta
/receta/<receta_id>

Ejemplo:

/receta/5
Preparación de receta
/receta/<receta_id>/preparacion
7. ADMINISTRACIÓN DE TIPOS DE PLATO
/admin/tipos_plato

Eliminar tipo de plato:

/admin/tipos_plato/borrar/<tipo_id>
8. ADMINISTRACIÓN DE UNIDADES DE MEDIDA
/admin/unidades

Eliminar unidad:

/admin/unidades/borrar/<unidad_id>
9. ADMINISTRACIÓN DE INGREDIENTES
/admin/ingredientes

Eliminar ingrediente:

/admin/ingredientes/borrar/<ingrediente_id>
10. ADMINISTRACIÓN DE PLATOS
/admin/platos

Eliminar plato:

/admin/platos/borrar/<plato_id>
11. ADMINISTRACIÓN DE RECETAS

Listado de recetas:

/admin/recetas/listado

Nueva receta:

/admin/recetas/nueva

Editar receta:

/admin/recetas/editar/<receta_id>

Ejemplo:

/admin/recetas/editar/12

Borrar receta:

/admin/recetas/borrar/<receta_id>
12. RUTAS INTERNAS DE BASE DE DATOS

Las operaciones de base de datos se realizan mediante funciones ubicadas en:

modulo_web/persistencia_db.py

Funciones principales:

db_cargar_platos()
db_cargar_unidades()
db_cargar_ingredientes()
db_cargar_recetas_maestro_listado()
db_cargar_tipos_plato()
db_cargar_receta_detalle()
get_connection()
13. FLUJO OPERATIVO DEL SISTEMA
PC_DESARROLLO
   ↓
Preparar USB
   ↓
Enviar USB
   ↓
PC_LEJANIA
   ↓
Captura de recetas
   ↓
Retorno del USB
   ↓
Integración de recetas al sistema principal
14. UTILIDAD DE ESTE DOCUMENTO

Este documento permite:

comprender la arquitectura completa

localizar rápidamente componentes del sistema

reconstruir el sistema en otra computadora

evitar errores de rutas

facilitar mantenimiento futuro

FIN DEL DOCUMENTO
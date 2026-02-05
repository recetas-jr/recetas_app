🧾 BITÁCORA TÉCNICA — PROYECTO SISTEMA DE RECETAS
📅 Inicio del proyecto

Se comenzó el desarrollo de un sistema de recetas gastronómicas con dos grandes áreas:

Nomencladores (catálogos):

Platos

Ingredientes

Unidades de medida

MASTER de recetas:

Relación Plato → Ingredientes + textos técnicos + raciones base

El sistema comenzó como aplicación de consola en Python y luego evolucionó a:

GUI con Tkinter

Posteriormente versión WEB con Flask

🧱 Decisiones de arquitectura tempranas

Separación conceptual entre:

Catálogos (nomencladores)

Maestro de recetas (MASTER)

Uso de JSON como almacenamiento temporal:

plato.json

recetas_publicadas.json

ingredientes y unidades en JSON independientes

Documentación paralela en /docs:

Estructura de datos

Glosario y terminología

Leyenda de estructura de carpetas

🌐 Migración a versión WEB (Flask)

Se implementó servidor Flask:

web_app.py

Rutas bajo /admin/*:

/admin/platos

/admin/ingredientes

/admin/recetas

Templates HTML en:

templates/
  admin_platos.html
  admin_ingredientes.html
  admin_recetas.html

🧩 MASTER de Recetas — Objetivo funcional

Formulario de captura con:

Plato (select desde nomenclador)

Raciones base

Textos técnicos:

Preparación

Elaboración

Presentación

Nutrición

Ingredientes:

Ingrediente

Cantidad

UM automática

Objetivo UX:

Flujo continuo solo con teclado

ENTER funciona como TAB entre campos

Validaciones antes de permitir guardar

⚠️ Problema crítico detectado: CONTROL DE FOCO CON ENTER

Síntoma principal:

ENTER funciona entre la mayoría de los campos

En el campo Nutrición, ENTER no avanza

El foco pasa con TAB al bloque de ingredientes

Se sospecha interferencia externa o problema de JS

🧪 Fase de diagnóstico

Se realizaron pruebas:

Confirmación de que el template correcto se está cargando

Se añadió banda roja:
*** ARCHIVO admin_recetas.html — PRUEBA DE TEMPLATE ***

Se probó ejecución de scripts con alert()

Se verificó consola de Flask (PowerShell)

Se abrió DevTools de Chrome

Se intentó detectar listeners activos con:

getEventListeners(document).keydown

Resultado parcial:

ENTER sí genera eventos

Pero el script de control de flujo no siempre se ejecuta

En algunos momentos no aparece ningún alert, indicando que:

El <script> puede no estarse ejecutando

O el HTML puede estar mal cerrado antes del script

🛑 Decisión estratégica

Se decide:

Detener modificaciones caóticas

Migrar a nueva pestaña de chat

Crear documento histórico técnico

A partir de ahora:

Cada pestaña nueva se inicia con estado documentado

Cada avance se agrega a la bitácora

Objetivo:

Trabajar con metodología profesional y evitar perder contexto.




📅 [2026-01-25] — Módulo Web / MASTER de Recetas
🔴 Problema detectado

Durante la depuración del formulario MASTER de recetas se detectaron fallos estructurales en el backend:

Existían funciones duplicadas:

cargar_ingredientes_con_unidad() estaba definida dos veces en web_app.py.

Algunas rutas utilizaban funciones inexistentes o incorrectas:

Uso de cargar_ingredientes() cuando debía usarse la función normalizada con UM.

Esto provocaba:

combos de ingredientes vacíos,

unidades de medida no visibles,

errores intermitentes (NameError),

comportamiento inconsistente entre nomencladores y MASTER.

🟡 Diagnóstico

El problema no estaba en HTML ni en JavaScript de control de foco, sino en:

desorganización de funciones backend,

múltiples fuentes de verdad,

falta de normalización en la carga de ingredientes y UM.

🟢 Decisión operativa

Se decidió:

Detener ajustes de UX y flujo con ENTER.

Limpiar y normalizar el backend primero, específicamente:

dejar una sola función válida para cargar ingredientes con UM,

asegurar que /admin/ingredientes y /admin/recetas (MASTER) usen la misma función,

eliminar funciones duplicadas y llamadas inconsistentes.

🔧 Acción ejecutada

Se eliminó un bloque duplicado de cargar_ingredientes_con_unidad() en web_app.py.

Se decidió continuar la limpieza por bloques completos, con cambios controlados uno a uno.

🎯 Próximo paso

Continuar con la limpieza estructural de web_app.py:

normalizar carga de ingredientes,

actualizar rutas para usar la función unificada,

verificar consistencia antes de retomar el flujo de captura con ENTER.




                             ACTUALIZACION TOTAL DEL PROYECTO 30-ENE-2026

# FASE XVI — RECUPERACIÓN Y BLINDAJE DEL PROYECTO RECETAS (ENERO 2026)

## Estado real del proyecto (derivado del disco)

La documentación a partir de esta fase refleja exclusivamente el estado real del proyecto,
verificado mediante inspección directa de la estructura de archivos y del código activo
(`tree /F` + auditoría de `persistencia.py`).

No se documentan suposiciones ni estados históricos no verificables.

---

## Arquitectura general confirmada

El sistema se organiza en tres capas claramente separadas:

1. Capa de datos (fuente de verdad)
2. Capa de acceso a datos (DAL)
3. Capa de presentación (Web Admin / Web Pública)

---

## Fuente de verdad de datos (CRÍTICA)

### data_compartida/data

Esta carpeta constituye la **ÚNICA FUENTE DE VERDAD OPERATIVA** del sistema.

Es utilizada por:
- módulo web
- versiones anteriores (consola / GUI)

Contiene, entre otros:
- platos.json
- ingredientes.json
- unidades.json
- config.json
- recetas_catalogo.json
- recetas_maestro.json
- recetas_detalle_version.json
- recetas_ingredientes.json
- backups históricos

NO es un módulo funcional.
Es infraestructura transversal.
NO debe eliminarse ni modificarse sin decisión explícita documentada.

---

## Capa de persistencia (DAL)

### persistencia.py

Archivo central de acceso a datos del sistema.

Rol:
- Capa de Acceso a Datos (Data Access Layer)
- Centraliza rutas y lectura/escritura de JSON
- Consume exclusivamente `data_compartida/data`

Estado:
- ACTIVO
- CRÍTICO
- Utilizado por Receta Web

No es código legacy aunque resida en la raíz del proyecto.

---

## Módulos existentes

### modulo_web (ACTIVO)

Módulo formal de la variante web del sistema.

Contiene:
- web_app.py (entrypoint Flask)
- routes/
- templates/
- static/
- web_data/ (persistencia exclusiva de publicación)

Este módulo está activo y en uso real.

---

### modulo_consola_v1 / modulo_consola_v2 (HISTÓRICOS)

Versiones anteriores del sistema (consola y GUI Tkinter).

Se conservan como referencia.
No son el foco operativo actual.

---

## Separación Web Admin vs Web Pública

### Web Admin
- Lee y escribe mediante `persistencia.py`
- Fuente de verdad: `data_compartida/data`

### Web Pública
- NO usa `persistencia.py`
- Consume exclusivamente:
  - modulo_web/web_data/recetas_publicadas.json
  - modulo_web/web_data/plato.json
- Rol: proyección / cache de publicación

Esta separación es intencional y correcta.

---

## Auditoría de persistencia — persistencia.py

### Archivos JSON consumidos (confirmados por código)

Nomencladores:
- platos.json
- ingredientes.json
- unidades.json
- config.json

Modelo de recetas (distribuido):
- recetas_catalogo.json
- recetas_maestro.json (núcleo del MASTER)
- recetas_ingredientes.json
- recetas_detalle_version.json

Observaciones:
- recetas.json está definido pero no consumido por ninguna función pública (legacy).
- recetas_detalle_version.json está definido pero aún no expuesto completamente en funciones DAL para Web.

---

## Modelo real de datos (CONTRATO EXPLÍCITO)

### recetas_catalogo.json
Rol: definición de existencia de receta.

Campos mínimos:
- id (int, único)
- nombre (str)
- tipo_plato (str)
- activo (bool)

No contiene versiones ni ingredientes.

---

### recetas_maestro.json
Rol: núcleo del MASTER.

Campos mínimos:
- id (int, único por versión)
- receta_id (int → recetas_catalogo.id)
- version (int o str)
- estado (activa | inactiva)
- raciones_base (int)
- peso_racion (float)

Reglas:
- Múltiples versiones por receta
- Solo una versión activa por receta

---

### recetas_detalle_version.json
Rol: textos técnicos por versión.

Campos mínimos:
- receta_maestro_id (int → recetas_maestro.id)
- preparacion (str)
- elaboracion (str)
- presentacion (str)
- nutricion (str)

---

### recetas_ingredientes.json
Rol: composición cuantitativa.

Campos mínimos:
- receta_maestro_id (int → recetas_maestro.id)
- ingrediente_id (int → ingredientes.id)
- cantidad (float)
- unidad_id (int → unidades.id)
- rol (str, opcional)

---

## Flujo operativo del MASTER (EXPLÍCITO)

1. Crear receta en recetas_catalogo.json
2. Crear versión en recetas_maestro.json
3. Asociar textos en recetas_detalle_version.json
4. Asociar ingredientes en recetas_ingredientes.json
5. Marcar versión como activa
6. (Opcional) Proyectar a web_data/recetas_publicadas.json

Reglas:
- No se publica sin versión activa
- El recalculo de raciones es solo para consulta, no persistente

---

## Clasificación de archivos

### ACTIVOS
- persistencia.py
- modulo_web/**
- data_compartida/data/**
- JSON del modelo distribuido de recetas
- nomencladores

### LEGACY / HISTÓRICOS
- modulo_consola_v1/**
- modulo_consola_v2/**
- JSON sueltos en raíz no consumidos por la DAL
- scripts auxiliares no importados por Web

No se eliminan en esta fase.

---

## Límites de alcance

### Operativo actual
- Nomencladores
- MASTER de recetas
- Web Admin
- Persistencia distribuida

### Fuera de alcance
- Costeo
- Contabilidad
- Históricos auditables
- Control de usuarios

---

## Protocolo de restauración (BLINDAJE)

Ante pérdida total de código:

1. Recuperar:
   - persistencia.py
   - data_compartida/data
2. Reconstruir:
   - rutas web usando exclusivamente la DAL
3. Verificar:
   - cargar_recetas_operativas()
4. Restaurar vistas administrativas
5. (Opcional) reconstruir publicación web

Este protocolo es suficiente para restaurar el sistema
al estado operativo previo a la pérdida de código.

---

## CIERRE DE FASE

Con esta documentación:
- La arquitectura real queda fijada
- El modelo de datos queda contractualizado
- El sistema es restaurable sin dependencia del código original
- Git puede capturar este estado como referencia estable

Se cierra formalmente la FASE XVI — Recuperación y Blindaje del Proyecto Recetas.



ESQUEMA DE ARBOL DE LOS ARCHIVOS:

## ANEXO — ESTRUCTURA REAL DEL PROYECTO (SNAPSHOT)

Estructura obtenida mediante `tree /F` sobre el directorio raíz del proyecto.

recetas_app/
│
├── bitácora de desarrollo.txt
├── CALCULO_RACIONES_ES_TEMPORAL.md
├── costos.py
├── estructura_actual.txt
├── ESTRUCTURA_JSON_RECETAS_INGREDIENTES.md
├── JSON_FUENTE_UNICA_VERDAD.md
├── LEYENDA_ESTRUCTURA_DOCUMENTACION.md
├── persistencia.py
├── prueba_persistencia.py
├── recetas_maestro.json
├── REGLAS_FORMATO_DATOS.md
│
├── data/
│ ├── ingredientes.json
│ ├── recetas_catalogo.json
│ └── unidades.json
│
├── data_compartida/
│ └── data/
│ ├── config.json
│ ├── ingredientes.json
│ ├── platos.json
│ ├── recetas.json
│ ├── recetas_backup_antes_limpieza.json
│ ├── recetas_catalogo.json
│ ├── recetas_detalle_version.json
│ ├── recetas_ingredientes.json
│ ├── recetas_ingredientes_v2.json
│ ├── recetas_maestro.json
│ ├── unidades.json
│ │
│ └── backup_prueba_gui/
│ ├── ingredientes.json
│ ├── recetas.json
│ ├── recetas_ingredientes.json
│ └── unidades.json
│
├── docs/
│ ├── ARCHIVOS_HISTORICOS.md
│ ├── config.json.md
│ ├── docs.txt
│ ├── GLOSARIO_TERMINOLOGIA_SISTEMA_RECETAS_WEB.md
│ ├── ingredientes.json.md
│ ├── recetas.json.md
│ ├── recetas_ingredientes.json.md
│ ├── unidades.json.md
│ │
│ ├── avances/
│ │ ├── 2026-01_FASE_G1_GUI_BASE.md
│ │ ├── 2026-01_FASE_G2_NOMENCLADORES.md
│ │ ├── 2026-01_FASE_G3_RECETAS.md
│ │ └── 2026-01_FASE_G4_RACIONES.md
│ │
│ ├── BITACORA_TECNICA/
│ │ └── proyecto_sistema_recetas.md
│ │
│ ├── codigo/
│ │ ├── main.py.md
│ │ ├── nomencladores.py.md
│ │ ├── persistencia.py.md
│ │ └── recetas_v2.py.md
│ │
│ ├── datos/
│ │ ├── ESTRUCTURA_JSON_RECETAS_INGREDIENTES.md
│ │ ├── ingredientes.json
│ │ ├── ingredientes.json.md
│ │ ├── recetas.json.md
│ │ ├── recetas_ingredientes.json.md
│ │ ├── unidades.json
│ │ └── unidades.json.md
│ │
│ ├── decisiones/
│ │ ├── CALCULO_RACIONES_ES_TEMPORAL.md
│ │ ├── CRITERIOS_REFACTORIZACION.md
│ │ ├── CRITERIOS_VALIDACION_ENTRADAS.md
│ │ ├── ESTRUCTURA_JSON_RECETAS_INGREDIENTES.md
│ │ ├── FASE_W1_W2_RESUMEN.md
│ │ ├── INTEGRACION_MODULOS.md
│ │ ├── JSON_FUENTE_UNICA_VERDAD.md
│ │ ├── LEYENDA_ESTRUCTURA_DOCUMENTACION.md
│ │ ├── PLAN_VARIANTE_WEB.md
│ │ ├── REGLAS_CALCULO_RACIONES.md
│ │ ├── REGLAS_DE_ORO_DEL_PROYECTO.md
│ │ └── REGLAS_FORMATO_DATOS.md
│ │
│ ├── estructura/
│ │ └── ESTRUCTURA_PROYECTO.md
│ │
│ ├── modulos/
│ │ ├── RECETAS.md
│ │ └── RECETAS_RACIONES.md
│ │
│ ├── notas/
│ │ ├── PROGRAMAS_UTILIZADOS.md
│ │ └── RECETAS_APP.md
│ │
│ └── pendientes/
│
├── modulo_consola_v1/
│ ├── main.py
│ ├── nomencladores.py
│ ├── persistencia.py
│ ├── recetas.py
│ ├── recetas_raciones.py
│ │
│ ├── data/
│ │ └── unidades.json
│ │
│ └── pycache/
│ └── persistencia.cpython-312.pyc
│
├── modulo_consola_v2/
│ ├── gui_ingredientes.py
│ ├── gui_main.py
│ ├── gui_nomencladores.py
│ ├── gui_raciones.py
│ ├── gui_recetas.py
│ ├── gui_recetas_catalogo.py
│ ├── gui_recetas_ingredientes_v2.py
│ ├── gui_recetas_maestro.py
│ ├── gui_receta_detalle.py
│ ├── gui_unidades.py
│ ├── migrar_modelo_v1.py
│ └── recetas_v2.py
│
├── modulo_web/
│ ├── exportar_recetas_web.py
│ ├── web_app.py
│ │
│ ├── routes/
│ │ ├── platos.py
│ │ ├── init.py
│ │ └── pycache/
│ │ ├── platos.cpython-312.pyc
│ │ └── init.cpython-312.pyc
│ │
│ ├── static/
│ │ └── styles.css
│ │
│ ├── templates/
│ │ ├── admin_ingredientes.html
│ │ ├── admin_platos.html
│ │ ├── admin_recetas.html
│ │ ├── admin_receta_detalle.html
│ │ ├── admin_unidades.html
│ │ ├── index.html
│ │ ├── nueva_receta.html
│ │ └── receta_detalle.html
│ │
│ ├── web_data/
│ │ ├── plato.json
│ │ └── recetas_publicadas.json
│ │
│ └── pycache/
│ └── web_app.cpython-312.pyc
│
└── pycache/
├── gui_ingredientes.cpython-312.pyc
├── gui_main.cpython-312.pyc
├── gui_nomencladores.cpython-312.pyc
├── gui_raciones.cpython-312.pyc
├── gui_recetas.cpython-312.pyc
├── gui_recetas_catalogo.cpython-312.pyc
├── gui_recetas_ingredientes_v2.cpython-312.pyc
├── gui_recetas_maestro.cpython-312.pyc
├── gui_receta_detalle.cpython-312.pyc
├── gui_unidades.cpython-312.pyc
├── nomencladores.cpython-312.pyc
├── persistencia.cpython-312.pyc
├── recetas.cpython-312.pyc
├── recetas_raciones.cpython-312.pyc
└── recetas_v2.cpython-312.pyc


---

**Listo.**  
Con este anexo, la bitácora queda **100 % autocontenida**: concepto + contratos + flujo + restauración + **estructura exacta**.

Cuando quieras, seguimos con código o descansamos.


======================================= ¿CÓMO ARRANCA LA CONSOLA Y POR QUÉ ======================================

## Ejecución correcta del módulo web (Flask)

El módulo web del sistema de recetas debe iniciarse usando ejecución
como módulo de paquete, NO como script directo.

Comando correcto:

    python -m modulo_web.web_app

Motivo técnico:

- `modulo_web` es un paquete Python (contiene __init__.py)
- El código utiliza imports entre módulos del paquete
- Ejecutar `web_app.py` directamente rompe el contexto de imports

El uso de `-m` garantiza:
- Resolución correcta de imports
- Inicialización adecuada del paquete
- Ejecución estable del servidor Flask

Este comando es obligatorio para el entorno de desarrollo web.


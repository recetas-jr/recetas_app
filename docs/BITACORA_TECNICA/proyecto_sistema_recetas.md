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


---

## 📅 2026-02 — Fase XIX — Master Web: borrados, validaciones y estabilidad

### 🎯 Objetivo
Consolidar el módulo web del MASTER de recetas incorporando:
- Borrado seguro de recetas.
- Borrado seguro en nomencladores (platos, unidades, ingredientes).
- Validaciones cruzadas contra el MASTER.
- Mejoras de usabilidad en el formulario (flujo por ENTER, control de abandono de datos, ajustes de UI).
- Estabilización de persistencia y rutas reales de guardado.

---

### 🧩 Cambios técnicos

#### Backend (Flask / Persistencia)
- Implementado borrado de **recetas MASTER**:
  - `POST /admin/recetas/borrar/<id>`
- Implementado borrado de **platos** con validación:
  - Si el plato está usado por alguna receta → se bloquea el borrado.
  - Si no está usado → se permite y se guarda.
- Implementado borrado de:
  - Unidades de medida (con validación de uso en ingredientes).
  - Ingredientes.
- Estandarizado uso de:
  - `cargar_recetas_maestro()`
  - `guardar_datos(RECETAS_MAESTRO_FILE, ...)`
- Corregidas rutas reales de guardado para evitar inconsistencias entre carpetas.
- Añadidos mensajes `flash`:
  - Éxito al borrar.
  - Error cuando un elemento está en uso.
  - En el caso de platos, el mensaje incluye el **nombre del plato resaltado**.

#### Frontend (Templates)

**admin_recetas.html**
- Botón de borrado por fila en el listado de recetas con confirmación.
- Control de cambios no guardados al cambiar de plato.
- Flujo de foco por ENTER entre campos.
- Ajustes de anchos:
  - Raciones base reducido.
  - Cantidad reducida.
  - Ingrediente ajustado.
- Visualización del **nombre de la unidad de medida** junto a la cantidad.
- Listado inferior compactado:
  - Anchos definidos para ID Receta, ID Plato, Raciones, #Ingredientes y Borrar.
  - Se mantiene scroll horizontal.

**admin_platos.html**
- Columna “Borrar” con icono 🗑️ por fila y confirmación.
- Integración con backend para:
  - Bloquear borrado si el plato está en uso en el MASTER.
  - Mostrar mensaje de error o éxito con `flash`.

---

### 🧠 Reglas funcionales

- ❌ No se puede borrar un **plato** si está usado por alguna receta MASTER.
- ❌ No se puede borrar una **unidad** si está usada por algún ingrediente.
- ❌ No se puede borrar un **ingrediente** si está en uso (según validación).
- ✅ El borrado de **recetas MASTER** es directo pero siempre con confirmación.
- ⚠️ Si hay datos no guardados y se cambia de plato:
  - El sistema advierte y permite cancelar.

---

### 🗂️ Control de versiones (Git)

- Se consolidó el uso de Git en el proyecto.
- Se realizaron commits que incluyen:
  - Borrados en MASTER y nomencladores.
  - Validaciones cruzadas.
  - Ajustes de UI y flujo de captura.
  - Cambios en persistencia.
  - Inclusión de documentación en `docs/`.
- El proyecto queda listo para backup completo copiando la carpeta `recetas_app` con su `.git`.

---

### ✅ Estado actual

- El sistema permite:
  - Crear, listar y borrar recetas MASTER.
  - Administrar platos, ingredientes y unidades con validaciones de integridad.
- El flujo de captura es estable y controlado.
- La integridad referencial entre MASTER y nomencladores está protegida.

---

### 📌 Próximos pasos

- Pulir detalles finos de UX (ESC para cancelar, pequeños ajustes visuales).
- Consolidar reglas finales de edición (no solo borrado).
- Preparar fase de pruebas con datos reales.
- Documentar la estructura final de datos como “fuente única de verdad”.

---
📜 2) Decisión 1 — Integridad en borrados
📄 Archivo nuevo: docs/decisiones/INTEGRIDAD_BORRADOS_MASTER.md
👉 Contenido exacto:

# Decisión: Integridad referencial en borrados (MASTER y nomencladores)

## Contexto
El sistema maneja:
- Nomencladores: Platos, Ingredientes, Unidades de Medida.
- Un MASTER de recetas que depende de esos nomencladores.

Borrar un elemento referenciado puede romper la coherencia del sistema.

## Decisión

1. ❌ No se permite borrar un PLATO si:
   - Está siendo usado por al menos una receta en el MASTER.

2. ❌ No se permite borrar una UNIDAD DE MEDIDA si:
   - Está asociada a al menos un ingrediente.

3. ❌ No se permite borrar un INGREDIENTE si:
   - Está siendo usado en alguna receta (según validación definida).

4. ✅ Sí se permite borrar una RECETA MASTER:
   - Siempre con confirmación explícita del usuario.

## Implementación

- Las validaciones se hacen en backend antes de ejecutar el borrado.
- Si el elemento está en uso:
  - Se bloquea la operación.
  - Se muestra un mensaje claro al usuario.
- Si no está en uso:
  - Se borra.
  - Se guarda persistencia.
  - Se notifica éxito.

## Consecuencias

- Se protege la integridad de los datos.
- Se evita dejar recetas huérfanas o referencias rotas.
- Se prioriza seguridad de datos sobre comodidad operativa.
📜 3) Decisión 2 — Flujo de captura en MASTER Web
📄 Archivo nuevo: docs/decisiones/FLUJO_CAPTURA_MASTER_WEB.md
👉 Contenido exacto:

# Decisión: Flujo de captura en MASTER Web y control de abandono de datos

## Contexto
El formulario MASTER de recetas es largo y con múltiples campos.
El usuario puede cambiar de plato o abandonar una receta sin guardarla, perdiendo datos.

## Decisión

1. Se implementa control de “cambios no guardados”.
2. Si el usuario intenta cambiar de plato y hay datos sin guardar:
   - El sistema muestra una advertencia.
   - El usuario puede cancelar o continuar.
3. Se estandariza el uso de ENTER para:
   - Avanzar entre campos.
   - Agilizar la captura.
4. El botón “Finalizar y Guardar” es la única acción que:
   - Confirma y persiste la receta.

## Implementación

- Se mantiene un flag `hayCambiosNoGuardados`.
- Se marca en cualquier input o textarea modificado.
- Al cambiar de plato:
  - Si hay cambios → se pide confirmación.
- El flujo de foco se controla por JavaScript.

## Consecuencias

- Se reduce el riesgo de pérdida accidental de datos.
- Se mejora la experiencia del operador.
- El sistema se comporta de forma predecible y segura.


## 📅 2026-02 — Fase XX — Estabilización del flujo de captura en MASTER Web

### 🎯 Objetivo
Pulir y estabilizar la experiencia de captura del MASTER de recetas en la versión Web, garantizando:
- Flujo continuo por teclado (ENTER).
- Cancelación global segura (ESC).
- Protección contra pérdida de datos al cambiar de receta/plato sin guardar.

---

### 🧩 Cambios implementados (Frontend)

Archivo principal afectado:
- `modulo_web/templates/admin_recetas.html`

Se consolidaron las siguientes reglas de UX:

#### 1) Flujo por ENTER
- ENTER avanza el foco entre los campos del formulario en el orden definido.
- En el campo **Cantidad**, ENTER:
  - Valida selección de ingrediente y valor numérico.
  - Agrega el ingrediente a la tabla.
  - Actualiza el JSON oculto (`ingredientes_json`).
  - Devuelve el foco al selector de Ingrediente.

#### 2) ESC como cancelación global
- Al presionar **ESC** en cualquier punto del formulario:
  - Se limpia toda la captura en curso.
  - Se vacía la tabla de ingredientes.
  - Se resetean los campos y banderas internas.
  - El foco vuelve al primer escaque (**Plato**).

Esto permite abortar una receta en cualquier momento y empezar de nuevo sin efectos colaterales.

#### 3) Control de abandono de datos (cambio de Plato)
- Se implementó un blindaje doble para detectar datos en curso:
  - Bandera: `hayCambiosNoGuardados`
  - Contenido real: `listaIngredientes.length > 0`
- Al cambiar el **Plato**:
  - Si hay datos en curso → se muestra advertencia de confirmación.
  - Si el usuario cancela → se restaura el Plato anterior.
  - Si confirma → se limpia el formulario y se continúa.

Esto evita pérdidas silenciosas de trabajo en curso.

#### 4) Marcado de cambios
- La bandera `hayCambiosNoGuardados` se activa:
  - Al escribir en campos de edición.
  - Al agregar ingredientes a la receta.
- Se resetea:
  - Al guardar.
  - Al usar ESC (cancelación total).
  - Al limpiar el formulario tras confirmar cambio de Plato.

---

### ✅ Resultado

- El MASTER Web queda con un flujo de captura:
  - Predecible
  - Seguro
  - 100% operable por teclado
- Se elimina el riesgo de perder datos sin advertencia.
- Se consolida un comportamiento de UX estable que sirve como base para futuras mejoras.

---

### 🗂️ Nota de control de versiones

Este hito corresponde a un punto estable del proyecto y debe quedar registrado en Git como:
- Estabilización del flujo de captura (ENTER / ESC / control de abandono).

## 🧩 Fase XX — Estabilización del MASTER de Recetas (Web)

**Commit de referencia:** `899b4e1`

### Estado actual (BASE ESTABLE)

Queda estabilizado el flujo del MASTER de Recetas en la versión web con las siguientes garantías:

- ✅ Flujo de captura con teclado:
  - ENTER avanza por los escaques según orden definido.
  - ENTER en Cantidad agrega ingrediente.
  - ESC cancela la captura, limpia el formulario y vuelve el foco a Plato.
- ✅ Validación de raciones:
  - Se valida en cliente de forma **instantánea**.
  - No permite avanzar si el valor no es numérico o ≤ 0.
- ✅ Control de duplicados:
  - **Duplicidad de receta (por Plato):** se valida en servidor (POST).
    - Si existe, se muestra mensaje de error y se limpia el formulario según reglas actuales.
  - **Duplicidad de ingrediente:** se valida en cliente al intentar agregarlo.
    - Se muestra mensaje y se limpia solo la línea de ingrediente.
- ✅ Listado de recetas separado:
  - Captura: `/admin/recetas`
  - Listado: `/admin/recetas/listado`

### Reglas de oro

- Este flujo se considera **base estable**.
- Cualquier cambio en:
  - manejo de ENTER / ESC,
  - validaciones,
  - limpieza de formulario,
  - o control de duplicados  
  debe hacerse con extremo cuidado para no romper la UX ya estabilizada.

## 2026-02-12 — Estabilización MASTER de Recetas (Web)

Se consolidó el flujo completo del módulo MASTER de Recetas en la versión web.

Cambios principales:
- Flujo de captura controlado por teclado:
  - ENTER avanza entre campos y agrega ingredientes.
  - ESC limpia todo el formulario y vuelve el foco a Plato.
- Validación inmediata de Raciones:
  - Solo se permite valor numérico entero > 0.
  - No avanza si el valor es inválido.
- Control de duplicidad:
  - No se permite crear más de una receta por Plato (regla MASTER).
  - Se muestra mensaje de error al intentar duplicar.
  - En caso de duplicado, se limpia el formulario de captura según reglas definidas.
- Control de duplicidad de ingredientes dentro de una receta:
  - Si se intenta repetir un ingrediente, se muestra mensaje y se limpia solo la línea de ingrediente.
- Separación de vistas:
  - Captura: /admin/recetas
  - Listado: /admin/recetas/listado

Estado:
- Flujo considerado estable.
- Cambios versionados en Git con commit: 899b4e1
- A partir de este punto, se continúa el desarrollo sobre esta base sin romper el flujo existente.

📅 2026-02-15 — Cierre Fase XXII — Migración del MASTER a SQLite

En esta fase se consolidó la migración del sistema desde JSON hacia SQLite como fuente principal de datos para la versión Web.

Estado de la base de datos (SQLite):
Archivo: modulo_web/recetas.db

Tablas activas y en uso:

tipos_plato

platos (incluye columna peso_racion)

unidades

ingredientes

recetas_maestro

recetas_ingredientes

recetas_detalle

Nomencladores (Web Admin):

Tipos de Plato: alta, listado y borrado en SQLite funcionando.

Unidades de Medida: alta, listado y borrado en SQLite funcionando.

Ingredientes: alta, listado y borrado en SQLite funcionando.

Platos: alta, listado y borrado en SQLite funcionando (con peso_racion en DB).

MASTER de Recetas (Web Admin):

Captura de recetas guardando en SQLite.

Guardado de ingredientes en recetas_ingredientes.

Guardado de textos técnicos en recetas_detalle.

Listado de recetas leído desde SQLite.

Borrado de recetas eliminando:

recetas_ingredientes

recetas_detalle

recetas_maestro

Navegación estable entre captura y listado.

Fallback a JSON:

Se mantiene un fallback a JSON en caso de fallo de la base de datos, pero el flujo principal ya es SQLite.

Herramientas añadidas:

fix_db.py: agregó columna peso_racion a platos.

fix_db_detalle.py: creó la tabla recetas_detalle.

Comando de backup:

python -m modulo_web.commands.backup_db

Exportador DB → JSON:

modulo_web/utils/export_db_a_json.py

Control de versiones:

Se realizó commit de cierre de fase:

"Fase XXII: MASTER en SQLite con detalle, nomencladores en DB, borrado y listado estables"

Decisiones de alcance:

En esta fase solo se cubren:

Alta

Listado

Borrado

La edición de registros se pospone para fases posteriores.

Estado final de la fase:

El sistema queda estable con SQLite como backend principal.

La arquitectura queda lista para:

Implementar edición,

Normalizar relaciones (Platos ↔ Tipos de Plato),

O preparar la Web pública.

## Fase XXIII — Estandarización UI y cierre parcial de Nomenclador PLATOS

**Fecha:** 2026-02-20  
**Estado:** PLATOS cerrado por ahora (funcional y estandarizado)

### Objetivo
Estandarizar la interfaz y el comportamiento de los nomencladores, tomando **PLATOS** como referencia para replicar el patrón en:
- Tipos de Plato
- Unidades de Medida (UM)
- Ingredientes
- (Luego) Master de Recetas

### Cambios y reglas aplicadas en PLATOS

#### 1) Interfaz (UI)
- Títulos de escaques (labels de captura) en **color intenso** y **negrita**.
- Encabezados de tabla y títulos de columnas en **color intenso** y **negrita**.
- Ajuste de anchos de escaques:
  - **Nombre del plato** más ancho.
  - **Tipo del plato** ancho medio.
  - **Peso ración** más estrecho.
- Texto fijo **"gramos"** a la derecha del escaque de Peso ración.
- Etiquetas en dos líneas cuando es necesario:
  - "Nombre del / plato"
  - "Tipo del / plato"
  - "Peso / ración"
- En la tabla:
  - Columna de nombre y tipo con **ancho limitado**.
  - Si el texto excede el ancho, se **corta con “…”** (ellipsis).
  - El valor de peso se muestra como: `NN.NN gramos`.
- Regla general establecida:  
  > **Ningún texto debe desbordar su columna o escaque. Todo queda limitado por ancho.**

#### 2) Comportamiento del teclado
- **Enter**:
  - En Nombre → pasa a Tipo.
  - En Tipo → pasa a Peso.
  - En Peso → **guarda**.
- **ESC**:
  - Limpia los campos del formulario.
  - Devuelve el foco a **Nombre**.
- Texto de ayuda visible en **color intenso**:
  - `<enter para guardar> | ESC aborta`

#### 3) Validaciones
- Nombre obligatorio.
- Tipo obligatorio.
- Peso ración:
  - Debe ser numérico.
  - Debe ser mayor que 0.
  - Debe ser menor o igual a 1000.0.
- Campos con límite de longitud (`maxlength`) para evitar desbordes.

#### 4) Borrado
- Botón de borrar estandarizado en la tabla.
- Confirmación antes de borrar (diálogo de confirmación).
- Mensaje de borrado:
  - Formato corto.
  - El **nombre del elemento** aparece en **rojo intenso**.
  - El resto del mensaje en **verde intenso**.
  - Ejemplo conceptual:  
    `xxxxxx borrado de Pla. correctamente.`
    (donde `xxxxxx` va en rojo).

#### 5) Criterios de estandarización definidos
Estos criterios se replicarán en:
- Tipos de Plato (T.P.)
- Unidades de Medida (UM)
- Ingredientes (Ing.)
- Master de Recetas (M.R.)

Reglas base:
- Títulos y encabezados en color intenso.
- Campos con ancho fijo y sin desbordes.
- Enter para avanzar/guardar, ESC para abortar.
- Mensajes de borrado con:
  - Elemento en rojo.
  - Texto explicativo en verde.
- Confirmación antes de borrar.
- SQLite como fuente viva de datos (JSON solo para backup/import/export).

### Estado actual
- **PLATOS**: cerrado por ahora, considerado estable y referencia de UI/UX.
- **UM, Ingredientes, Tipos de Plato**: ya adaptados en gran parte al estándar, con ajustes finos pendientes/realizados durante esta fase.
- **Siguiente foco**: revisión final de estandarización en todos los nomencladores y luego abordar la **captura del Master de Recetas** con este mismo patrón.

---


## 📌 Fase: Afinado del Master de Recetas (UI, validaciones y estabilidad)

**Fecha:** 2026-02-21  
**Rama:** `fase-xix-master-web`

### 🎯 Objetivo
Mejorar la ergonomía del formulario **Master de Recetas**, reforzar validaciones críticas y estabilizar el flujo de captura, **sin romper** funcionalidades ya correctas.

---

### 🖥️ Cambios en la Interfaz (UI / UX)

- Se implementó la **Variante B** del Master:
  - Distribución de los textos en **dos columnas**: Preparación / Elaboración y Presentación / Nutrición.
  - Reducción de la altura de los textareas para que **la parte inferior del formulario sea visible** sin tanto scroll.
  - Aprovechamiento del ancho de pantalla para mejorar la lectura y escritura.

- Se añadió una **barra de acciones fija (sticky)** en la parte superior derecha con:
  - `Guardar receta`
  - `Ir al Listado`
  - `Cancelar`
  - Los botones permanecen visibles al hacer scroll, mejorando la ergonomía y velocidad de operación.

- Se aplicó **resaltado violeta claro al foco** en inputs, selects, textareas y botones para mejorar la orientación visual del operador.

- Se ajustó el campo **Raciones base** a un ancho reducido (pendiente de ajuste fino en siguiente iteración para permitir 3 cifras con comodidad).

---

### ✅ Validaciones y Flujo de Captura

- **Cantidad**:
  - Debe ser **numérica y mayor que 0**.
  - No se permite salir del campo con `Enter` si el valor es inválido.

- **Rol**:
  - Debe ser **numérico y >= 0**.
  - Puede ser **igual o menor que Cantidad** (se permite igualdad).
  - No puede ser mayor que Cantidad.
  - Rol = 0 indica que el ingrediente **no participa en decoración**.

- **Detección de duplicados de ingredientes**:
  - Al presionar `Enter` en **Rol**, se verifica si el ingrediente ya existe en la receta.
  - Si está duplicado:
    - Se muestra mensaje de error con el **nombre del ingrediente**.
    - El selector de esa fila se limpia y queda con foco.
    - No se crea nueva fila.

- **Flujo de Enter**:
  - Ingrediente → Cantidad → Rol → (si todo es válido) nueva fila.
  - Si Cantidad o Rol son inválidos, el foco **no avanza** y se muestra mensaje.

---

### 🎨 Decoración en el Listado de Recetas

- Se definió que una receta **tiene decoración** solo si:
  - Existe **al menos un ingrediente con Rol > 0**.
- El listado muestra un **icono de decoración** únicamente en ese caso.
- Se agregó una **leyenda visual**: “Tiene decoración”.

---

### 🧱 Estabilidad y Control de Cambios

- Se hizo énfasis en:
  - Ajustes **quirúrgicos** para no romper funciones existentes.
  - Separación clara entre cambios de **UI** y **lógica de negocio**.
- Se realizó un **commit de checkpoint** con:
  > `Checkpoint: Master de Recetas (UI, validaciones, listado y persistencia)`

---

### 📌 Pendientes Inmediatos

- Ajustar ligeramente el ancho del campo **Raciones base** para permitir 3 cifras cómodamente.
- Revisar y **reparar la migración** de base de datos con foco en consistencia y compatibilidad.
- Continuar fortaleciendo la documentación técnica del proyecto.



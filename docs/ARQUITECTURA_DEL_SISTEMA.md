# ARQUITECTURA DEL SISTEMA — RECETAS_APP

Este documento describe la **arquitectura técnica del sistema recetas_app**.

Su propósito es explicar:

- cómo está construido el sistema
- qué componentes existen
- cómo se comunican entre sí
- dónde reside la lógica del sistema
- dónde se almacenan los datos

Este documento complementa:

docs/MAPA_DEL_SISTEMA.md

Mientras el mapa del sistema muestra la **visión general**,  
este documento describe **la arquitectura técnica real**.

---

# PRINCIPIOS DE ARQUITECTURA

El sistema recetas_app sigue varios principios de diseño.

### Separación de capas

El sistema separa claramente:

- Interfaz
- Lógica
- Persistencia de datos

Esto facilita:

- mantenimiento
- evolución del sistema
- control de errores

---

### Integridad referencial

Las relaciones entre entidades se protegen mediante:

- validaciones en backend
- restricciones de base de datos
- reglas de negocio

Ejemplos:

- no se puede borrar un ingrediente usado en recetas
- no se puede borrar un plato asociado a una receta
- una receta no puede contener ingredientes duplicados

---

### Persistencia controlada

La información se almacena en **SQLite**.

Esto permite:

- integridad de datos
- consultas rápidas
- simplicidad operativa

---

# CAPAS DEL SISTEMA

La arquitectura se organiza en **cuatro capas principales**.


USUARIO
│
▼
INTERFAZ WEB
│
▼
LOGICA DE APLICACION
│
▼
BASE DE DATOS


Cada capa cumple una función específica.

---

# CAPA 1 — USUARIO

El usuario interactúa con el sistema mediante el navegador web.

Existen dos tipos de usuario.

### Usuario de consulta

Puede:

- consultar recetas
- ver ingredientes
- recalcular raciones

No puede modificar datos.

---

### Administrador del sistema

Puede:

- gestionar nomencladores
- crear recetas
- borrar recetas
- administrar ingredientes
- administrar unidades de medida

Accede al sistema mediante rutas:


/admin/*


---

# CAPA 2 — INTERFAZ WEB

La interfaz web está implementada mediante **Flask**.

Archivo principal:


modulo_web/web_app.py


Responsabilidades:

- recibir solicitudes HTTP
- ejecutar lógica del sistema
- renderizar páginas HTML
- mostrar datos al usuario

---

# TEMPLATES HTML

Las plantillas HTML se encuentran en:


modulo_web/templates/


Principales plantillas del sistema:


admin_platos.html
admin_unidades.html
admin_ingredientes.html
admin_recetas_nueva.html
admin_recetas_listado.html
index.html
receta_detalle.html


Estas plantillas utilizan **Jinja2** para renderizar datos dinámicos.

---

# RECURSOS ESTÁTICOS

Los archivos estáticos se encuentran en:


modulo_web/static/


Ejemplo:


styles.css


Estos archivos definen:

- estilos visuales
- apariencia del sistema
- comportamiento visual de la interfaz

---

# CAPA 3 — LÓGICA DE APLICACIÓN

La lógica del sistema se encuentra principalmente en:


modulo_web/web_app.py
modulo_web/persistencia_db.py


Responsabilidades principales:

- validación de datos
- control de reglas de negocio
- gestión de formularios
- control de duplicados
- control de integridad referencial

---

# EJEMPLOS DE REGLAS DE NEGOCIO

El sistema implementa reglas importantes.

### Regla de receta única

No puede existir más de una receta para el mismo plato.

---

### Ingredientes sin duplicar

Una receta no puede contener el mismo ingrediente más de una vez.

---

### Control de cantidades

- cantidad > 0
- rol ≥ 0
- rol ≤ cantidad

---

### Integridad de nomencladores

No se permite borrar elementos si están en uso.

Ejemplos:

- unidad usada por ingredientes
- ingrediente usado en recetas
- plato usado por recetas

---

# CAPA 4 — BASE DE DATOS

El sistema utiliza SQLite.

Archivo:


modulo_web/recetas.db


La base de datos contiene varias tablas.

---

# TABLAS DEL SISTEMA

## tipos_plato

Define categorías de platos.

Ejemplo:

- Entrada
- Plato fuerte
- Postre

---

## platos

Define los platos del sistema.

Campos principales:

- id
- nombre
- tipo_plato_id
- peso_racion

---

## unidades

Define las unidades de medida.

Ejemplos:

- g
- kg
- ml
- l
- unidad

---

## ingredientes

Define los ingredientes disponibles.

Campos:

- id
- nombre
- unidad_id

---

## recetas_maestro

Define las recetas.

Campos:

- id
- plato_id
- raciones_base

---

## recetas_ingredientes

Relaciona recetas con ingredientes.

Campos:

- receta_id
- ingrediente_id
- cantidad
- rol

---

## recetas_detalle

Contiene textos técnicos de la receta.

Campos:

- preparacion
- elaboracion
- presentacion
- nutricion

---

# RELACIONES PRINCIPALES

Relación conceptual del sistema:


PLATO
│
│ 1
│
└───────────∞
RECETA
│
│ 1
│
└──────────∞
INGREDIENTES


Esto significa:

- un plato tiene una receta
- una receta tiene muchos ingredientes

---

# ESTRUCTURA GENERAL DEL PROYECTO

El sistema está organizado en carpetas.


recetas_app/

├─ modulo_web/
│ ├─ web_app.py
│ ├─ persistencia_db.py
│ ├─ recetas.db
│ │
│ ├─ templates/
│ └─ static/
│
├─ data_compartida/
│
├─ docs/
│
├─ modulo_consola_v1/
├─ modulo_consola_v2/


---

# COMPONENTES HISTÓRICOS

El sistema evolucionó a través de varias etapas.

### Fase 1

Aplicación de consola.

---

### Fase 2

Interfaz gráfica con Tkinter.

---

### Fase 3

Migración a aplicación web.

---

### Fase 4

Persistencia en SQLite.

---

# DOCUMENTACIÓN DEL SISTEMA

Toda la documentación se encuentra en:


docs/


Documentos principales:


START_HERE.md
INDICE_DOCUMENTACION.md
MAPA_DEL_SISTEMA.md
ARQUITECTURA_DEL_SISTEMA.md


---

# OBJETIVO DEL SISTEMA

El sistema recetas_app permite:

- gestionar recetas gastronómicas
- estandarizar ingredientes
- controlar cantidades
- facilitar consulta de recetas

El sistema también sirve como base futura para:

- costeo de recetas
- planificación de producción
- control nutricional
- análisis de ingredientes

---

# FIN DEL DOCUMENTO docs/ARQUITECTURA_DEL_SISTEMA.md
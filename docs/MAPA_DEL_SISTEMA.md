# MAPA DEL SISTEMA — RECETAS_APP

Este documento muestra **cómo está construido el sistema completo de recetas**.

Su objetivo es que cualquier persona pueda entender rápidamente:

- qué partes tiene el sistema
- cómo se conectan
- dónde están los datos
- qué hace cada componente

Este documento es un **mapa general del sistema**.

---

# VISIÓN GENERAL DEL SISTEMA

El sistema recetas_app permite:

- administrar recetas gastronómicas
- gestionar ingredientes
- controlar unidades de medida
- consultar recetas y calcular raciones

El sistema tiene dos tipos de usuarios:

**Administrador**
- crea y gestiona recetas
- mantiene los nomencladores

**Usuario**
- consulta recetas
- recalcula raciones
- no modifica datos

---

# ARQUITECTURA GENERAL

El sistema está organizado en **capas**.


USUARIO
│
▼
INTERFAZ WEB (Flask)
│
▼
LOGICA DE APLICACION
│
▼
CAPA DE DATOS (SQLite)


Cada capa tiene responsabilidades específicas.

---

# CAPA 1 — USUARIO

Existen dos tipos de usuario.

### Usuario de consulta

Puede:

- ver recetas
- consultar ingredientes
- recalcular raciones

No puede modificar datos.

---

### Administrador del sistema

Puede:

- crear recetas
- borrar recetas
- editar nomencladores
- gestionar ingredientes
- gestionar unidades

Accede al sistema mediante:


/admin/*


---

# CAPA 2 — INTERFAZ WEB

La interfaz web está implementada con **Flask**.

Archivo principal:


modulo_web/web_app.py


Funciones principales:

- recibir solicitudes HTTP
- ejecutar lógica del sistema
- renderizar plantillas HTML
- mostrar datos al usuario

Las páginas HTML se encuentran en:


modulo_web/templates/


Ejemplos:


admin_platos.html
admin_ingredientes.html
admin_unidades.html
admin_recetas_nueva.html
index.html
receta_detalle.html


Los estilos se encuentran en:


modulo_web/static/styles.css


---

# CAPA 3 — LÓGICA DEL SISTEMA

La lógica principal del sistema se encuentra en:


modulo_web/web_app.py
modulo_web/persistencia_db.py


Responsabilidades:

- validaciones
- reglas de negocio
- control de duplicados
- control de integridad referencial
- procesamiento de formularios

Ejemplos de reglas:

- no puede existir más de una receta por plato
- un ingrediente no puede repetirse dentro de una receta
- el rol no puede ser mayor que la cantidad
- no se pueden borrar elementos en uso

---

# CAPA 4 — BASE DE DATOS

El sistema utiliza **SQLite**.

Archivo de base de datos:


modulo_web/recetas.db


Tablas principales:


tipos_plato
platos
unidades
ingredientes
recetas_maestro
recetas_ingredientes
recetas_detalle


Relación principal del sistema:


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
├─ modulo_consola_v1/ (histórico)
├─ modulo_consola_v2/ (histórico)


---

# COMPONENTES PRINCIPALES DEL SISTEMA

Los componentes fundamentales del sistema son:

### Nomencladores

Definen los catálogos del sistema.

Ejemplos:

- Tipos de plato
- Platos
- Unidades de medida
- Ingredientes

---

### MASTER de Recetas

Define la receta técnica completa.

Incluye:

- plato
- raciones base
- ingredientes
- cantidades
- rol del ingrediente
- preparación
- elaboración
- presentación
- nutrición

---

### Web Admin

Permite administrar el sistema.

Rutas principales:


/admin/platos
/admin/unidades
/admin/ingredientes
/admin/recetas


---

### Web Pública

Permite consultar recetas.

Ejemplos de rutas:


/
/receta/<id>


---

# PRINCIPIOS DE DISEÑO DEL SISTEMA

El sistema sigue varias reglas de diseño.

### Integridad de datos

No se permiten relaciones rotas.

Ejemplo:

- no se puede borrar un ingrediente en uso

---

### Separación de responsabilidades

El sistema separa:

- interfaz
- lógica
- datos

Esto facilita mantenimiento.

---

### Documentación integrada

Toda la documentación del sistema se encuentra en:


docs/


Documentos clave:


START_HERE.md
INDICE_DOCUMENTACION.md
MAPA_DEL_SISTEMA.md


---

# PROPÓSITO DEL SISTEMA

El sistema recetas_app fue diseñado para:

- gestionar recetas gastronómicas
- estandarizar ingredientes
- controlar cantidades
- facilitar consulta de recetas
- servir como base para cálculos futuros
  (costeo, producción, planificación)

---

# FIN DEL DOCUMENTO docs/MAPA_DEL_SISTEMA.md
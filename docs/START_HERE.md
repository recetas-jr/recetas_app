# START HERE — Sistema de Recetas (recetas_app)

Bienvenido al proyecto **recetas_app**.

Este documento es el **punto de entrada oficial** al sistema.  
Si es la primera vez que ves el proyecto, comienza aquí.

El objetivo de este documento es permitir que cualquier persona comprenda rápidamente:

- qué es el sistema
- cómo está organizado
- cómo ejecutarlo
- dónde encontrar la información importante

---

# 1. ¿Qué es este sistema?

**recetas_app** es un sistema para gestionar **recetas culinarias profesionales**.

El sistema permite:

- administrar **nomencladores**
- crear **recetas técnicas (MASTER)**
- consultar recetas desde una **interfaz web**

El sistema está pensado para:

- producción gastronómica
- control de recetas
- estandarización culinaria
- consulta por parte de usuarios de cocina

---

# 2. Tipos de usuarios del sistema

El sistema distingue dos tipos de usuarios.

## Administrador del sistema

Puede:

- crear platos
- crear ingredientes
- crear unidades de medida
- crear recetas MASTER
- borrar registros

Accede mediante:


/admin/*


Ejemplos:


/admin/platos
/admin/ingredientes
/admin/unidades
/admin/recetas


---

## Usuario de consulta

El usuario normal **no modifica datos**.

Solo puede:

- consultar recetas
- ver ingredientes
- ver procedimiento
- recalcular raciones

Accede mediante:


/


---

# 3. Arquitectura general del sistema

El sistema se organiza en **capas claramente separadas**.


Usuario
│
▼
Interfaz Web (Flask)
│
▼
Lógica de aplicación
│
▼
Persistencia de datos
│
▼
Base de datos SQLite


Componentes principales:


modulo_web/
persistencia_db.py
recetas.db
templates/
static/


---

# 4. Componentes principales del proyecto

El sistema contiene cuatro áreas fundamentales.

## 1. Interfaz Web

Ubicación:


modulo_web/


Contiene:

- servidor Flask
- rutas
- templates HTML
- estilos CSS

Archivo principal:


modulo_web/web_app.py


---

## 2. Lógica del sistema

La lógica del sistema se encarga de:

- validaciones
- reglas de negocio
- gestión de recetas
- control de ingredientes

Parte de esta lógica se encuentra en:


web_app.py
persistencia_db.py


---

## 3. Base de datos

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


---

## 4. Documentación

Toda la documentación del proyecto se encuentra en:


docs/


Para navegar la documentación completa ver:


docs/INDICE_DOCUMENTACION.md


---

# 5. Cómo ejecutar el sistema

Desde la carpeta raíz del proyecto ejecutar:


python -m modulo_web.web_app


Esto inicia el servidor Flask.

Luego abrir en el navegador:


http://127.0.0.1:5000


---

# 6. Estructura básica del proyecto


recetas_app/
│
├─ modulo_web/
│ ├─ web_app.py
│ ├─ persistencia_db.py
│ ├─ templates/
│ └─ static/
│
├─ docs/
│
└─ data/


---

# 7. Conceptos clave del sistema

## Nomencladores

Catálogos controlados del sistema.

Ejemplos:

- unidades de medida
- ingredientes
- platos
- tipos de plato

---

## Receta MASTER

La receta MASTER es la **ficha técnica completa de un plato**.

Contiene:

- plato
- raciones base
- ingredientes
- cantidades
- textos técnicos
- nutrición

---

# 8. Documentos importantes

Después de leer este documento, el orden recomendado es:

1️⃣


docs/MAPA_DEL_SISTEMA.md


2️⃣


docs/INDICE_DOCUMENTACION.md


3️⃣

Documentos dentro de:


docs/arquitectura/


---

# 9. Estado actual del proyecto

El sistema actualmente incluye:

- administración de nomencladores
- creación de recetas MASTER
- persistencia en SQLite
- validaciones completas
- interfaz web estable

El sistema se encuentra en **fase de evolución continua**.

---

# Fin del documento docs/START_HERE.md
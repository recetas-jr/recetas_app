# INDICE GENERAL DE DOCUMENTACIÓN — SISTEMA RECETAS_APP

Este documento funciona como **mapa de navegación de toda la documentación del proyecto**.

Su objetivo es permitir localizar rápidamente:

- arquitectura del sistema
- estructura del proyecto
- decisiones técnicas
- documentación de datos
- bitácora del proyecto
- documentos históricos

Este índice se consulta **cuando se necesita investigar o analizar el sistema**.

Para comenzar a entender el sistema desde cero, primero leer:


docs/START_HERE.md


---

# 1. DOCUMENTOS DE ENTRADA AL SISTEMA

Estos documentos permiten comprender el sistema rápidamente.


docs/START_HERE.md


Documento de entrada al sistema.

Explica:

- qué es el sistema
- cómo ejecutarlo
- estructura general
- conceptos principales

---

# 2. DOCUMENTACIÓN DE ARQUITECTURA

Describe **cómo está construido el sistema**.

Ubicación:


docs/arquitectura/


Documentos principales:


MAPA_ARQUITECTONICO_RECETAS_APP.md
SUPER_MAPA_ARQUITECTONICO_COMPLETO.md
MAPA_DE_SEGURIDAD_RECETAS_APP.md


Contenido:

- capas del sistema
- relaciones entre módulos
- componentes críticos
- zonas de seguridad

---

# 3. FLUJO DEL SISTEMA

Describe **cómo circula la información dentro del sistema**.

Documento:


II-FLUJO_DEL_SISTEMA_RECETAS_APP.md


Contenido:

- flujo de creación de recetas
- flujo de edición
- validaciones
- interacción usuario–sistema

---

# 4. MODELO DE DATOS

Describe **la estructura de la información del sistema**.

Documento principal:


I-ESQUEMA_BASE_DATOS_RECETAS_APP.md


Contenido:

- entidades del sistema
- relación receta–ingrediente
- unidades de medida
- reglas de integridad

---

# 5. DOCUMENTACIÓN DEL PROYECTO

Ubicación:


docs/


Incluye documentos sobre:

- estructura del proyecto
- nomencladores
- reglas del sistema
- formato de datos

Documentos relevantes:


docs/estructura/ESTRUCTURA_PROYECTO.md
docs/decisiones/REGLAS_DE_ORO_DEL_PROYECTO.md
docs/decisiones/PLAN_VARIANTE_WEB.md
docs/decisiones/REGLAS_FORMATO_DATOS.md


---

# 6. BITÁCORA TÉCNICA DEL PROYECTO

Registro histórico del desarrollo.

Ubicación:


docs/BITACORA_TECNICA/


Documento principal:


docs/BITACORA_TECNICA/proyecto_sistema_recetas.md


Contenido:

- evolución del sistema
- decisiones técnicas
- problemas detectados
- cambios importantes

---

# 7. DOCUMENTACIÓN DE AVANCES

Describe las fases del desarrollo del sistema.

Ubicación:


docs/avances/


Ejemplos:


2026-01_FASE_G1_GUI_BASE.md
2026-01_FASE_G2_NOMENCLADORES.md
2026-01_FASE_G3_RECETAS.md
2026-01_FASE_G4_RACIONES.md


---

# 8. DOCUMENTACIÓN DEL CÓDIGO

Explica archivos importantes del sistema.

Ubicación:


docs/codigo/


Ejemplos:


main.py.md
persistencia.py.md
recetas_v2.py.md


---

# 9. DOCUMENTACIÓN DE DATOS

Explica la estructura de los archivos de datos.

Ubicación:


docs/datos/


Ejemplos:


ingredientes.json.md
unidades.json.md
recetas_ingredientes.json.md


---

# 10. GLOSARIO DEL SISTEMA

Define el vocabulario oficial del proyecto.

Documento:


GLOSARIO_TERMINOLOGIA_SISTEMA_RECETAS_WEB.md


Define términos como:

- nomenclador
- receta MASTER
- ingrediente
- raciones base
- unidad de medida

---

# 11. ESTRUCTURA GENERAL DEL PROYECTO

Para entender cómo está organizado el código:


docs/estructura/ESTRUCTURA_PROYECTO.md


Este documento explica:

- carpetas del sistema
- módulos
- componentes activos
- componentes históricos

---

# 12. ORDEN RECOMENDADO DE LECTURA

Para comprender completamente el sistema:

1️⃣


docs/START_HERE.md


2️⃣


docs/arquitectura/MAPA_ARQUITECTONICO_RECETAS_APP.md


3️⃣


docs/arquitectura/SUPER_MAPA_ARQUITECTONICO_COMPLETO.md


4️⃣


docs/estructura/ESTRUCTURA_PROYECTO.md


5️⃣


docs/BITACORA_TECNICA/proyecto_sistema_recetas.md


---

# 13. OBJETIVO DE ESTA DOCUMENTACIÓN

Toda la documentación del sistema existe para:

- facilitar mantenimiento del sistema
- permitir comprensión rápida del proyecto
- evitar pérdida de conocimiento
- permitir restaurar el sistema en caso de fallo

La documentación forma parte esencial del sistema.

---

# FIN DEL DOCUMENTO docs/INDICE_DOCUMENTACION.md
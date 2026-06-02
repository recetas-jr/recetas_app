II-FLUJO DEL SISTEMA — RECETAS_APP
1. Propósito del documento

Este documento describe el flujo operativo del sistema recetas_app.
Su objetivo es explicar cómo interactúan:

el usuario

la interfaz web

la lógica del sistema

los archivos de datos

para gestionar recetas e ingredientes.

2. Flujo general del sistema

El funcionamiento general del sistema sigue el siguiente flujo:

Usuario
   │
   ▼
Interfaz Web
   │
   ▼
Lógica de la Aplicación
   │
   ▼
Validaciones
   │
   ▼
Persistencia en archivos JSON

Este flujo se ejecuta cada vez que el usuario realiza una operación en el sistema.

3. Flujo de creación de una receta

El proceso para crear una receta es el siguiente.

Usuario abre el módulo recetas
        │
        ▼
Formulario de nueva receta
        │
        ▼
Usuario introduce datos
        │
        ▼
Sistema valida datos
        │
        ▼
Receta se guarda en recetas.json

Datos mínimos requeridos:

nombre de receta

categoría

raciones base

4. Flujo de edición de una receta

Cuando el usuario edita una receta existente ocurre el siguiente proceso.

Usuario selecciona receta
        │
        ▼
Sistema carga datos de la receta
        │
        ▼
Usuario modifica información
        │
        ▼
Sistema valida cambios
        │
        ▼
Sistema actualiza archivo recetas.json
5. Flujo de gestión de ingredientes

Cada receta puede contener múltiples ingredientes.

Proceso de adición de ingredientes:

Usuario abre receta
        │
        ▼
Usuario agrega ingrediente
        │
        ▼
Sistema valida cantidad y unidad
        │
        ▼
Ingrediente se registra en recetas_ingredientes.json

Cada ingrediente incluye:

nombre del ingrediente

cantidad

unidad de medida

6. Validaciones del sistema

Antes de guardar información el sistema aplica varias validaciones.

Principales validaciones:

el nombre de la receta no puede estar vacío

la cantidad de ingrediente debe ser mayor que cero

la unidad debe existir en el nomenclador

las raciones base deben ser mayores que cero

Estas validaciones evitan inconsistencias en los datos.

7. Persistencia de datos

El sistema guarda la información en archivos JSON.

Archivos principales utilizados:

recetas.json
recetas_maestro.json
recetas_ingredientes.json
unidades.json

Estos archivos se encuentran en:

data_compartida/data/
8. Flujo de lectura de datos

Cuando el sistema necesita mostrar información realiza el siguiente proceso.

Sistema solicita datos
        │
        ▼
Lectura de archivos JSON
        │
        ▼
Procesamiento de datos
        │
        ▼
Datos enviados a la interfaz web
9. Consideraciones operativas

El sistema está diseñado para trabajar con archivos JSON debido a su simplicidad y portabilidad.

Sin embargo, esta arquitectura requiere:

control de validaciones

cuidado en la edición de archivos

protección contra inconsistencias

10. Evolución futura

En versiones futuras del sistema el flujo podría evolucionar hacia:

persistencia en base de datos SQLite

mayor control de integridad de datos

optimización de acceso a información

Estas mejoras permitirán aumentar la robustez del sistema.
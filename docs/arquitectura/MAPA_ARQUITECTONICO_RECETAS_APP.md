III-MAPA ARQUITECTONICO DEL SISTEMA — RECETAS_APP
1. Propósito del documento

Este documento describe la arquitectura general del sistema recetas_app.

Su objetivo es definir:

los componentes principales del sistema

la relación entre módulos

la estructura lógica del sistema

la organización de los datos

Este documento sirve como referencia arquitectónica para el desarrollo y mantenimiento del sistema.

2. Visión general del sistema

El sistema recetas_app es una aplicación destinada a la gestión de recetas culinarias.

Permite:

crear recetas

editar recetas

gestionar ingredientes

controlar cantidades y unidades

El sistema se ejecuta mediante una interfaz web que interactúa con una lógica de aplicación y con archivos de datos.

3. Componentes principales del sistema

El sistema se compone de los siguientes elementos principales.

Usuario
Interfaz Web
Lógica de Aplicación
Sistema de Validaciones
Archivos de Datos

Cada uno cumple una función específica dentro del sistema.

4. Estructura general del sistema

La arquitectura general del sistema puede representarse de la siguiente manera.

Usuario
   │
   ▼
Interfaz Web
   │
   ▼
Lógica del Sistema
   │
   ▼
Validaciones
   │
   ▼
Persistencia de Datos (JSON)

Esta estructura define el flujo de funcionamiento del sistema.

5. Interfaz Web

La interfaz web permite la interacción entre el usuario y el sistema.

Sus funciones principales son:

mostrar recetas

mostrar ingredientes

permitir la edición de datos

enviar información al sistema

La interfaz actúa como punto de entrada al sistema.

6. Lógica de aplicación

La lógica de aplicación procesa las acciones realizadas por el usuario.

Sus responsabilidades incluyen:

gestión de recetas

gestión de ingredientes

control de raciones

interacción con los archivos de datos

Esta capa representa el núcleo funcional del sistema.

7. Sistema de validaciones

El sistema incorpora validaciones para garantizar la integridad de los datos.

Entre las validaciones principales se encuentran:

campos obligatorios

valores numéricos válidos

unidades de medida válidas

consistencia de datos

Estas validaciones evitan errores en la información almacenada.

8. Sistema de datos

El sistema utiliza archivos JSON como mecanismo de almacenamiento.

Archivos principales utilizados:

recetas.json
recetas_maestro.json
recetas_ingredientes.json
unidades.json

Estos archivos contienen la información necesaria para el funcionamiento del sistema.

9. Organización del proyecto

El proyecto está organizado en carpetas que separan:

código

datos

documentación

La documentación técnica se encuentra en la carpeta:

docs/

Dentro de esta carpeta se almacenan los documentos que describen la arquitectura, los datos y el funcionamiento del sistema.

10. Importancia del mapa arquitectónico

El mapa arquitectónico permite:

comprender la estructura del sistema

mantener coherencia en el desarrollo

facilitar futuras modificaciones

evitar errores estructurales

Este documento constituye una referencia fundamental para el mantenimiento del proyecto.

VII-DIAGRAMA VISUAL DEL SISTEMA — RECETAS_APP
1. Propósito del documento

Este documento presenta una representación visual simplificada del sistema recetas_app.

El objetivo del diagrama visual es facilitar la comprensión rápida de:

la estructura general del sistema

la relación entre sus componentes

el flujo de interacción entre usuario, aplicación y datos

Este documento complementa los mapas arquitectónicos proporcionando una visión clara e inmediata del sistema.

2. Visión general del sistema

El sistema recetas_app permite gestionar recetas culinarias mediante una interfaz web que interactúa con una lógica de aplicación y con archivos de datos.

El sistema se organiza en varios componentes que trabajan de forma coordinada.

3. Componentes principales

Los componentes principales del sistema son:

Usuario
Interfaz Web
Lógica de Aplicación
Sistema de Validaciones
Archivos de Datos

Cada componente cumple una función específica dentro del funcionamiento general del sistema.

4. Diagrama visual del sistema

La relación entre los componentes del sistema puede representarse de la siguiente manera.

                USUARIO
                   │
                   ▼
            INTERFAZ WEB
                   │
                   ▼
         LOGICA DE APLICACION
                   │
                   ▼
            VALIDACIONES
                   │
                   ▼
           ARCHIVOS DE DATOS

Este diagrama muestra el flujo básico de funcionamiento del sistema.

5. Descripción del flujo visual

El funcionamiento del sistema puede interpretarse de la siguiente forma.

El usuario interactúa con la interfaz web.

La interfaz envía las acciones del usuario a la lógica de la aplicación.

La lógica procesa la información y aplica las reglas del sistema.

El sistema ejecuta validaciones para garantizar la integridad de los datos.

Los datos se almacenan o consultan en los archivos de persistencia.

6. Ubicación del módulo principal

Dentro del diagrama, el núcleo funcional del sistema se encuentra en la lógica de aplicación.

Es en esta capa donde se realizan las operaciones principales:

gestión de recetas

gestión de ingredientes

control de raciones

interacción con los datos

Esta capa constituye el centro operativo del sistema.

7. Utilidad del diagrama visual

El diagrama visual permite:

comprender rápidamente la estructura del sistema

explicar el funcionamiento del sistema a nuevos desarrolladores

facilitar la identificación de los componentes principales

servir como referencia para la arquitectura general

Este documento actúa como representación visual de la arquitectura del sistema recetas_app.

docs/arquitectura/MAPA_ARQUITECTONICO_RECETAS_APP.md

DIAGRAMA GENERAL DEL SISTEMA

El sistema recetas_app se organiza en capas funcionales que separan la interacción del usuario, la lógica del sistema y la persistencia de datos.

INTERFAZ WEB (UI)
modulo_web/
        │
        ▼
LOGICA DE APLICACION
validaciones / procesos
        │
        ▼
MODELO DE DATOS
SQLite + nomencladores
        │
        ▼
DOCUMENTACION + CONTROL
Git + docs/

Este esquema resume la arquitectura del sistema:

La interfaz web permite la interacción del usuario.

La lógica de aplicación gestiona validaciones y procesos del sistema.

El modelo de datos almacena la información en SQLite.

La documentación y control garantizan trazabilidad mediante Git y los documentos técnicos del proyecto.
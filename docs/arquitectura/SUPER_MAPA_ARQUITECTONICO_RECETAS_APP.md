IV-SUPER MAPA ARQUITECTONICO COMPLETO DEL SISTEMA — RECETAS_APP
1. Propósito del documento

Este documento describe la arquitectura completa del sistema recetas_app a nivel de ingeniería.

Su objetivo es detallar:

las capas del sistema

los componentes principales

las dependencias entre módulos

la organización estructural del proyecto

Este documento complementa el Mapa Arquitectónico del Sistema, proporcionando un nivel mayor de detalle.

2. Niveles arquitectónicos del sistema

El sistema recetas_app está organizado en varios niveles o capas funcionales.

Las capas principales son:

Capa de Usuario
Capa de Interfaz Web
Capa de Lógica de Aplicación
Capa de Validaciones
Capa de Persistencia de Datos

Cada capa tiene responsabilidades específicas dentro del sistema.

3. Capa de usuario

Esta capa representa al usuario que interactúa con el sistema.

El usuario puede realizar acciones como:

consultar recetas

crear nuevas recetas

editar recetas existentes

gestionar ingredientes

El usuario interactúa con el sistema mediante la interfaz web.

4. Capa de interfaz web

La interfaz web permite la comunicación entre el usuario y el sistema.

Sus funciones incluyen:

mostrar información al usuario

recibir datos introducidos en formularios

enviar solicitudes a la lógica de la aplicación

Esta capa constituye la puerta de entrada al sistema.

5. Capa de lógica de aplicación

La lógica de aplicación procesa las acciones realizadas por el usuario.

Entre sus responsabilidades se encuentran:

gestión de recetas

gestión de ingredientes

cálculo de raciones

actualización de datos

Esta capa contiene las reglas de negocio del sistema.

6. Capa de validaciones

Antes de almacenar o modificar información, el sistema aplica validaciones.

Las validaciones garantizan que los datos sean correctos.

Ejemplos de validaciones:

cantidades mayores que cero

unidades válidas

nombres de recetas no vacíos

coherencia de datos

Estas validaciones protegen la integridad del sistema.

7. Capa de persistencia de datos

La persistencia de datos se realiza mediante archivos JSON.

Archivos principales:

recetas.json
recetas_maestro.json
recetas_ingredientes.json
unidades.json

Estos archivos almacenan la información utilizada por el sistema.

8. Dependencias entre componentes

Los componentes del sistema interactúan siguiendo el siguiente esquema.

Usuario
   │
   ▼
Interfaz Web
   │
   ▼
Lógica de Aplicación
   │
   ▼
Validaciones
   │
   ▼
Archivos de Datos

Cada componente depende del anterior para realizar su función.

9. Organización del proyecto

El proyecto está organizado en varias áreas principales.

Código del sistema
Archivos de datos
Documentación técnica

La documentación técnica se encuentra en la carpeta:

docs/

Dentro de esta carpeta se organizan los documentos relacionados con:

arquitectura

base de datos

operación del sistema

10. Rol del super mapa arquitectónico

El Super Mapa Arquitectónico cumple las siguientes funciones:

proporcionar una visión global del sistema

facilitar el mantenimiento del proyecto

orientar futuras ampliaciones del sistema

servir como referencia para desarrolladores

Este documento constituye una guía estructural del sistema recetas_app.
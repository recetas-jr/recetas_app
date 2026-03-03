Glosario Y Terminología — Sistema De Recetas
📘 Glosario y Terminología — Sistema de Recetas
🎯 Propósito

Este documento define el vocabulario oficial del proyecto para que siempre usemos los mismos términos con el mismo significado.

👉 Cada vez que aparezca un concepto nuevo, se agrega aquí antes de seguir avanzando.

Cuando abramos una pestaña nueva, lo primero será revisar este glosario para mantener coherencia.

📐 Reglas de uso

Un concepto = un término.

No usar sinónimos si ya existe un término definido.

Si un término cambia de alcance, se actualiza aquí.

🧱 Estructura del Sistema (Conceptos Base)
🔹 Nomenclador

Conjunto de datos maestros y controlados que definen qué existe en el sistema.

Ejemplos de nomencladores:

Platos

Ingredientes

Unidades de medida

Roles de ingrediente

Características:

Se mantienen por administración.

Evitan duplicados y errores de escritura.

Alimentan al MASTER.

🔹 Plato (Entidad)

Elemento del nomenclador de platos que identifica un platillo por su nombre estandarizado.

Campos típicos:

id

nombre

tipo de plato

peso por ración

foto

👉 El plato no tiene ingredientes ni procedimiento.

🔹 Receta MASTER (Ficha Técnica)

Definición técnica completa de un plato para producción.

Relaciona:

un plato (por id)

ingredientes con cantidades

textos técnicos

datos nutricionales

👉 El MASTER se construye a partir de nomencladores.

🔹 Ingrediente (Entidad)

Elemento del nomenclador de ingredientes.

Campos típicos:

id

nombre

unidad de medida

👉 La cantidad se define en la receta, no aquí.

🔹 Unidad de Medida

Define cómo se mide un ingrediente.

Ejemplos:

g (gramos)

ml (mililitros)

unidad

Puede ser:

un campo dentro del ingrediente, o

un nomenclador independiente (si se requiere más control).

🔴 En la VARIANTE WEB del sistema, la Unidad de Medida es un NOMENCLADOR OBLIGATORIO y no se codifica libremente.

🔹 Rol de Ingrediente

Clasificación funcional del ingrediente dentro de la receta.

Ejemplos:

básico (componente principal del plato)

decorativo (guarnición o adorno del plato)

condimento

proceso

Sirve para:

separar cantidades por función

análisis de costos

presentación del plato

👉 El rol NO pertenece al ingrediente como entidad, se asigna dentro de la receta MASTER.

👥 Roles de Usuario
🔹 Usuario de Red (Cliente)

Persona que solo consulta el sistema.

Puede:

listar recetas

ver ficha técnica

recalcular raciones (temporal)

No puede:

crear

modificar

borrar datos

🔹 Administrador del Sistema

Usuario que mantiene el sistema.

Puede:

gestionar nomencladores

crear y editar recetas MASTER

publicar recetas

👉 Es el único que altera datos persistentes.

📄 Vistas del Sistema
🔹 Ficha Técnica (Página I)

Vista que muestra:

datos del plato

raciones base

peso por ración

ingredientes y cantidades

Enfocada a:

producción

compras

🔹 Procedimiento (Página II)

Vista que muestra:

preparación

elaboración

presentación

nutrición

Enfocada a:

cocina

capacitación

🔢 Conceptos de Raciones
🔹 Raciones Base

Cantidad de porciones para las que está formulada la receta MASTER.

👉 Es un dato fijo del MASTER.

🔹 Raciones Solicitadas

Cantidad temporal introducida por el usuario para recalcular ingredientes.

👉 No se guarda. 👉 No modifica el MASTER.

🔹 Peso por Ración

Peso estándar de una porción del plato.

Se usa para:

estandarización

costos

nutrición

👉 No interviene directamente en el cálculo de ingredientes.

📝 Términos Pendientes / en Discusión

(Se agregan aquí conceptos que surjan y aún no estén completamente definidos)

Versionado de recetas

Rendimiento / merma

Costeo

Planificación de producción

📌 Historial de Cambios

Creación inicial del glosario — Fase W2

👏 Anotado y totalmente de acuerdo contigo, José Ramón.
Y ya lo dejé por escrito en el glosario:

🔴 En la VARIANTE WEB, la Unidad de Medida es un NOMENCLADOR OBLIGATORIO.

Eso significa, en diseño del sistema:

❌ No se escribe “g”, “ml”, “unidad” a mano

✅ Se selecciona desde un catálogo controlado

✅ Ingredientes referencian una unidad por id

✅ Recetas heredan esa unidad desde el ingrediente

👉 Esto es exactamente como funcionan los sistemas serios.

🧱 ORDEN CORRECTO DE NOMENCLADORES (VARIANTE WEB)

Corrigiendo el plan según tu regla (muy bien vista):

1️⃣ Nomenclador de Unidades ✅ (VA PRIMERO)

Porque:

ingredientes dependen de unidades

2️⃣ Nomenclador de Ingredientes

Porque:

cada ingrediente usa una unidad

3️⃣ Nomenclador de Platos ✅ (ya existe)
4️⃣ Constructor de Receta MASTER

Que une:

plato + ingredientes + textos


# Nomenclador Oficial — Unidades de Medida (Variante Web)

Este documento define las únicas unidades de medida válidas en el Sistema de Recetas — Variante Web.

La Unidad de Medida es un NOMENCLADOR OBLIGATORIO.
No se permite texto libre en ingredientes ni en recetas.

## Unidades oficiales

| Código  | Nombre      |
|---------|-------------|
| g       | Gramo       |
| kg      | Kilogramo   |
| l       | Litro       |
| ml      | Mililitro   |
| lb      | Libra       |
| oz      | Onza        |
| unidad  | Unidad      |

## Reglas del sistema

- Las unidades se seleccionan desde catálogo, no se escriben.
- Ingredientes referencian la unidad por id.
- Las recetas MASTER heredan la unidad desde el ingrediente.
- El Administrador es el único que puede gestionar nomencladores.
- En fase de desarrollo, el catálogo puede ser editable para pruebas.
- En producción, el catálogo se considera fijo.

## Relación con otros nomencladores

Orden correcto en Variante Web:

1. Unidades de Medida
2. Ingredientes
3. Platos
4. Receta MASTER

Este orden garantiza integridad referencial del sistema.

### MASTER de Recetas
Módulo central donde se definen las recetas completas asociadas a un Plato.
Incluye:
- Plato
- Raciones base
- Textos descriptivos (preparación, elaboración, etc.)
- Lista de ingredientes con cantidades y unidades

A diferencia de los nomencladores, el MASTER contiene **entidades compuestas** y reglas de negocio.

### Captura (de Recetas)
Pantalla destinada a la creación de nuevas recetas en el MASTER.
URL: `/admin/recetas`

### Listado (de Recetas)
Pantalla destinada a la visualización y gestión del conjunto de recetas existentes.
URL: `/admin/recetas/listado`

### Duplicidad de Receta
Regla de negocio que establece que:
> No puede existir más de una receta para el mismo Plato en el MASTER.

Se valida contra los datos persistidos en el servidor.

### Duplicidad de Ingrediente
Regla de interfaz que establece que:
> Una receta no puede contener el mismo ingrediente más de una vez.

Se valida en cliente durante la captura de la receta.

## Actualización de Terminología — Fase XXIII

**Fecha:** 2026-02-20

### Siglas y abreviaturas estándar del sistema

- **UM** — Unidad de Medida  
  Unidad utilizada para medir ingredientes o cantidades (ej: gramos, ml, etc.).

- **Ing.** — Ingrediente  
  Elemento básico que compone una receta. Siempre asociado a una UM.

- **Pla.** — Plato  
  Representa el plato/receta base dentro del sistema (nomenclador de platos).

- **T.P.** — Tipo de Plato  
  Clasificación del plato (ej: entrada, principal, postre, etc.).

- **M.R.** — Master de Recetas  
  Registro maestro que define:
  - Plato
  - Raciones base
  - Lista de ingredientes con cantidades
  - Detalles: preparación, elaboración, presentación y nutrición.

### Convenciones de uso en la interfaz

- En mensajes del sistema, especialmente en **borrado**:
  - El **nombre del elemento** se muestra en **rojo intenso**.
  - El resto del mensaje se muestra en **verde intenso**.
  - Ejemplos:
    - `xxxxx borrado de UM correctamente.`
    - `yyyyy borrado de Ing. correctamente.`
    - `zzzzz borrado de Pla. correctamente.`
    - `aaaaa borrado de T.P. correctamente.`
    - `bbbbb borrado de M.R. correctamente.`

- En formularios de captura:
  - Los **títulos de los escaques** se muestran en color intenso y negrita.
  - Los **encabezados de tablas** y **títulos de columnas** se muestran en color intenso y negrita.
  - Texto de ayuda estándar:
    - `<enter para guardar> | ESC aborta`

### Convenciones de datos

- **SQLite** es la **fuente viva** de datos del sistema.
- **JSON** se utiliza únicamente para:
  - Backup
  - Importación / Exportación
  - Recuperación de emergencia

### Convenciones de visualización

- Todos los campos y columnas tienen **ancho fijo**.
- **Ningún texto debe desbordar** su escaque o columna:
  - Si excede el ancho, se corta con “…” (ellipsis).
- Las unidades de medida visibles en pantalla se muestran como **texto descriptivo** (ej: “gramos”), no como código interno.

---

VIII-GLOSARIO OPERATIVO DEL SISTEMA — RECETAS_APP
1. Propósito del documento

Este documento forma parte del glosario del sistema recetas_app y tiene como objetivo definir los principales términos operativos utilizados dentro del proyecto.

El glosario permite:

mantener coherencia terminológica

facilitar la comprensión del sistema

evitar ambigüedades en la documentación

establecer definiciones comunes para el desarrollo del proyecto

Este documento complementa el glosario general del sistema.

2. Receta

Una receta es la entidad principal del sistema.

Representa la descripción estructurada de una preparación culinaria.

Una receta puede contener:

nombre

descripción

categoría

raciones base

ingredientes

Cada receta puede tener múltiples ingredientes asociados.

3. Ingrediente

Un ingrediente es un componente que forma parte de una receta.

Cada ingrediente se define mediante:

nombre del ingrediente

cantidad

unidad de medida

Los ingredientes se relacionan con las recetas mediante registros en los archivos de datos del sistema.

4. Cantidad

La cantidad representa el valor numérico asociado a un ingrediente dentro de una receta.

La cantidad indica cuánto del ingrediente se utiliza.

Ejemplos de cantidades:

50
100
250
1
2

Las cantidades deben ser siempre valores positivos.

5. Unidad de medida

La unidad de medida indica la forma en que se expresa la cantidad de un ingrediente.

Ejemplos de unidades utilizadas en el sistema:

g
kg
ml
l
taza
cucharada

Las unidades forman parte de un nomenclador del sistema.

6. Raciones base

Las raciones base indican el número de porciones para las cuales está diseñada una receta.

Este valor permite calcular la proporción de ingredientes necesaria para preparar la receta.

Las raciones base deben ser siempre mayores que cero.

7. Nomenclador

Un nomenclador es una lista controlada de valores válidos dentro del sistema.

En el sistema recetas_app existen nomencladores para:

ingredientes

unidades de medida

categorías de recetas

Los nomencladores permiten mantener consistencia en los datos.

8. Persistencia de datos

La persistencia de datos es el mecanismo mediante el cual el sistema guarda la información.

En el sistema recetas_app la persistencia se realiza mediante archivos JSON.

Estos archivos almacenan información sobre:

recetas

ingredientes

unidades de medida

9. Validación

La validación es el proceso mediante el cual el sistema verifica que los datos introducidos sean correctos antes de guardarlos.

Las validaciones permiten:

evitar errores en los datos

mantener la integridad de la información

garantizar coherencia en el sistema

10. Interfaz web

La interfaz web es el componente del sistema que permite al usuario interactuar con la aplicación.

Mediante la interfaz web el usuario puede:

visualizar recetas

crear recetas

editar recetas

gestionar ingredientes

La interfaz web constituye el punto de acceso principal al sistema.
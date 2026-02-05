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
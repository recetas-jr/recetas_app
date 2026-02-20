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

## Decisión: Dónde se valida cada regla

### 1. Duplicidad de receta (por Plato)

- **Se valida en servidor (POST)** contra las recetas persistidas.
- Motivo:
  - La fuente de verdad es el almacenamiento.
  - Evita inconsistencias si hay cambios externos o concurrencia.
- Comportamiento:
  - Si existe una receta con el mismo Plato:
    - Se muestra mensaje de error.
    - Se limpia el formulario según las reglas actuales del MASTER.
    - No se guarda la receta.

### 2. Validación de Raciones

- **Se valida en cliente de forma instantánea** (al presionar ENTER en el campo).
- Motivo:
  - Mejor experiencia de usuario.
  - Evita enviar formularios inválidos al servidor.
- Regla:
  - Debe ser numérico y mayor que 0.
  - Si no es válido, no se avanza al siguiente campo.

### 3. Duplicidad de Ingrediente en una Receta

- **Se valida en cliente** al intentar agregar el ingrediente.
- Motivo:
  - Es una regla local al formulario en curso.
  - No depende del estado persistido.
- Comportamiento:
  - Si el ingrediente ya existe en la lista:
    - Se muestra mensaje.
    - Se limpia solo la línea de ingrediente (no toda la receta).

## Decisión: Flujo estable de captura en MASTER de Recetas (Web)

Se define como flujo oficial:

1. Navegación por teclado:
   - ENTER avanza entre campos.
   - En Cantidad, ENTER agrega el ingrediente a la tabla.
   - ESC limpia todo el formulario y devuelve el foco a Plato.

2. Validación de Raciones:
   - Debe ser entero > 0.
   - La validación es inmediata en frontend.
   - No se permite avanzar si el valor es inválido.

3. Duplicidad de Receta (regla MASTER):
   - No puede existir más de una receta por Plato.
   - La validación se realiza en servidor al guardar.
   - Si hay duplicado:
     - Se muestra mensaje de error.
     - Se limpia el formulario de captura según las reglas definidas.

4. Duplicidad de Ingredientes:
   - No se permite repetir un ingrediente dentro de la misma receta.
   - Si ocurre:
     - Se muestra mensaje indicando el ingrediente duplicado.
     - Se limpia solo la línea de ingrediente (no toda la receta).

5. Separación de vistas:
   - Captura: /admin/recetas
   - Listado: /admin/recetas/listado

Este flujo se considera base estable para continuar el desarrollo del sistema.

## Actualización — Flujo de Captura del Master de Recetas (alineado a estándar UI/UX)

**Fecha:** 2026-02-20  
**Estado:** Definido para implementación

### Objetivo
Definir el flujo de captura del **Master de Recetas (M.R.)** usando el mismo estándar aplicado en los nomencladores (PLATOS como referencia), garantizando:
- Consistencia visual
- Flujo por teclado (Enter / ESC)
- Validaciones claras
- No desbordes de texto
- Mensajes de borrado y acciones con formato uniforme

### Reglas generales (heredadas del estándar)

- Títulos de escaques en **color intenso** y **negrita**.
- Encabezados de tablas y títulos de columnas en **color intenso** y **negrita**.
- Todos los campos y columnas con **ancho fijo**.
- **Ningún texto debe desbordar**:
  - Si excede el ancho, se corta con “…” (ellipsis).
- Texto de ayuda visible:
  - `<enter para guardar> | ESC aborta` (en color intenso)

### Flujo de captura propuesto

#### 1) Selección de plato
- Campo: **Plato** (combo desde DB).
- Enter:
  - Avanza al siguiente campo.
- ESC:
  - Limpia formulario y vuelve al primer campo.

#### 2) Raciones base
- Campo: **Raciones base** (numérico, entero > 0).
- Validaciones:
  - Obligatorio
  - Numérico
  - Mayor que 0
- Enter:
  - Avanza a la sección de ingredientes.

#### 3) Captura de ingredientes (bloque repetible)
Por cada ingrediente:
- Campo: **Ingrediente** (combo).
- Campo: **Cantidad** (numérico > 0).
- Enter en Cantidad:
  - Agrega el ingrediente a la lista de la receta.
  - Limpia campos de ingrediente y cantidad.
  - Vuelve el foco a **Ingrediente** para seguir agregando.
- La tabla/lista de ingredientes:
  - Muestra: Nombre, Cantidad, UM (texto, no código).
  - Columnas con ancho fijo y sin desbordes.
  - Botón de borrar ingrediente con confirmación.

#### 4) Detalle de receta
Campos de texto (con ancho fijo y límite de longitud):
- Preparación
- Elaboración
- Presentación
- Nutrición

Reglas:
- Enter navega entre campos.
- En el último campo:
  - Enter guarda la receta completa.
- ESC:
  - Aborta la captura y limpia el formulario.

### Guardado

- Enter en el último campo del formulario:
  - Valida:
    - Plato seleccionado
    - Raciones base válidas
    - Al menos un ingrediente
  - Si todo es correcto:
    - Guarda en SQLite:
      - recetas_maestro
      - recetas_ingredientes
      - recetas_detalle
- Mensaje de éxito:
  - Formato corto.
  - Nombre del plato en **verde intenso** (o formato estándar de éxito del sistema).

### Borrado de recetas (listado del Master)

- Botón de borrar por receta.
- Confirmación previa.
- Borrado en orden:
  1) recetas_ingredientes
  2) recetas_detalle
  3) recetas_maestro
- Mensaje de borrado:
  - Formato estándar:
    - `xxxxxx borrado de M.R. correctamente.`
  - Donde:
    - `xxxxxx` (nombre del plato o receta) va en **rojo intenso**.
    - El resto del mensaje en **verde intenso**.

### Notas de implementación

- El Master **no debe usar JSON** en el flujo normal.
- SQLite es la **fuente viva** de datos.
- El comportamiento del teclado (Enter / ESC) debe ser idéntico al de los nomencladores.
- El diseño visual debe copiar el patrón ya validado en **PLATOS**.

---
# Reglas de Oro del Proyecto — Recetas App

## Regla de Oro: Uso de Extensiones de Archivo

- La extensión de un archivo **no cambia su contenido**,  
  solo indica a las herramientas **cómo debe ser tratado**.

- Las extensiones se usan de forma **intencional y coherente** en todo el proyecto.

### Extensiones estándar del proyecto

- `.py` → Código Python
- `.md` → Documentación del proyecto (Markdown)
- `.txt` → Texto simple, notas temporales o pruebas

### Principios asociados

- La extensión es parte del **nombre del archivo**
- Crear un archivo implica **decidir conscientemente su extensión**
- La documentación del proyecto **siempre** se guarda en archivos `.md`
- No se mezclan propósitos (por ejemplo, documentación en `.py` o `.txt`)

Estado: DEFINIDA — VIGENTE




## Regla de Oro: Definición de Receta

- En este sistema, una **receta** es una entidad completa que integra:
  - un nombre (seleccionado del nomenclador de recetas),
  - raciones base,
  - peso de la ración,
  - y **ingredientes asociados**.
- Un nombre en el nomenclador **no es una receta** por sí mismo.
- Una receta existe como registro desde su creación mínima,
  pero **solo se considera receta real cuando tiene ingredientes**.
- La receta es la unidad central del sistema y gobierna cálculos,
  visualización y uso operativo.

Estado: DEFINIDA — VIGENTE





## Regla de Oro: Unidades de Medida como Nomenclador

- Las unidades de medida **son nomencladores**.
- No se escriben como texto libre en recetas ni ingredientes.
- Toda unidad se referencia mediante un **ID**.
- Las unidades pertenecen a una **familia** (peso, volumen, unidad).
- No se permiten mezclas de unidades incompatibles por diseño.

Estado: DEFINIDA — VIGENTE





## Regla de Oro: La Receta Define las Raciones Base

- Cada receta define explícitamente su **cantidad de raciones base**.
- No se asumen valores fijos (10, 100 u otros).
- Los ingredientes se almacenan **para la receta base**, no por ración.
- Los cálculos posteriores se realizan a partir de esa base.
- La receta es la única fuente de verdad sobre sus raciones.

Estado: DEFINIDA — VIGENTE




# ARCHIVOS HISTÓRICOS DEL PROYECTO — Recetas App

Este documento describe la estructura, propósito y uso del conjunto de carpetas
y archivos que conforman los **ARCHIVOS HISTÓRICOS** del proyecto.

Los ARCHIVOS HISTÓRICOS representan la memoria, las decisiones y la evolución
del sistema. No contienen código ejecutable.

---

## Estructura general

docs/
├─ decisiones/
├─ modulos/
├─ pendientes/
└─ notas/

yaml
Copiar código

---

## 📁 docs/decisiones/
### DECISIONES CERRADAS DEL PROYECTO

Aquí se documentan las **reglas de oro** y decisiones que:
- afectan al modelo de datos
- afectan al comportamiento del sistema
- no se discuten nuevamente

Ejemplos:
- Reglas de Oro del Proyecto
- Unidades de medida como nomenclador
- Ingredientes en minúscula
- básico / deco
- Qué define una receta válida

Pregunta que responde esta carpeta:
> ¿Por qué el sistema es así?

---

## 📁 docs/modulos/
### DESCRIPCIÓN FUNCIONAL DE LOS MÓDULOS

Aquí se documenta:
- qué hace cada módulo
- cuál es su responsabilidad
- qué NO es su responsabilidad

Ejemplos:
- RECETAS.md
- NOMENCLADORES.md
- PERSISTENCIA.md

Pregunta que responde esta carpeta:
> ¿Para qué sirve cada parte del sistema?

---

## 📁 docs/pendientes/
### DECISIONES TOMADAS, NO IMPLEMENTADAS

Aquí se documentan funcionalidades que:
- ya fueron pensadas
- ya fueron decididas
- pero se implementarán más adelante

Ejemplos:
- Importación de datos (CSV / copia y pega)
- Conversión automática de unidades
- Costos y mermas
- Versionado de recetas

Pregunta que responde esta carpeta:
> ¿Qué sabemos que falta, pero decidimos dejar para después?

---

## 📁 docs/notas/
### IDEAS, APUNTES Y BORRADORES

Aquí se guardan:
- ideas en proceso
- dudas abiertas
- esquemas preliminares
- reflexiones que aún no están cerradas

Nada en esta carpeta es definitivo.

Pregunta que responde esta carpeta:
> ¿Qué estamos pensando, pero aún no decidimos?

---

## Regla de uso

- Todo documento debe guardarse **en una sola carpeta**, según su naturaleza.
- Si un contenido pasa de idea a decisión, se mueve de `notas` a `decisiones`.
- Los ARCHIVOS HISTÓRICOS deben mantenerse claros, ordenados y actualizados.





## Regla de Oro: Estados de la Receta

- Una receta puede encontrarse en distintos **estados lógicos** durante su ciclo de vida.
- Los estados definidos son:

### Receta en construcción
- La receta tiene estructura mínima (nombre, raciones base, peso de ración).
- Aún **no tiene ingredientes**.
- No puede usarse para cálculos ni como receta operativa.

### Receta válida
- La receta tiene **al menos un ingrediente asociado**.
- Puede utilizarse para cálculos, visualización completa y uso operativo.
- Puede ser modificada sin perder su identidad.

- El estado de la receta **no es un dato decorativo**, gobierna el comportamiento del sistema.
- El paso de “en construcción” a “válida” ocurre automáticamente al agregar ingredientes.

Estado: DEFINIDA — VIGENTE





Regla clave (confirmada)

✔ Un ingrediente puede aparecer dos veces en una receta:

una como básico

otra como deco

❌ No puede repetirse con el mismo tipo de uso

La unicidad es:

(receta, ingrediente, tipo_uso)

🔁 Ajuste final al flujo “Agregar ingredientes”

El paso queda así:

Tipo de uso del ingrediente:
1. básico   (por defecto)
2. deco


ENTER → básico

Selección explícita → deco

Nada más cambia.
Todo lo demás sigue igual.

🔒 Esto queda cerrado

✔ Terminología fijada
✔ Valor por defecto definido
✔ Coherente con lo ya hablado
✔ Sin ambigüedades futuras

## Regla de Oro: Roles de Ingredientes (básico / deco)

- Todo ingrediente asociado a una receta debe tener un **rol de uso**.
- Los únicos roles válidos definidos en el sistema son:
  - **básico**
  - **deco**

### Rol básico
- Es el rol **por defecto** de todo ingrediente.
- El ingrediente forma parte de la elaboración del plato.
- El ingrediente participa en los cálculos (raciones, costos, etc.).
- Si el usuario no indica un rol explícitamente, el sistema asigna **básico**.

### Rol deco
- El ingrediente se utiliza para **decoración o presentación**.
- Su uso es explícito; nunca se asigna por defecto.
- Un ingrediente con rol deco no altera la definición básica del plato.

### Reglas de coexistencia
- Un mismo ingrediente puede aparecer más de una vez en una receta
  **siempre que tenga roles distintos**.
- No se permite repetir un ingrediente con el **mismo rol** dentro de una receta.
- La unicidad de un ingrediente en una receta está definida por la combinación:
  (receta, ingrediente, rol).

Estado: DEFINIDA — VIGENTE

VI-REGLAS DE BLINDAJE DEL MAPA ARQUITECTONICO — RECETAS_APP
1. Propósito del documento

Este documento establece las reglas de protección del mapa arquitectónico del sistema recetas_app.

Su objetivo es garantizar que la arquitectura del sistema se mantenga estable y coherente a lo largo del tiempo.

El blindaje arquitectónico permite:

evitar modificaciones desordenadas

preservar la estructura del sistema

mantener coherencia en el desarrollo

2. Importancia del blindaje arquitectónico

El mapa arquitectónico define la estructura general del sistema.

Modificar esta estructura sin control puede provocar:

pérdida de coherencia del sistema

errores en el funcionamiento

dificultades en el mantenimiento

Por esta razón, el mapa arquitectónico debe considerarse un documento estructural del proyecto.

3. Principios de protección arquitectónica

La arquitectura del sistema debe regirse por los siguientes principios.

Estabilidad estructural

La estructura general del sistema no debe modificarse sin una justificación clara.

Coherencia funcional

Las modificaciones deben respetar las funciones y relaciones existentes.

Documentación obligatoria

Cualquier cambio relevante en la arquitectura debe quedar documentado.

4. Reglas para modificaciones arquitectónicas

Cuando sea necesario modificar la arquitectura del sistema se deben seguir estas reglas.

Analizar el impacto del cambio.

Verificar las dependencias entre componentes.

Actualizar la documentación arquitectónica.

Registrar el cambio en la bitácora del proyecto.

Estas reglas permiten mantener control sobre la evolución del sistema.

5. Cambios permitidos

Se consideran modificaciones aceptables aquellas que:

mejoran la organización del sistema

corrigen inconsistencias estructurales

optimizan el funcionamiento del sistema

Siempre que estos cambios se encuentren debidamente documentados.

6. Cambios que requieren revisión

Las siguientes modificaciones deben evaluarse cuidadosamente.

cambios en la estructura de datos

cambios en el flujo general del sistema

eliminación de componentes del sistema

cambios en las relaciones entre módulos

Estos cambios pueden afectar directamente la estabilidad del sistema.

7. Registro de cambios arquitectónicos

Toda modificación arquitectónica debe registrarse en la documentación del proyecto.

El registro debe incluir:

descripción del cambio

motivo del cambio

impacto en el sistema

fecha de la modificación

Esto permite mantener un historial claro de la evolución del sistema.

8. Responsabilidad del mantenimiento arquitectónico

El mantenimiento de la arquitectura del sistema es responsabilidad del desarrollo del proyecto.

La documentación arquitectónica debe mantenerse actualizada para reflejar el estado real del sistema.

Esto garantiza que el proyecto pueda evolucionar de manera controlada.

docs/decisiones/REGLAS_DE_ORO_DEL_PROYECTO.md

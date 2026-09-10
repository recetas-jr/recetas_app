# AEFi — ALGORITMO DE ESTADO FUNCIONAL DE LA FILA

## Documento Maestro

**Proyecto:** recetas_app  
**Módulo:** Editor de recetas Master  
**Ámbito:** RECETA NUEVA + EDICIÓN NUEVA  
**Versión:** 0.1 — Diseño inicial  
**Fecha:** 8 de septiembre de 2026

---

## 1. AUTORIDAD DEL DOCUMENTO

Este documento define el comportamiento funcional del **AEFi — Algoritmo de Estado Funcional de la Fila**.

A partir de su aprobación, cuando exista una duda sobre el estado de una fila del editor, se consulta primero este documento.

El código deberá obedecer al AEFi.

El código no deberá decidir por su cuenta un comportamiento contrario al AEFi para resolver un caso particular.

**Regla:**

```text
DUDA
  ↓
CONSULTAR AEFi
  ↓
DETERMINAR ESTADO
  ↓
APLICAR LO QUE DEFINE AEFi
```

---

## 2. OBJETIVO

AEFi determina, para cada fila de ingrediente:

1. cuál es su estado funcional;
2. cuál es su Unidad de Medida canónica;
3. cuál es su Unidad de Captura;
4. si la Unidad de Captura es canónica o equivalente;
5. cuál es la etapa funcional actual;
6. cuál debe ser el estado visual;
7. cuál es el siguiente campo al que debe pasar el operador;
8. qué debe conservarse al editar una receta existente;
9. qué debe reiniciarse cuando realmente cambia la Unidad de Captura.

AEFi controla el **estado de la fila**. No administra la base de datos y no crea nuevos datos persistentes.

---

## 3. PRINCIPIO FUNDAMENTAL

La información almacenada y el estado funcional no son la misma cosa.

```text
DATOS DE LA FILA
      ↓
AEFi interpreta los datos
      ↓
ESTADO FUNCIONAL
      ↓
PRESENTACIÓN VISUAL
      ↓
SIGUIENTE ACCIÓN
```

La interfaz no debe deducir el estado a partir del color que ya tenga la pantalla.

Primero se determina el estado lógico. Después se representa visualmente.

---

## 4. DATOS QUE AEFi RECIBE

La fila utiliza información que ya existe en el modelo actual:

- `ingredient_id`
- Unidad de Medida canónica del ingrediente
- `unidad_codigo_presentacion` / Unidad de Captura persistida
- `expresion_c_id`
- `expresion_c_texto`
- `cantidad_captura`
- `expresion_d_id`
- `expresion_d_texto`
- `deco_captura`
- cantidad canónica
- rol canónico

**COCINA no es un dato independiente almacenado:** es un valor calculado.

AEFi no requiere nuevas columnas de base de datos para funcionar.

---

## 5. DEFINICIONES

### 5.1 Ingrediente

Es la entidad que determina el contexto de la fila y su Unidad de Medida canónica.

### 5.2 UM canónica

Es la Unidad de Medida de referencia del ingrediente.

### 5.3 UM de Captura

Es la Unidad con la que el operador está expresando la fila en ese momento.

### 5.4 UM equivalente

Es una Unidad de Captura diferente de la UM canónica.

### 5.5 Cambio real de UM

Existe únicamente cuando:

```text
UM anterior ≠ UM seleccionada
```

Ese cambio inicia una nueva definición culinaria de la fila.

### 5.6 Misma UM + ENTER

Cuando:

```text
UM anterior = UM seleccionada
```

no existe cambio real de UM.

Se conserva la definición culinaria existente y sólo se determina la transición siguiente.

---

## 6. ESTADOS FUNCIONALES

AEFi reconoce las siguientes etapas funcionales de la fila:

```text
E0  INGREDIENTE
E1  UM
E2  EXPRESION-C
E3  CANTIDAD
E4  EXPRESION-D
E5  DECO
E6  COCINA
```

La numeración identifica la etapa; la condición canónica/equivalente determina el recorrido.

---

## 7. RUTA DE UM CANÓNICA

Cuando:

```text
UM de Captura = UM canónica
```

la ruta funcional es:

```text
INGREDIENTE
   ↓ ENTER
UM CANÓNICA
   ↓ ENTER
CANTIDAD
   ↓ ENTER
DECO
   ↓ ENTER
COCINA
```

### Estado visual esperado

```text
NORMAL
```

No debe aparecer el estado azul por el simple hecho de entrar, regresar o volver a seleccionar la UM canónica.

---

## 8. RUTA DE UM EQUIVALENTE

Cuando:

```text
UM de Captura ≠ UM canónica
```

la ruta funcional es:

```text
INGREDIENTE
   ↓ ENTER
UM EQUIVALENTE
   ↓ ENTER
EXPRESION-C
   ↓ ENTER
CANTIDAD
   ↓ ENTER
EXPRESION-D
   ↓ ENTER
DECO
   ↓ ENTER
COCINA
```

### Estado visual esperado

```text
AZUL → EXPRESION-C / CANTIDAD
NARANJA → EXPRESION-D / DECO
```

El color representa una etapa funcional; no es la fuente del estado.

---

## 9. REGLA DE CAMBIO REAL DE UM

Si:

```text
UM anterior ≠ UM seleccionada
```

AEFi ordena una nueva definición culinaria.

Se reinician los valores culinarios internos asociados a la nueva representación:

```text
CANTIDAD
DECO
COCINA
valores canónicos derivados de la representación anterior
```

La receta no cambia de identidad por este hecho; cambia su representación culinaria.

---

## 10. REGLA DE MISMA UM + ENTER

Si:

```text
UM anterior = UM seleccionada
```

AEFi no reinicia los valores.

Después determina:

```text
¿UM es canónica?
   ├─ SÍ → CANTIDAD
   └─ NO → EXPRESION-C
```

Esta regla es especialmente importante en la edición de recetas existentes.

---

## 11. ESTADO DE UNA RECETA EXISTENTE

Al abrir una receta existente, AEFi debe reconstruir el estado a partir de los datos almacenados.

No basta con mostrar los valores guardados.

Debe reconstruirse también el estado funcional correspondiente.

Ejemplo:

```text
UM captura = taza
UM canónica = gramos
EXP-C = 1/2
CANTIDAD = 1/2
DECO = 1/4
```

produce un estado compatible con:

```text
UM EQUIVALENTE
      ↓
EXPRESION-C
      ↓
CANTIDAD
```

y, si esa es la etapa restaurada, debe representarse visualmente con el estado azul correspondiente.

---

## 12. ESTADO DE UNA FILA NUEVA

Al crear una fila nueva, AEFi debe comenzar sin arrastrar estados visuales de la fila anterior.

Secuencia:

```text
CREAR FILA
   ↓
LIMPIAR ESTADOS VISUALES
   ↓
INGREDIENTE
   ↓
IDENTIFICAR UM CANÓNICA
   ↓
UM DE CAPTURA INICIAL
   ↓
AEFi determina CANÓNICA / EQUIVALENTE
```

La fila nueva nunca debe heredar accidentalmente el azul o naranja de otra fila.

---

## 13. REGLA DE INICIALIZACIÓN DE UM CANÓNICA

La UM canónica debe quedar determinada **al establecer el contexto del ingrediente**.

Debe existir una operación equivalente conceptualmente a:

```text
INGREDIENTE seleccionado
        ↓
obtener UM canónica del ingrediente
        ↓
guardar unidadCanonica de la fila
```

La evaluación posterior de UM utiliza ese dato.

AEFi no debe depender de que el operador haya causado previamente otra transición para conocer la UM canónica.

---

## 14. REGLA DE PRESENTACIÓN

El operador debe ver exactamente la expresión que seleccionó o escribió.

Ejemplo:

```text
1 3/4
```

no puede sustituirse visualmente por:

```text
1.75
```

Las conversiones numéricas pertenecen al estado interno y no deben alterar la presentación al operador.

---

## 15. CANTIDAD

Reglas:

```text
cantidad <= 0
      ↓
DETENER
      ↓
mensaje de validación
      ↓
FOCO EN CANTIDAD
```

La validación de cantidad pertenece al comportamiento del editor, pero AEFi debe respetar el hecho de que una cantidad inválida no permite avanzar normalmente.

---

## 16. DECO

DECO conserva la captura visible del operador.

La captura debe sincronizarse con el dato de persistencia correspondiente.

AEFi no modifica el principio de que el operador debe conservar su representación de captura.

---

## 17. COCINA

COCINA se calcula a partir del estado culinario de la fila.

Conceptualmente:

```text
COCINA = max(0, CANTIDAD - DECO)
```

COCINA no constituye una Unidad de Captura independiente.

CANTIDAD, DECO y COCINA comparten la misma Unidad de Captura de la fila.

---

## 18. ESTADO VISUAL

AEFi nunca debe usar la lógica:

```text
"está azul, por tanto es equivalente"
```

La lógica correcta es:

```text
UM captura
     ↓
comparar con UM canónica
     ↓
determinar estado
     ↓
determinar etapa
     ↓
aplicar representación visual
```

### Mapa visual

```text
CANÓNICA
   ↓
NORMAL

EQUIVALENTE + EXPRESION-C/CANTIDAD
   ↓
AZUL

EQUIVALENTE + EXPRESION-D/DECO
   ↓
NARANJA

FILA NO ACTIVA
   ↓
NEUTRAL

### NEUTRAL

NEUTRAL → fila no activa; sin atención visual pendiente.
```

---

## 19. REGLA DE RESTAURACIÓN

Cuando una receta existente contiene una expresión, una cantidad o un DECO ya almacenados, AEFi debe distinguir entre:

```text
DATO RESTAURADO
```

y:

```text
TRANSICIÓN PRODUCIDA POR EL OPERADOR
```

Restaurar un dato no equivale a que el operador haya cambiado la UM.

Por tanto, la restauración no debe ejecutar accidentalmente las reglas de cambio real de UM.

---

## 20. INVARIANTES DE AEFi

Las siguientes condiciones deben permanecer siempre verdaderas:

### I1 — Una fila tiene un solo contexto de ingrediente

```text
INGREDIENTE
   ↓
UM canónica
```

### I2 — La UM de Captura pertenece a la fila

Es compartida por:

```text
CANTIDAD
DECO
COCINA
```

### I3 — La UM canónica no cambia cuando el operador sólo cambia la representación

### I4 — Un cambio real de UM reinicia la definición culinaria

### I5 — Misma UM + ENTER no reinicia la definición

### I6 — El azul sólo representa un estado equivalente en la etapa correspondiente

### I7 — El naranja sólo representa la etapa EXPRESION-D / DECO

### I8 — Los valores visibles del operador se conservan como presentación

### I9 — COCINA es calculada

### I10 — La base de datos no necesita nuevos campos para AEFi

---

## 21. PRUEBAS MÍNIMAS OBLIGATORIAS

AEFi deberá considerarse correcto únicamente después de comprobar como mínimo:

### P1 — Fila nueva + UM canónica

```text
INGREDIENTE
→ UM canónica
→ ENTER
→ CANTIDAD
```

Resultado visual: **NORMAL**.

### P2 — Fila nueva + UM equivalente

```text
INGREDIENTE
→ UM equivalente
→ ENTER
→ EXPRESION-C
```

Resultado visual: **AZUL**.

### P3 — Receta existente + UM canónica

Abrir y continuar sin modificar la UM.

Resultado: conservar comportamiento canónico.

### P4 — Receta existente + UM equivalente

Abrir y continuar sin modificar la UM.

Resultado: reconstruir el estado equivalente correcto.

### P5 — Cambiar realmente de UM

```text
UM A
→ UM B
```

Resultado: nueva definición culinaria y reinicio de los valores internos correspondientes.

### P6 — Misma UM + ENTER

Resultado: no reiniciar valores; continuar según canónica/equivalente.

---

## 22. REGLA DE TRABAJO DEL PROYECTO

AEFi no se implementa mediante cambios masivos.

Se mantiene:

```text
AUDITORÍA
   ↓
DISEÑO AEFi
   ↓
1 CAMBIO
   ↓
1 PRUEBA
   ↓
RESULTADO
   ↓
AUDITORÍA
   ↓
SIGUIENTE CAMBIO
```

No se refactoriza sin necesidad.

No se toca backend mientras el problema pueda resolverse en el estado funcional del editor.

No se modifica DECO salvo que una prueba demuestre un problema nuevo.

No se modifica el bloque que representa el estado azul para ocultar un error de determinación del estado.

---

## 23. RECETA NUEVA Y EDICIÓN NUEVA

La relación arquitectónica queda fijada así:

```text
RECETA NUEVA
     ↓
comportamiento funcional estabilizado
     ↓
       AEFi
     ↑
EDICIÓN NUEVA
     ↓
receta existente + datos almacenados
```

Ambos flujos deben terminar obedeciendo al mismo algoritmo de estado.

---

## 24. NO FORMA PARTE DE AEFi

AEFi no administra:

- tablas de la base de datos;
- catálogo de ingredientes;
- catálogo de unidades;
- equivalencias como información administrativa;
- persistencia de recetas;
- Motor de Conversión como servicio.

AEFi interpreta y gobierna el **estado funcional de la fila del editor**.

---

## 25. REGLA DE ORO

```text
AEFi NO PINTA PARA DESCUBRIR EL ESTADO.

AEFi DETERMINA EL ESTADO
        ↓
Y DESPUÉS
        ↓
LA INTERFAZ LO REPRESENTA.
```

---

## 26. ESTADO DEL DOCUMENTO

Este documento constituye el **diseño inicial del algoritmo**.

Antes de convertir AEFi en código, cada regla deberá comprobarse contra:

1. el comportamiento probado de RECETA NUEVA;
2. el comportamiento observado en EDICIÓN NUEVA;
3. las pruebas reales del usuario;
4. las reglas funcionales ya aceptadas del proyecto.

Las reglas nuevas que contradigan una regla aceptada deberán quedar expresamente identificadas y aprobadas antes de modificar código.

---

# FIN DEL DOCUMENTO MAESTRO AEFi

## 27. ALGORITMO BASE AEFi

AEFi debe ser determinista: para una misma combinación de datos de fila y contexto de interacción debe producir el mismo estado.

### 27.1 Entrada mínima

```text
filaActiva
ingrediente
umCanonica
umCapturaActual
umCapturaAnterior
expresionC
cantidad
expresionD
deco
etapaActual
```

No todas las entradas deben estar presentes en una fila nueva; cuando falten, AEFi utiliza el estado inicial definido para esa etapa.

### 27.2 Clasificación de UM

```text
SI umCapturaActual = umCanonica
    tipoUM = CANONICA
SI umCapturaActual ≠ umCanonica
    tipoUM = EQUIVALENTE
```

Esta clasificación es lógica. Nunca se obtiene consultando una clase CSS.

### 27.3.1 Regla de independencia respecto al evento

El evento de interfaz NO determina si existe un cambio real de UM.

AEFi determina el cambio real exclusivamente mediante:

    umCapturaAnterior ≠ umCapturaActual

Por tanto:

    UM anterior = UM actual
        → NO existe cambio real de UM

    UM anterior ≠ UM actual
        → SÍ existe cambio real de UM

Esta regla es válida independientemente de la acción de interfaz que haya producido la evaluación.

El evento informa el contexto de interacción.

La comparación entre UM anterior y UM actual determina el cambio real.

### 27.4 Determinación de etapa

Para una UM canónica:

```text
UM → CANTIDAD → DECO → COCINA
```

Para una UM equivalente:

```text
UM → EXPRESION-C → CANTIDAD → EXPRESION-D → DECO → COCINA
```

La etapa no se determina por el color existente. Se determina por el estado lógico y por la última transición válida.

### 27.5 Determinación visual

```text

SI fila no está activa
    estadoVisual = NEUTRAL
    devolver estadoVisual

SI tipoUM = CANONICA
    estadoVisual = NORMAL

SI tipoUM = EQUIVALENTE
    SI etapa = EXPRESION-C o CANTIDAD
        estadoVisual = AZUL
    SI etapa = EXPRESION-D o DECO
        estadoVisual = NARANJA
```

La visualización es una consecuencia del estado.

### 27.6 Determinación del siguiente campo

```text
CANONICA + ENTER en UM
    → CANTIDAD

EQUIVALENTE + ENTER en UM
    → EXPRESION-C

EQUIVALENTE + ENTER en EXPRESION-C
    → CANTIDAD

EQUIVALENTE + ENTER en CANTIDAD
    → EXPRESION-D

EQUIVALENTE + ENTER en EXPRESION-D
    → DECO

CANONICA + ENTER en CANTIDAD
    → DECO

ENTER en DECO válido
    → COCINA
```

### 27.7 Regla de conservación

Si la UM no cambia realmente:

```text
umAnterior = umActual
```

AEFi no reinicia la definición culinaria existente.

Si la UM cambia realmente:

```text
umAnterior ≠ umActual
```

AEFi inicia una nueva definición culinaria y permite el reinicio definido por la ruta correspondiente.

### 27.8 Regla de restauración

Al abrir una receta existente:

```text
datos persistidos
      ↓
construir estado lógico
      ↓
determinar etapa
      ↓
aplicar estado visual
      ↓
preparar siguiente transición
```

La restauración nunca debe consistir únicamente en copiar valores a controles visuales.

### 27.9 Regla de fila nueva

Al crear una fila nueva:

```text
fila limpia
   ↓
ingrediente seleccionado
   ↓
obtener UM canónica
   ↓
establecer UM de captura inicial
   ↓
clasificar UM
   ↓
estado inicial
```

La fila nueva no hereda la etapa ni el color de la fila anterior.

---

## 28. PSEUDOCÓDIGO MAESTRO

```text
AEFi(fila, evento):

    leer datos de fila

    obtener umCanonica
    obtener umCapturaActual
    obtener umAnterior

    clasificar UM

    SI evento implica cambio de UM:
        determinar si existe cambio real

        SI cambio real:
            iniciar nueva definición culinaria
            reiniciar magnitudes según regla

    determinar etapa funcional

    determinar siguiente transición

    determinar si la fila está activa

    SI fila no está activa:
        estadoVisual = NEUTRAL
    SI fila está activa:
        determinar estado visual según tipoUM y etapa

    devolver:
        estado
        tipoUM
        etapa
        siguienteCampo
        estadoVisual
        reinicioRequerido
```

AEFi devuelve una decisión funcional. La interfaz se limita a ejecutarla.

---

## 29. PRIMERA REGLA DE IMPLEMENTACIÓN

Antes de sustituir código existente, debe existir en el editor una implementación que pueda responder de forma verificable, como mínimo, a estos cuatro casos:

```text
CASO 1
UM canónica en fila nueva
→ NORMAL
→ CANTIDAD

CASO 2
UM equivalente en fila nueva
→ AZUL
→ EXPRESION-C

CASO 3
UM canónica en fila existente
→ NORMAL
→ CANTIDAD

CASO 4
UM equivalente en fila existente
→ estado correspondiente a la etapa restaurada
```

Estos cuatro casos constituyen la primera batería de aceptación del AEFi.

---

## 30. ESTADO DE ESTA FASE

**AEFi v0.2 — Algoritmo funcional definido.**

En esta fase no se sustituye todavía el código del editor.

El siguiente trabajo será auditar qué información disponible en `admin_recetas_editar_nuevo.html` permite alimentar AEFi sin crear nuevas columnas ni modificar la base de datos.

Después de esa auditoría se emitirá el primer ORDENO de implementación, respetando:

```text
1 CAMBIO
   ↓
1 PRUEBA
   ↓
RESULTADO
   ↓
SIGUIENTE CAMBIO
```

# LA GUINDA DEL PASTEL

## Documento maestro del algoritmo de captura y re-edición de ingredientes

**Proyecto:** `recetas_app`  
**Módulo:** Editor de recetas Master  
**Propósito:** conservar en un único documento las reglas funcionales acordadas para la captura, cálculo canónico y re-edición de los ingredientes de una receta.

---

# 1. PROPÓSITO

Este documento es la referencia maestra para entender **qué debe hacer el sistema**, **por qué se tomó cada decisión** y **cómo debe comportarse la captura y la re-edición de una fila de ingrediente**.

Cuando exista una duda futura sobre el comportamiento del editor, este documento debe consultarse antes de modificar código.

La regla general es:

> **La captura del operador y el estado canónico son dos cosas distintas y deben conservarse de forma independiente.**

---

# 2. PRINCIPIO FUNDAMENTAL

## 2.1. CAPTURA

La captura representa exactamente lo que el operador seleccionó o escribió.

Debe conservarse la representación utilizada por el operador.

Ejemplo:

```text
CANTIDAD = "1/2"
DECO     = "1/4"
```

No debe transformarse visualmente en:

```text
0.5
0.25
```

aunque internamente existan esos valores numéricos.

## 2.2. CANÓNICO

El estado canónico representa los valores que el motor necesita para realizar cálculos y conversiones.

Ejemplo:

```text
CANTIDAD CANÓNICA = 0.5
DECO CANÓNICO     = 0.25
```

La información canónica y la información de captura coexisten.

---

# 3. ESTADO DE UNA FILA

Cada fila de ingrediente debe entenderse como un estado compuesto por tres capas persistentes/lógicas y una capa temporal de interfaz.

## 3.1. Identidad

```text
ingrediente_id
```

Identifica el ingrediente de la fila.

## 3.2. Captura

```text
unidad_captura

expresion_c_id
expresion_c_texto
cantidad_captura

expresion_d_id
expresion_d_texto
deco_captura
```

### Significado

- `unidad_captura`: UM seleccionada por el operador.
- `expresion_c_id`: identificación de EXPRESION-C, cuando existe.
- `expresion_c_texto`: texto de EXPRESION-C.
- `cantidad_captura`: texto exacto mostrado/capturado en CANTIDAD.
- `expresion_d_id`: identificación de EXPRESION-D, cuando existe.
- `expresion_d_texto`: texto de EXPRESION-D.
- `deco_captura`: texto exacto mostrado/capturado en DECO.

## 3.3. Estado canónico

```text
cantidad_canonica
deco_canonico
```

La UM canónica **no se duplica en `recetas_ingredientes`**.

Se obtiene desde:

```text
ingrediente_id
    ↓
ingredientes.unidad_id
    ↓
unidades.id
    ↓
unidades.codigo
```

Por tanto, la UM canónica del ingrediente tiene una única fuente de verdad.

## 3.4. Estado temporal de interfaz

Existe información que sirve únicamente para controlar la interfaz:

```text
etapa_actual
control_activo
atención visual
```

Estos datos no forman parte del estado persistente de la receta.

---

# 4. MÁQUINA DE ESTADOS

La secuencia funcional acordada es:

```text
INGREDIENTE
    ↓
UM
    ↓
EXPRESION-C
    ↓
CANTIDAD
    ↓
EXPRESION-D
    ↓
DECO
    ↓
COCINA
```

La ausencia de una expresión es un camino válido dentro de la misma máquina de estados.

No se crea una máquina distinta para el caso sin expresión.

---

# 5. REGLA GENERAL DE LA INTERFAZ

La interfaz no debe intentar deducir el estado de negocio a partir de colores, foco, valores visuales o elementos DOM dispersos.

El estado funcional de una fila debe ser coherente por sí mismo.

La interfaz debe reflejar ese estado.

La lógica conceptual es:

```text
acción del operador
        ↓
estado de la fila
        ↓
nuevo estado
        ↓
interfaz refleja el nuevo estado
```

---

# 6. TRANSICIÓN INGREDIENTE → UM

## Estado inicial

```text
INGREDIENTE
```

Cuando el operador pulsa ENTER:

1. Se valida que exista un ingrediente.
2. Se obtiene la UM canónica de ese ingrediente.
3. Se obtienen las UM de captura disponibles para ese ingrediente.
4. Se establece la UM de captura inicial.
5. Se pasa al estado UM.
6. El foco pasa al selector UM.

### Regla importante

Seleccionar el ingrediente **no calcula todavía CANTIDAD ni DECO**.

En ese momento:

```text
CAPTURA
ingrediente = seleccionado
UM captura  = UM canónica inicial
CANTIDAD    = todavía sin capturar
DECO        = todavía sin capturar
```

---

# 7. TRANSICIÓN UM → EXPRESION-C

Cuando el operador está en UM y pulsa ENTER:

1. Se toma la UM seleccionada.
2. Se compara con la UM canónica del ingrediente.
3. Se guarda la UM de captura.
4. Se limpia cualquier estado anterior de CANTIDAD, DECO y expresiones de esa fila que corresponda reiniciar.
5. Se consultan las expresiones disponibles para la UM seleccionada.
6. Se pasa a EXPRESION-C.
7. El foco pasa al selector EXPRESION-C.

### Regla importante

La selección de UM **no calcula todavía CANTIDAD**.

Primero se determina si el operador desea utilizar una expresión.

Ejemplo:

```text
CUP
 ↓
EXPRESION-C
 ↓
1/2
```

o:

```text
G
 ↓
EXPRESION-C
 ↓
ninguna
```

---

# 8. TRANSICIÓN EXPRESION-C → CANTIDAD

Hay dos caminos válidos.

## 8.1. Con expresión

Ejemplo:

```text
UM            = CUP
EXPRESION-C   = 1/2
```

Al pulsar ENTER:

1. Se guarda `expresion_c_id`.
2. Se guarda `expresion_c_texto = "1/2"`.
3. Se obtiene el factor de la expresión.
4. CANTIDAD muestra exactamente `"1/2"`.
5. El valor numérico se conserva internamente para el cálculo.
6. Se pasa a CANTIDAD.
7. El foco pasa a CANTIDAD.

### Regla

La pantalla debe seguir mostrando:

```text
1/2
```

y no:

```text
0.5
```

El valor numérico es interno.

## 8.2. Sin expresión

Si el operador no selecciona expresión:

```text
expresion_c_id    = NULL
expresion_c_texto = NULL
```

CANTIDAD queda disponible para captura manual.

---

# 9. TRANSICIÓN CANTIDAD → EXPRESION-D

Cuando el operador está en CANTIDAD y pulsa ENTER:

1. Se valida CANTIDAD.
2. Se conserva literalmente el texto capturado en `cantidad_captura`.
3. Se obtiene su valor numérico.
4. Se calcula `cantidad_canonica` usando:
   - ingrediente;
   - unidad de captura;
   - valor numérico capturado.
5. La visualización no se sustituye por el valor canónico.
6. Se prepara EXPRESION-D.
7. Se pasa a EXPRESION-D.
8. El foco pasa a EXPRESION-D.

### Regla fundamental

El cálculo canónico se produce al cerrar CANTIDAD.

EXPRESION-D **no modifica CANTIDAD**.

La cadena es:

```text
EXPRESION-C → CANTIDAD → CANTIDAD CANÓNICA
```

---

# 10. TRANSICIÓN EXPRESION-D → DECO

Hay dos caminos válidos.

## 10.1. Con expresión

Ejemplo:

```text
EXPRESION-D = 1/4
```

Al pulsar ENTER:

1. Se guarda `expresion_d_id`.
2. Se guarda `expresion_d_texto = "1/4"`.
3. Se obtiene el factor.
4. DECO muestra exactamente `"1/4"`.
5. El valor numérico se conserva internamente.
6. Se calcula `deco_canonico`.
7. Se pasa a DECO.

### Regla

EXPRESION-D afecta exclusivamente a DECO.

No modifica:

```text
EXPRESION-C
CANTIDAD
cantidad_canonica
```

## 10.2. Sin expresión

Si el operador no selecciona expresión:

```text
expresion_d_id    = NULL
expresion_d_texto = NULL
```

DECO queda disponible para captura manual.

---

# 11. TRANSICIÓN DECO → COCINA

Cuando el operador está en DECO y pulsa ENTER:

1. Se valida DECO.
2. Se conserva literalmente el texto en `deco_captura`.
3. Se obtiene el valor numérico.
4. Se calcula `deco_canonico`.
5. Se conserva la expresión D, si existió.
6. Si no hubo expresión D:
   - `expresion_d_id = NULL`
   - `expresion_d_texto = NULL`
7. La fila queda completa.
8. Se pasa a COCINA.
9. El foco pasa a COCINA.

Al entrar en COCINA, la fila debe tener completos sus datos de captura y sus datos canónicos.

---

# 12. DOS CADENAS INDEPENDIENTES

La máquina debe mantener separadas estas dos cadenas:

```text
EXPRESION-C
     ↓
CANTIDAD
     ↓
CANTIDAD CANÓNICA
```

y:

```text
EXPRESION-D
     ↓
DECO
     ↓
DECO CANÓNICO
```

Nunca debe utilizarse EXPRESION-D para modificar CANTIDAD.

Nunca debe utilizarse EXPRESION-C para modificar DECO.

---

# 13. EJEMPLO COMPLETO

Supongamos:

```text
Ingrediente = Harina
UM          = CUP
EXPRESION-C = 1/2
CANTIDAD    = 1/2
EXPRESION-D = 1/4
DECO        = 1/4
```

### Captura

```text
unidad_captura    = CUP

expresion_c_id    = 2
expresion_c_texto = "1/2"
cantidad_captura  = "1/2"

expresion_d_id    = 1
expresion_d_texto = "1/4"
deco_captura      = "1/4"
```

### Canónico

```text
cantidad_canonica = 0.5
deco_canonico     = 0.25
```

La pantalla de re-edición debe poder reconstruir:

```text
UM            CUP
EXPRESION-C   1/2
CANTIDAD      1/2
EXPRESION-D   1/4
DECO          1/4
```

Sin deducir nada desde:

```text
0.5
0.25
```

---

# 14. CASO SIN EXPRESIONES

Ejemplo:

```text
UM       = G
CANTIDAD = 250
DECO     = 10
```

Se conserva:

```text
unidad_captura    = G

expresion_c_id    = NULL
expresion_c_texto = NULL
cantidad_captura  = "250"

expresion_d_id    = NULL
expresion_d_texto = NULL
deco_captura      = "10"
```

Y por separado:

```text
cantidad_canonica = resultado canónico
deco_canonico     = resultado canónico
```

La ausencia de expresión es un estado válido.

---

# 15. REGLA DE PRESENTACIÓN EN RE-EDICIÓN

La re-edición debe mostrar la **representación capturada**, no intentar reconstruirla desde el número canónico.

Principio:

> **La base de datos conserva la verdad canónica; la re-edición reconstruye la verdad de captura.**

Ejemplo:

```text
Base canónica:
cantidad = 0.5
```

No es suficiente para saber si el operador escribió:

```text
1/2
0.5
2/4
```

y por eso, cuando la captura es relevante, se conserva el texto capturado.

---

# 16. POR QUÉ EXPRESION-C Y EXPRESION-D SON INDEPENDIENTES

El diseño anterior utilizaba un único:

```text
expresion_id
```

Eso no permite representar correctamente dos expresiones independientes en una misma fila.

Una fila como:

```text
EXPRESION-C = 1/2
EXPRESION-D = 1/4
```

requiere dos identidades distintas:

```text
expresion_c_id
expresion_d_id
```

El documento adopta por tanto la regla:

> **EXPRESION-C y EXPRESION-D son datos independientes y nunca deben compartir un único campo de persistencia.**

---

# 17. DECISIÓN SOBRE `expresion_id`

El campo antiguo:

```text
expresion_id
```

queda fuera del nuevo modelo.

No se conserva para la nueva estructura porque representa una única expresión y genera ambigüedad entre C y D.

Las tres recetas reales existentes serán recapturadas bajo las nuevas reglas, por lo que no se requiere conservar una compatibilidad especial de captura antigua para ellas.

---

# 18. NUEVO MODELO CONCEPTUAL DE `recetas_ingredientes`

La estructura acordada es:

```text
id
receta_id
ingrediente_id

unidad_codigo_presentacion

expresion_c_id
expresion_c_texto
cantidad_captura

expresion_d_id
expresion_d_texto
deco_captura

cantidad
rol
```

### Interpretación

```text
unidad_codigo_presentacion
    = UM de captura

expresion_c_id
expresion_c_texto
cantidad_captura
    = captura de CANTIDAD

expresion_d_id
expresion_d_texto
deco_captura
    = captura de DECO

cantidad
    = CANTIDAD CANÓNICA

rol
    = DECO CANÓNICO
```

La UM canónica no se duplica en esta tabla porque se obtiene desde el ingrediente.

### Aclaración sobre `unidad_captura`

En el modelo conceptual, `unidad_captura` identifica la UM seleccionada
por el operador.

En la estructura física de `recetas_ingredientes`, ese mismo dato se
persiste como:

```text
unidad_codigo_presentacion

### Aclaración sobre `rol`

En el modelo actual, el campo físico `rol` se utiliza para conservar el valor
numérico canónico correspondiente a DECO.

Por tanto:

```text
rol = DECO CANÓNICO

---

# 19. TIPOS DE DATOS CONCEPTUALES

## Captura textual

```text
cantidad_captura = TEXT
deco_captura     = TEXT
```

Porque deben conservar exactamente la representación del operador.

## Identidad de expresión

```text
expresion_c_id = NULL o referencia válida
expresion_d_id = NULL o referencia válida
```

## Canónicos

```text
cantidad = valor numérico canónico
rol      = valor numérico canónico
```

---

# 20. ESTADO DE INTERFAZ NO PERSISTENTE

No deben almacenarse como parte de la receta:

```text
foco
cursor
colores
encabezado activo
atención visual
etapa visual temporal
```

Esos elementos sirven para la navegación de la interfaz, pero no son datos de la receta.

---

# 21. PRINCIPIO DE SEPARACIÓN DE RESPONSABILIDADES

El comportamiento conceptual debe mantenerse separado en tres responsabilidades:

```text
CAPTURA
    conserva lo que hace el operador

MOTOR
    interpreta, valida y calcula el estado canónico

PERSISTENCIA
    guarda el estado acordado
```

La interfaz refleja el estado, pero no debe convertirse en la fuente de verdad del modelo de negocio.

---

# 22. REGLAS QUE NO DEBEN ROMPERSE

## Regla 1

> Lo que el operador captura debe conservarse como captura.

## Regla 2

> El valor canónico es independiente de la representación visual.

## Regla 3

> EXPRESION-C y EXPRESION-D son independientes.

## Regla 4

> Una expresión no debe sustituir visualmente la captura por su equivalente decimal.

## Regla 5

> EXPRESION-D no modifica CANTIDAD.

## Regla 6

> La ausencia de expresión es válida.

## Regla 7

> La UM canónica proviene del ingrediente y no debe duplicarse sin necesidad.

## Regla 8

> La re-edición no debe adivinar la captura original desde el valor canónico.

## Regla 9

> Los datos de interfaz no son datos persistentes de la receta.

## Regla 10

> Antes de modificar el editor, consultar este documento y respetar la máquina de estados acordada.

---

# 23. TRATAMIENTO DE LAS TRES RECETAS REALES

Actualmente existen tres recetas reales que se consideran válidas para conservar como contenido.

La decisión acordada es:

```text
NO migrar artificialmente su antigua captura.

SÍ volver a capturarlas con las nuevas reglas.
```

De esta forma, las tres recetas reales quedarán incorporadas al nuevo modelo mediante captura nueva y consistente.

---

# 24. SITUACIÓN DE LA IMPLEMENTACIÓN

La especificación funcional de la máquina de estados queda definida.

Todavía no implica que el código existente haya sido modificado.

El orden correcto de trabajo es:

```text
1. Especificar
2. Implementar
3. Probar
4. Verificar persistencia
5. Verificar re-edición
```

No debe invertirse ese orden mediante parches aislados sobre la lógica antigua.

## 24.1. REGLA DE COMPLETITUD DE FILA Y CICLO DE PERSISTENCIA

Toda funcionalidad de captura debe verificarse sobre el ciclo completo de vida
de la fila, no únicamente sobre la captura inicial.

La cadena obligatoria es:

```text
CREAR FILA
    ↓
CAPTURAR DATO
    ↓
CONSERVAR CAPTURA
    ↓
TRANSPORTAR CAPTURA AL POST
    ↓
PERSISTIR
    ↓
RECUPERAR
    ↓
VOLVER A EDITAR
    ↓
RESTAURAR LA MISMA CAPTURA

Por tanto, toda fila nueva debe disponer de todos los elementos necesarios
para:

- presentar el dato al operador;
- conservar exactamente su captura;
- transportar esa captura durante el POST;
- persistirla;
- recuperarla posteriormente;
- volver a presentarla durante la re-edición.

La existencia de un mecanismo de captura en una fila ya existente
no garantiza que ese mecanismo exista también en la plantilla de fila nueva.

La plantilla de fila nueva debe auditarse explícitamente contra la estructura
y los mecanismos de una fila restaurada.

Una funcionalidad no se considera completamente integrada por funcionar
durante la captura inicial.

**NO MODIFICAR NADA MÁS.**
Debe superar obligatoriamente la prueba:

```text
CREAR
→ CAPTURAR
→ GUARDAR
→ CERRAR / RECARGAR
→ EDITAR
→ RESTAURAR
**NO MODIFICAR NADA MÁS.**
# 25. OBJETIVO FINAL

El resultado buscado es que una fila pueda conservar simultáneamente:

```text
CAPTURA
────────────────────────
UM            = CUP
EXPRESION-C   = 1/2
CANTIDAD      = 1/2
EXPRESION-D   = 1/4
DECO          = 1/4

CANÓNICO
────────────────────────
cantidad      = 0.5
deco          = 0.25
```

y que al volver a editar la receta el operador vea nuevamente:

```text
CUP | 1/2 | 1/2 | 1/4 | 1/4
```

sin perder la información que el motor necesita para trabajar.

---

# 26. FRASE RECTORA

> **CAPTURAR COMO EL OPERADOR LO EXPRESÓ.  
> CALCULAR COMO EL MOTOR LO NECESITA.  
> GUARDAR AMBAS VERDADES POR SEPARADO.  
> REEDITAR SIN ADIVINAR.**

---

**Fin de LA GUINDA DEL PASTEL**

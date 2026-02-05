# recetas_v2.py

## 1. Rol del archivo

`recetas_v2.py` implementa la **versión actual y activa** del manejo de recetas
en el sistema **recetas_app**.

Este módulo:
- define qué es una receta
- gestiona su ciclo de vida
- asocia ingredientes con cantidades y unidades
- diferencia ingredientes básicos y decorativos
- permite visualizar una receta completa

Es el **núcleo funcional** del sistema.

---

## 2. Principios de diseño

- Separación estricta de responsabilidades
- Sin menús propios (orquestado por `main.py`)
- Persistencia delegada a `persistencia.py`
- Uso obligatorio de nomencladores
- Flujo guiado (no IDs manuales)
- Regla de retorno: toda acción vuelve a un punto conocido

---

## 3. Modelo de datos

### 3.1 Receta (`recetas.json`)

Cada receta contiene:

- `id` : identificador interno
- `nombre` : nombre normalizado (minúsculas)
- `raciones_base` : cantidad base de raciones
- `peso_racion` : valor numérico
- `unidad_peso_racion_id` : referencia a unidad de medida
- `estado` : `en_construccion` | `valida`

Una receta sin ingredientes **no es válida**.

---

### 3.2 Ingredientes por receta (`recetas_ingredientes.json`)

Relación independiente receta–ingrediente:

- `id`
- `receta_id`
- `ingrediente` : nombre del ingrediente
- `cantidad`
- `unidad_id`
- `rol` : `basico` | `deco`

Un mismo ingrediente puede existir en ambos roles.

---

## 4. Flujo funcional

### 4.1 Crear receta

La función `crear_receta()`:

1. Solicita nombre de la receta
2. Solicita raciones base
3. Solicita peso de una ración
4. Solicita unidad del peso
5. Crea la receta en estado `en_construccion`
6. Redirige automáticamente a la carga de ingredientes

No existen recetas “vacías”.

---

### 4.2 Agregar ingredientes

La función `agregar_ingredientes_receta()`:

- utiliza selectores de ingrediente y unidad
- valida cantidades numéricas
- asigna rol (`basico` por defecto)
- permite agregar múltiples ingredientes
- actualiza automáticamente el estado de la receta

---

### 4.3 Modificar ingredientes

La función `modificar_ingredientes_receta()` permite:

- cambiar cantidad
- alternar rol (`basico` / `deco`)
- eliminar ingredientes

El estado de la receta se recalcula al finalizar.

---

### 4.4 Ver receta completa

La función `ver_receta_completa_v2()` muestra:

- nombre
- estado
- raciones base
- peso de ración con unidad
- ingredientes básicos
- ingredientes decorativos

La visualización es de solo lectura,
equivalente a una “página de libro”.

---

## 5. Selectores reutilizables

El módulo define:

- `seleccionar_receta_v2()`

Este selector:
- lista recetas disponibles
- muestra estado
- evita el uso de IDs manuales
- es reutilizable por otros flujos

---

## 6. Manejo de errores

- Entradas inválidas no rompen el flujo
- Cancelaciones controladas
- Estados coherentes
- Persistencia consistente

---

## 7. Relación con otros módulos

`recetas_v2.py` depende de:

- `persistencia.py` (datos)
- `nomencladores.py` (ingredientes y unidades)

No depende de:
- `main.py`
- módulos de presentación
- cálculos externos

---

## 8. Alcance actual

✔ Gestión completa de recetas  
✔ Modelo estable  
✔ Visualización funcional  
✔ Base lista para cálculos y tablas  

---

## 9. Pendientes

- Cálculo de raciones
- Tablas de salida
- Exportación
- Versionado histórico
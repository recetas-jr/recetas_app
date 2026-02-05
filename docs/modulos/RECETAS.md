contenido completo del archivo RECETAS_V2.md)
# Módulo RECETAS_V2

## 1. Propósito

El módulo **Recetas V2** gestiona recetas gastronómicas completas,
permitiendo:

- crear recetas
- asociar ingredientes
- diferenciar ingredientes básicos y decorativos
- manejar unidades de medida coherentes
- visualizar una receta completa

Este módulo sustituye progresivamente al sistema de recetas legado.

---

## 2. Principios de diseño

- Arquitectura modular
- Sin estado global
- Persistencia delegada a `persistencia.py`
- Uso exclusivo de nomencladores
- Flujo guiado (no IDs a ciegas)
- Regla de retorno: toda acción vuelve a un destino conocido

---

## 3. Modelo de datos

### 3.1 Receta (`recetas.json`)

Cada receta contiene:

- `id` : identificador interno
- `nombre` : nombre normalizado (minúsculas)
- `raciones_base` : cantidad base de raciones
- `peso_racion` : valor numérico del peso
- `unidad_peso_racion_id` : referencia a nomenclador de unidades
- `estado` : `en_construccion` | `valida`

---

### 3.2 Ingredientes por receta (`recetas_ingredientes.json`)

Relación receta–ingrediente:

- `id`
- `receta_id`
- `ingrediente` : nombre del ingrediente (minúsculas)
- `cantidad`
- `unidad_id`
- `rol` : `basico` | `deco`

Un mismo ingrediente puede existir en ambos roles.

---

## 4. Flujo funcional

### 4.1 Crear receta

1. Se solicita nombre
2. Se solicitan raciones base
3. Se solicita peso de ración
4. Se selecciona unidad del peso
5. Se crea receta en estado `en_construccion`
6. Se redirige automáticamente a agregar ingredientes

---

### 4.2 Agregar ingredientes

- Selección desde nomenclador
- Cantidad numérica validada
- Selección de unidad
- Rol:
  - `basico` (por defecto)
  - `deco`
- La receta pasa a estado `valida` cuando tiene al menos un ingrediente

---

### 4.3 Modificar ingredientes

Permite:

- cambiar cantidad
- cambiar rol
- eliminar ingrediente

El estado de la receta se recalcula automáticamente.

---

### 4.4 Ver receta completa

Muestra:

- nombre
- estado
- raciones base
- peso de ración con unidad
- ingredientes básicos
- ingredientes decorativos

La visualización es de solo lectura.

---

## 5. Selectores reutilizables

El módulo incluye selectores para:

- recetas (`seleccionar_receta_v2`)
- ingredientes
- unidades

Evitan el uso de IDs manuales y mejoran la UX.

---

## 6. Alcance actual

✔ Flujo principal completo  
✔ Modelo estable  
✔ Persistencia coherente  
✔ Visualización funcional  

---

## 7. Pendiente (fuera de este módulo)

- Cálculo de raciones
- Tablas de salida
- Exportación (PDF / ficha técnica)
- Nomenclador formal de recetas
- Versionado histórico de recetas
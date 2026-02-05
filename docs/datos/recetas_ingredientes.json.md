# recetas_ingredientes.json

## 1. Propósito

`recetas_ingredientes.json` almacena la **relación entre recetas e ingredientes**
del sistema **recetas_app**.

Este archivo define:
- qué ingredientes componen cada receta
- en qué cantidad
- con qué unidad
- y con qué rol (básico o decorativo)

Es el archivo que convierte una receta en una receta real.

---

## 2. Tipo de archivo

- Formato: JSON
- Contenido: lista de objetos
- Uso: datos relacionales (receta ↔ ingrediente)

---

## 3. Estructura de datos

Cada entrada representa un ingrediente dentro de una receta
y contiene los siguientes campos:

- `id` : integer  
  Identificador interno único de la relación.

- `receta_id` : integer  
  Referencia al `id` de la receta en `recetas.json`.

- `ingrediente` : string  
  Nombre del ingrediente (normalizado, minúsculas).

- `cantidad` : float  
  Cantidad del ingrediente para la receta base.

- `unidad_id` : integer  
  Referencia a la unidad de medida en `unidades.json`.

- `rol` : string  
  Rol del ingrediente dentro de la receta. Valores permitidos:
  - `basico`
  - `deco`

---

## 4. Reglas de negocio

- Una receta debe tener al menos un ingrediente para ser válida
- El rol por defecto es `basico`
- Un mismo ingrediente puede aparecer:
  - como `basico`
  - como `deco`
- La cantidad debe ser mayor que cero
- La unidad debe ser compatible con el ingrediente
- No se permiten duplicados exactos (misma receta, ingrediente y rol)

---

## 5. Ejemplo de contenido

```json
[
  {
    "id": 1,
    "receta_id": 1,
    "ingrediente": "arroz",
    "cantidad": 1000,
    "unidad_id": 1,
    "rol": "basico"
  },
  {
    "id": 2,
    "receta_id": 1,
    "ingrediente": "sal fina",
    "cantidad": 10,
    "unidad_id": 1,
    "rol": "basico"
  },
  {
    "id": 3,
    "receta_id": 1,
    "ingrediente": "cebollino",
    "cantidad": 5,
    "unidad_id": 1,
    "rol": "deco"
  }
]
6. Relación con otros archivos
Depende de recetas.json (receta_id)

Depende de ingredientes.json (nombre del ingrediente)

Depende de unidades.json (unidad_id)

No existe sin recetas

7. Módulos que lo utilizan
persistencia.py

recetas_v2.py

8. Alcance y límites
recetas_ingredientes.json:

NO define recetas

NO define ingredientes

NO define unidades

NO realiza cálculos

Su responsabilidad termina en describir la composición exacta de una receta.


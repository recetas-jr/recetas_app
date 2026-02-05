# ingredientes.json

## 1. Propósito

`ingredientes.json` almacena el **nomenclador de ingredientes** del sistema
**recetas_app**.

Su función es:
- centralizar los nombres de ingredientes
- evitar duplicaciones
- garantizar consistencia en todas las recetas

Este archivo **no almacena cantidades ni unidades**.

---

## 2. Tipo de archivo

- Formato: JSON
- Contenido: lista de objetos
- Uso: datos base (catálogo)

---

## 3. Estructura de datos

Cada ingrediente es un objeto con los siguientes campos:

- `id` : integer  
  Identificador interno único.

- `descripcion` : string  
  Nombre del ingrediente en **minúsculas**.

---

## 4. Reglas de negocio

- No pueden existir dos ingredientes con la misma descripción
- La descripción se normaliza a minúsculas
- El `id` se genera automáticamente
- Los ingredientes **no se eliminan**, solo se dejan de usar
- Un ingrediente puede:
  - ser básico en una receta
  - ser decorativo en otra
  - cumplir ambos roles

---

## 5. Ejemplo de contenido

```json
[
  {
    "id": 1,
    "descripcion": "arroz"
  },
  {
    "id": 2,
    "descripcion": "sal fina"
  },
  {
    "id": 3,
    "descripcion": "cebollino"
  }
]

6. Relación con otros archivos

Se relaciona con recetas_ingredientes.json

No contiene información de recetas

No contiene información de unidades

7. Módulos que lo utilizan

nomencladores.py

recetas_v2.py

8. Alcance y límites

ingredientes.json:

NO almacena cantidades

NO almacena unidades

NO almacena roles

NO almacena estados

Su responsabilidad termina en definir qué ingredientes existen.

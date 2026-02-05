# recetas.json

## 1. Propósito

`recetas.json` almacena la **información general de las recetas** del sistema
**recetas_app**.

Este archivo define **qué recetas existen** y sus atributos principales,
pero **no** almacena los ingredientes (eso se maneja por separado).

---

## 2. Tipo de archivo

- Formato: JSON
- Contenido: lista de objetos
- Uso: datos principales del dominio “recetas”

---

## 3. Estructura de datos

Cada receta es un objeto con los siguientes campos:

- `id` : integer  
  Identificador interno único de la receta.

- `nombre` : string  
  Nombre de la receta, normalizado en **minúsculas**.

- `raciones_base` : integer  
  Cantidad de raciones para la cual está definida la receta.

- `peso_racion` : float  
  Peso de una ración individual.

- `unidad_peso_racion_id` : integer  
  Referencia a la unidad de medida en `unidades.json`.

- `estado` : string  
  Estado funcional de la receta. Valores permitidos:
  - `en_construccion`
  - `valida`

---

## 4. Reglas de negocio

- Una receta sin ingredientes no es válida
- El estado inicial es siempre `en_construccion`
- El estado pasa a `valida` cuando tiene al menos un ingrediente
- El nombre debe ser único (a nivel lógico)
- El peso de la ración debe ser mayor que cero
- La unidad del peso debe ser coherente con el tipo `peso`

---

## 5. Ejemplo de contenido

```json
[
  {
    "id": 1,
    "nombre": "arroz blanco",
    "raciones_base": 10,
    "peso_racion": 120,
    "unidad_peso_racion_id": 1,
    "estado": "valida"
  },
  {
    "id": 2,
    "nombre": "arroz frito especial",
    "raciones_base": 5,
    "peso_racion": 200,
    "unidad_peso_racion_id": 1,
    "estado": "en_construccion"
  }
]
6. Relación con otros archivos
Se relaciona con recetas_ingredientes.json mediante receta_id

Se relaciona con unidades.json mediante unidad_peso_racion_id

No contiene ingredientes directamente

7. Módulos que lo utilizan
persistencia.py

recetas_v2.py

8. Alcance y límites
recetas.json:

NO almacena ingredientes

NO almacena preparación ni elaboración

NO realiza cálculos

NO gestiona unidades directamente

Su responsabilidad termina en definir la receta como entidad principal.


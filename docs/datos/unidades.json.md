# unidades.json

## 1. Propósito

`unidades.json` almacena el **nomenclador de unidades de medida** del sistema
**recetas_app**.

Su función es:
- definir las unidades válidas del sistema
- evitar mezclas de unidades incompatibles
- servir como referencia única para cantidades y pesos

Este archivo **no almacena cantidades**, solo definiciones de unidades.

---

## 2. Tipo de archivo

- Formato: JSON
- Contenido: lista de objetos
- Uso: datos base (nomenclador)

---

## 3. Estructura de datos

Cada unidad es un objeto con los siguientes campos:

- `id` : integer  
  Identificador interno único.

- `nombre` : string  
  Nombre completo de la unidad (ej.: "gramo", "kilogramo").

- `simbolo` : string  
  Símbolo corto de la unidad (ej.: "g", "kg").

- `tipo` : string  
  Tipo semántico de la unidad. Valores permitidos:
  - `peso`
  - `volumen`
  - `unidad`

---

## 4. Reglas de negocio

- No pueden existir dos unidades con el mismo símbolo
- El símbolo identifica la unidad de forma única
- El tipo define compatibilidad entre unidades
- Las conversiones **no se realizan automáticamente**
- No se permiten mezclas de tipos incompatibles

---

## 5. Ejemplo de contenido

```json
[
  {
    "id": 1,
    "nombre": "gramo",
    "simbolo": "g",
    "tipo": "peso"
  },
  {
    "id": 2,
    "nombre": "kilogramo",
    "simbolo": "kg",
    "tipo": "peso"
  },
  {
    "id": 3,
    "nombre": "mililitro",
    "simbolo": "ml",
    "tipo": "volumen"
  },
  {
    "id": 4,
    "nombre": "unidad",
    "simbolo": "u",
    "tipo": "unidad"
  }
]
6. Relación con otros archivos
Se referencia desde recetas.json

Se referencia desde recetas_ingredientes.json

No contiene información de recetas ni ingredientes

7. Módulos que lo utilizan
nomencladores.py

recetas_v2.py

8. Alcance y límites
unidades.json:

NO almacena cantidades

NO almacena conversiones

NO realiza cálculos

NO valida reglas de negocio complejas

Su responsabilidad termina en definir qué unidades existen y de qué tipo son.

# nomencladores.py

## 1. Rol del archivo

`nomencladores.py` gestiona todos los **catálogos base (nomencladores)** del sistema
**recetas_app**.

Un nomenclador es un conjunto controlado de valores reutilizables que:
- evita duplicaciones
- garantiza consistencia de datos
- centraliza la validación básica

Actualmente se gestionan:
- ingredientes
- unidades de medida

---

## 2. Principios de diseño

- Datos normalizados (minúsculas)
- Sin estado global persistente
- Persistencia delegada a `persistencia.py`
- Menús locales y controlados
- Reutilización mediante selectores
- Separación entre gestión y selección

---

## 3. Nomenclador de ingredientes

### 3.1 Estructura de datos

Cada ingrediente contiene:
- `id`
- `descripcion`

Los ingredientes:
- se almacenan en `ingredientes.json`
- se identifican internamente por `id`
- se muestran por `descripcion`

---

### 3.2 Funcionalidades

El módulo permite:
- listar ingredientes
- crear ingredientes
- editar ingredientes
- buscar ingredientes por descripción

Se evita la duplicación mediante normalización de texto.

---

## 4. Nomenclador de unidades de medida

### 4.1 Estructura de datos

Cada unidad contiene:
- `id`
- `nombre`
- `simbolo`
- `tipo` (peso / volumen / unidad)

Las unidades:
- se almacenan en `unidades.json`
- se seleccionan por símbolo o listado
- mantienen compatibilidad semántica por tipo

---

### 4.2 Funcionalidades

El módulo permite:
- listar unidades
- crear unidades
- editar unidades
- buscar unidades por símbolo

---

## 5. Selectores reutilizables

El módulo define funciones selectoras reutilizables para ser usadas por
otros módulos (por ejemplo `recetas_v2.py`):

- selección de ingrediente
- selección de unidad

Estos selectores:
- presentan listados numerados
- evitan el uso de IDs manuales
- devuelven valores normalizados

---

## 6. Menús internos

`nomencladores.py` incluye menús propios para:
- ingredientes
- unidades
- navegación interna

Estos menús:
- no dependen del menú principal
- retornan siempre a un punto conocido
- no contienen lógica de negocio externa

---

## 7. Manejo de errores

- Entradas inválidas no rompen el sistema
- Cancelaciones controladas
- Mensajes claros al usuario
- Flujo siempre reversible

---

## 8. Alcance y límites

`nomencladores.py`:
- NO conoce recetas
- NO realiza cálculos
- NO gestiona estados
- NO interpreta cantidades

Su responsabilidad termina en **proveer datos base confiables**.

---

## 9. Estado actual

- Estable
- Cerrado en funcionalidad
- Reutilizado por módulos de recetas

Cualquier ampliación futura debe respetar
la naturaleza de “catálogo” del módulo.
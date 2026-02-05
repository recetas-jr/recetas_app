# main.py

## 1. Rol del archivo

`main.py` es el **punto de entrada** del sistema **recetas_app**.

Su única responsabilidad es:
- mostrar el menú principal
- orquestar la navegación entre módulos
- delegar toda la lógica de negocio a otros archivos

`main.py` **NO** contiene:
- lógica de recetas
- lógica de nomencladores
- acceso directo a datos

---

## 2. Principios aplicados

- Orquestación pura (controller)
- Sin lógica de dominio
- Sin persistencia directa
- Flujo guiado por menús
- Regla de retorno: toda acción vuelve a un menú conocido

---

## 3. Menú principal

El menú principal expone las grandes áreas del sistema:

- Nomencladores
- Recetas (legado)
- Recetas V2 (actual)
- Cálculo de raciones (pendiente)
- Salida controlada del sistema

El menú es un bucle infinito que solo termina al seleccionar “Salir”.

---

## 4. Integración de módulos

`main.py` importa y utiliza:

- `menu_nomencladores()` desde `nomencladores.py`
- `menu_recetas()` desde `recetas.py` (legado)
- funciones específicas desde `recetas_v2.py`:
  - crear receta
  - modificar ingredientes
  - ver receta completa
  - seleccionar receta

La comunicación entre módulos se hace **por funciones**, no por variables compartidas.

---

## 5. Submenú Recetas V2

El submenú de Recetas V2 permite:

- crear una receta
- modificar ingredientes de una receta existente
- visualizar una receta completa

Este submenú:
- no maneja IDs manuales
- utiliza selectores
- no contiene lógica de negocio

---

## 6. Control de flujo

- Cada opción valida la entrada del usuario
- Entradas inválidas no rompen el sistema
- El flujo siempre retorna a un menú
- No existen salidas abruptas

---

## 7. Configuración

`main.py` carga configuración básica desde `config.json` a través de `persistencia.py`.

Actualmente:
- solo se usa como base para extensiones futuras
- no altera el flujo principal

---

## 8. Estado actual

- Estable
- Funcional
- Cerrado en responsabilidad

Cualquier ampliación futura debe:
- respetar la separación de responsabilidades
- delegar la lógica a módulos específicos
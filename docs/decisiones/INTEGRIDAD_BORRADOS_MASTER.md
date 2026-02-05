# Decisión: Integridad referencial en borrados (MASTER y nomencladores)

## Contexto
El sistema maneja:
- Nomencladores: Platos, Ingredientes, Unidades de Medida.
- Un MASTER de recetas que depende de esos nomencladores.

Borrar un elemento referenciado puede romper la coherencia del sistema.

## Decisión

1. ❌ No se permite borrar un PLATO si:
   - Está siendo usado por al menos una receta en el MASTER.

2. ❌ No se permite borrar una UNIDAD DE MEDIDA si:
   - Está asociada a al menos un ingrediente.

3. ❌ No se permite borrar un INGREDIENTE si:
   - Está siendo usado en alguna receta (según validación definida).

4. ✅ Sí se permite borrar una RECETA MASTER:
   - Siempre con confirmación explícita del usuario.

## Implementación

- Las validaciones se hacen en backend antes de ejecutar el borrado.
- Si el elemento está en uso:
  - Se bloquea la operación.
  - Se muestra un mensaje claro al usuario.
- Si no está en uso:
  - Se borra.
  - Se guarda persistencia.
  - Se notifica éxito.

## Consecuencias

- Se protege la integridad de los datos.
- Se evita dejar recetas huérfanas o referencias rotas.
- Se prioriza seguridad de datos sobre comodidad operativa.

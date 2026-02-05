# Decisión: Flujo de captura en MASTER Web y control de abandono de datos

## Contexto
El formulario MASTER de recetas es largo y con múltiples campos.
El usuario puede cambiar de plato o abandonar una receta sin guardarla, perdiendo datos.

## Decisión

1. Se implementa control de “cambios no guardados”.
2. Si el usuario intenta cambiar de plato y hay datos sin guardar:
   - El sistema muestra una advertencia.
   - El usuario puede cancelar o continuar.
3. Se estandariza el uso de ENTER para:
   - Avanzar entre campos.
   - Agilizar la captura.
4. El botón “Finalizar y Guardar” es la única acción que:
   - Confirma y persiste la receta.

## Implementación

- Se mantiene un flag `hayCambiosNoGuardados`.
- Se marca en cualquier input o textarea modificado.
- Al cambiar de plato:
  - Si hay cambios → se pide confirmación.
- El flujo de foco se controla por JavaScript.

## Consecuencias

- Se reduce el riesgo de pérdida accidental de datos.
- Se mejora la experiencia del operador.
- El sistema se comporta de forma predecible y segura.
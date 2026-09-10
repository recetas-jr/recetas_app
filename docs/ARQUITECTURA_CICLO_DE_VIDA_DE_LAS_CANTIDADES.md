==========================================================
ARQUITECTURA DEL CICLO DE VIDA DE LAS CANTIDADES
==========================================================

CAPÍTULO 1
Naturaleza de una Cantidad
Propósito

Este capítulo define qué representa una cantidad dentro de recetas_app y establece los conceptos fundamentales sobre los que se construye el Motor de Conversión.

No describe algoritmos ni implementación.

Describe el dominio.

1.1 ¿Qué es una cantidad?

A primera vista podría parecer que una cantidad es simplemente un valor numérico asociado a una unidad de medida.

Sin embargo, dentro del dominio gastronómico esto no es suficiente.

Una expresión como:

2 cucharadas

carece de significado por sí sola.

No es posible determinar:

su peso;
su volumen;
su valor nutricional;
su costo;
ni su equivalencia con otras unidades.

El significado aparece únicamente cuando la cantidad se interpreta en el contexto de un ingrediente específico.

Por ejemplo:

2 cucharadas de azúcar

y

2 cucharadas de aceite

comparten exactamente la misma cantidad y la misma unidad, pero representan magnitudes completamente diferentes.

Por esta razón, dentro de recetas_app una cantidad nunca se considera un dato independiente.

Siempre forma parte de una expresión culinaria completa.

1.2 La expresión culinaria

La unidad mínima de información manipulada por el sistema está formada por tres elementos inseparables:

ingrediente;
cantidad;
unidad.

Por ejemplo:

Ingrediente:
Harina

Cantidad:
2

Unidad:
Taza

Eliminar cualquiera de estos tres elementos destruye el significado de la información.

1.3 Principio fundamental

Una cantidad nunca posee significado por sí misma.

El significado surge exclusivamente de la combinación de:

ingrediente;
cantidad;
unidad.

En consecuencia, toda conversión realizada por el Motor deberá ejecutarse siempre dentro del contexto de un ingrediente específico.

Este principio constituye uno de los fundamentos del modelo de dominio de recetas_app.
Reglas de trabajo — MASTER Web y Nomencladores
Estado de referencia

Rama base: master-ui-final-estable

El MASTER funciona correctamente:

A) Carga Plato

B) Agrega ingredientes

C) Guarda

D) Va al listado

Nomencladores integrados y funcionando:

Tipos de Plato

Unidades de Medida

Ingredientes

Platos

Este estado se considera base estable. Cualquier trabajo parte desde aquí.

Reglas operativas

Cambios pequeños y uno por uno
No se hacen paquetes grandes de cambios. Cada modificación debe ser:

pequeña,

entendible,

reversible.

Primero probar en local → luego commit
Si un cambio no está probado y validado, no se commitea.

El MASTER es sagrado
Después de cada cambio se debe revalidar:

A) carga Plato

B) agrega ingredientes

C) guarda

D) va al listado

Si algo falla:

No se continúa.

Se vuelve al último commit estable con Git.

Un objetivo por commit
Cada commit debe tener un solo propósito claro.
Ejemplos:

“Estandarización de mensajes en Tipos de Plato”

“Ajuste de UI en Unidades”

“Mejora de validación en Ingredientes”

Está prohibido mezclar varios objetivos en un mismo commit.

No tocar ENTER / ESC / validaciones sin documentar
Cualquier cambio en:

flujo de ENTER,

comportamiento de ESC,

validaciones de datos,

debe:

documentarse en docs/decisiones/,

y marcarse explícitamente como REGLA NUEVA.

Flujo de trabajo con archivos

Se trabaja un solo archivo o un solo bloque a la vez.

El archivo se presenta con:

Nombre del archivo al inicio

Nombre del archivo al final

URL a probar

Procedimiento:

Se copia el archivo

Se prueba

Se valida el MASTER

Si todo está OK → commit

Referencia de cantidad de líneas
Cada vez que se toque un archivo:

Se anota (o se tiene en cuenta) la cantidad de líneas

Para detectar pérdidas accidentales de código.

Si algo se rompe, se revierte con Git

No se hacen parches sobre cosas rotas.

Se vuelve al último commit estable y se corrige desde ahí.

Cada módulo/nomenclador estable = su propio commit
Cuando:

un nomenclador queda funcionando,

y el MASTER sigue funcionando,

entonces:

se hace un commit exclusivo para ese cambio.

Objetivo permanente

Trabajar con bisturí, no con machete:

Cambios controlados

Probados

Versionados

Sin perder estabilidad

El sistema debe poder volver en cualquier momento a un punto sano usando Git.

🆕 Reglas operativas añadidas (UI/UX y estabilidad)
1) El MASTER es intocable mientras se trabaja en nomencladores

Cualquier cambio en nomencladores:

Se prueba el MASTER antes y después del cambio.

Si el MASTER falla → revertir inmediatamente al último commit estable.

No se hacen “arreglos rápidos” en web_app.py fuera del plan acordado.

2) web_app.py se modifica con bisturí

Cambios pequeños y localizados.

Un objetivo por commit.

Antes de tocar web_app.py:

Identificar la función/ruta exacta.

Verificar que no afecta rutas del MASTER (/, /admin/recetas/nueva, listados, etc.).

3) Ejecución estándar del servidor Flask

El servidor siempre se ejecuta desde la raíz del proyecto con:

python -m modulo_web.web_app

Evitar ejecutar python web_app.py desde subcarpetas para no romper imports.

4) Estado limpio antes de cambios importantes

Antes de empezar un bloque de trabajo:

git status

Debe estar:

nothing to commit, working tree clean

Si no está limpio, no se continúa hasta ordenar el repo.

5) Reaplicación de mejoras UI por capas (orden obligatorio)

Orden fijo:

Tipos de Plato

Unidades

Ingredientes

Platos

En cada paso:

Cambio pequeño

Probar el MASTER

Commit

Continuar al siguiente

6) Estándar UI obligatorio

Todos los mensajes deben ser informativos:

Indicar qué elemento y en qué módulo.

Usar colores diferenciados y ícono de acción.

Foco violeta en el campo activo:

Fondo: violeta claro

Borde: violeta oscuro

Cualquier excepción debe quedar documentada.
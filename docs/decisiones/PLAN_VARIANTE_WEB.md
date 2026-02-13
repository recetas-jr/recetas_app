PLAN DE CONSTRUCCIÓN — SISTEMA DE RECETAS (VARIANTE WEB)
🎯 Objetivo

Construir un sistema web de recetas con separación total entre:

👥 Usuario de Red (solo consulta)

🛠️ Administrador del Sistema (mantiene datos)

Los datos se construyen a partir de nomencladores controlados y luego se usan para crear el MASTER de recetas.

🧱 Principios de Diseño

❌ No se permite texto libre donde exista nomenclador.

✅ Todo dato seleccionado debe venir de catálogo controlado.

❌ No se borran registros: solo se desactivan.

✅ La validación real se hace en backend, no solo en HTML.

✅ Las tablas de visualización siempre tienen scroll interno.

✅ Los formularios de captura deben permanecer siempre visibles.

🧩 Orden de Construcción de Módulos
FASE W2 — NOMENCLADORES
1️⃣ Unidades de Medida (Nomenclador)

Estado: 🟡 En curso

Funcionalidades obligatorias:

✔ Alta

✔ Listado

✔ Desactivar (no borrar)

🔜 Reactivar

🔒 Validación backend:

código solo letras

longitud 1 o 2 caracteres

UI:

campos del tamaño del dato real

tabla con scroll interno

formulario siempre visible

Datos persistentes:

{ "id": 1, "codigo": "KG", "nombre": "Kilogramo", "activo": true }

2️⃣ Ingredientes (Nomenclador)

Estado: 🔴 Pendiente

Reglas:

El ingrediente NO define cantidad.

El ingrediente selecciona:

una Unidad de Medida por id

No se permite texto libre para unidad.

Funcionalidades:

Alta

Listado

Desactivar / Reactivar

Validación de duplicados por nombre

Datos persistentes:

{ "id": 1, "nombre": "Arroz", "unidad_id": 2, "activo": true }

3️⃣ Platos (Nomenclador)

Estado: 🟡 Parcial

Reglas:

El plato NO tiene ingredientes.

Es solo la entidad del platillo.

Funcionalidades:

Alta

Listado

Desactivar / Reactivar

Campos:

nombre

tipo de plato

peso por ración

foto (futuro)

FASE W3 — RECETA MASTER
4️⃣ Constructor de Receta MASTER

Relaciona:

Plato (por id)

Ingredientes (por id)

Cantidades

Rol de ingrediente

Reglas:

Raciones base fijas

Recalcular solo para consulta (no se guarda)

👥 Vistas de Usuario de Red

Listado de recetas publicadas

Ficha técnica

Recalcular raciones (temporal)

NO puede modificar datos

📌 Reglas de UX Generales

Formularios siempre visibles

Tablas con scroll interno

Evitar scroll de página

Campos del tamaño del dato real

Autocomplete del navegador desactivado

📌 Notas de Implementación

Archivos JSON como persistencia local en fase inicial

Rutas administrativas siempre bajo /admin/*

Separación clara entre:

nomencladores

datos MASTER

vistas públicas

✅ PLAN INICIAL REGISTRADO



14-ENE-2026
🔒 Reglas de Integridad — Unidades de Medida
❌ Borrado

No se permite borrar registros.

Solo se permite desactivar / reactivar.

Los registros inactivos se conservan por integridad histórica.

🔁 Reactivación

Las unidades de medida inactivas pueden ser reactivadas por el administrador.

🔒 Validaciones Backend Obligatorias

Antes de guardar:

El código debe contener solo letras.

Longitud del código: 1 o 2 caracteres.

No se permiten duplicados:

mismo código (ignorando mayúsculas/minúsculas)

mismo nombre (ignorando mayúsculas/minúsculas)

✏️ Edición

Solo se permite editar el nombre de la unidad de medida.

El código no debe modificarse una vez creado.

Este documento debe revisarse al iniciar cada nueva fase o pestaña de trabajo.

14-ENE-2026
🧭 UX — Flujo de Captura (Nomencladores)

Diseño orientado a captura rápida por teclado.

Entrada de Datos

No se utiliza botón Guardar.

El guardado se realiza únicamente con la tecla Enter en el último campo.

Campo Código (primer escaque)

Autofocus al cargar la página.

Enter:

si está vacío → no avanza.

si tiene valor → pasa al campo Nombre.

ESC:

cancela la captura en cualquier momento antes del guardado.

limpia los campos.

elimina el foco (cursor desaparece).

Campo Nombre (segundo escaque)

Clic con Código vacío:

muestra advertencia.

devuelve el foco al campo Código.

Enter:

guarda el registro.

limpia los campos.

foco vuelve automáticamente al campo Código.

Mensajes de Ayuda

Mostrar texto visible:

“ESC para salir”

“Enter guarda”

Objetivos del Diseño

Minimizar uso del mouse.

Permitir captura en serie.

Evitar errores de flujo.

Mantener comportamiento predecible para el operador.

Estas reglas aplican también a futuros nomencladores
(Ingredientes, Platos, etc.).

15-ENE-2026
👉 Agregar sección:

Nomenclador Unidades de Medida — Reglas

Código: solo letras, longitud 1–2

Código y nombre no pueden duplicarse

Mensajes de validación visibles en UI

No se limpian campos si hay error

Enter guarda

ESC cancela entrada

Esto es diseño funcional del sistema, no detalle técnico.

15-ENE-2026
✅ Código de Unidad de Medida se guarda y se muestra en MAYÚSCULAS
para estandarización visual en todo el sistema.

15-ENE-2026
Política de Datos del Proyecto

Durante desarrollo se usan datos de prueba

Al cerrar un módulo, los JSON se limpian

A partir de ahí solo se cargan datos reales

No se reutilizan archivos de producción para testing

✅ Cada módulo se limpia antes de pasar al siguiente
✅ Datos de prueba NO pasan a producción

15-ENE-2026
Para Nomenclador UM:

✔ Si hay varios errores → se muestran TODOS
✔ Mensajes incluyen el valor duplicado
✔ Color de error diferenciado (rojo)

Esto lo vamos a replicar luego en:

Ingredientes

Platos

Receta MASTER

Patrón de sistema ✔

COMIENZO DE DECISIONES  DIA:15-ENE-2026  HORA: 1:25 pm

ETAPA ACTUAL DEL PROYECTO — ENFOQUE OPERATIVO

1) En esta etapa, el objetivo principal del sistema es OPERATIVO, no contable.

El sistema está orientado a que:
- los usuarios de red puedan ver las recetas existentes
- puedan recalcular cantidades para distintas raciones

No es objetivo en esta etapa:
- control histórico estricto
- contabilidad
- costeo

--------------------------------------------------

REGLAS POR ETAPAS PARA NOMENCLADORES

2) Solo el Nomenclador de Unidades de Medida se considera ESTRUCTURAL y rígido.

Para Unidades de Medida:
- NO se permite borrar
- solo se permite desactivar / reactivar
- el código no se puede modificar

Para los demás nomencladores en esta etapa (Ingredientes y Platos):
- SÍ se permite editar
- SÍ se permite eliminar
- NO se usa aún el mecanismo de activo / inactivo

En etapas futuras, todos los nomencladores pasarán a:
- no borrar
- solo activar / desactivar

--------------------------------------------------

DECISIÓN DE DOMINIO: BEBIDA NO ES PLATO

3) Las bebidas NO forman parte del Nomenclador de Platos.

El Nomenclador de Platos representa únicamente:
- comida sólida

Las bebidas podrán tratarse en el futuro como:
- otra entidad
- u otro tipo de receta

Pero NO pertenecen al catálogo de platos.

--------------------------------------------------

TIPO DE PLATO — CATÁLOGO CONTROLADO

4) El campo "tipo de plato" es un catálogo controlado, no texto libre.

Valores permitidos en Fase W2:

- Principal
- Guarnición
- Postre

No se permiten otros valores.

--------------------------------------------------

PESO POR RACIÓN — DEFINICIÓN FUNCIONAL

5) El campo "peso por ración" es un valor numérico que:

- debe ser mayor que cero
- puede tener decimales (float)

Se utiliza para:
- estandarización
- nutrición
- análisis futuros

No interviene directamente en el cálculo de ingredientes,
ya que las cantidades se definen en la Receta MASTER.

--------------------------------------------------

REGLAS DE VALIDACIÓN (SE MANTIENEN)

6) Aunque el sistema esté en etapa operativa:

- todas las validaciones deben hacerse en backend
- no se depende solo de validaciones HTML o JavaScript
- los duplicados deben detectarse en servidor

--------------------------------------------------

PROTOCOLO DE DOCUMENTACIÓN DE DECISIONES

7) Toda decisión nueva de arquitectura o terminología debe registrarse con el formato:

COMIENZO DE DECISIONES  DIA:DD-MMM-AAAA  HORA: HH:MM am/pm
< texto >
FIN DE DECISIONES  DIA:DD-MMM-AAAA  HORA: HH:MM am/pm

Reglas:
- la fecha y hora deben ser idénticas al inicio y al final
- cada bloque representa una unidad de cambio del proyecto
- no se agregan decisiones fuera de este formato

Este protocolo aplica para:
- docs/decisiones
- docs/glosario

FIN DE DECISIONES  DIA:15-ENE-2026  HORA: 1:25 pm


COMIENZO DE DECISIONES
DIA: 16-ENE-2026 — HORA: 3:35 pm

MÓDULO: NOMENCLADOR DE PLATOS — CIERRE DE FASE OPERATIVA

El Nomenclador de Platos queda habilitado para:

Alta

Edición

Borrado físico (en esta etapa operativa)

En esta fase NO se implementa:

Activar / Desactivar

Historial de cambios

Control contable
Estas reglas se reservan para fases posteriores.

Campos definitivos del Nomenclador de Platos en esta fase:

nombre (texto, obligatorio)

tipo (lista finita controlada)

peso_por_ración (float, siempre con 2 decimales)

UX de Captura:

No existe botón Guardar.

El guardado se realiza con ENTER en el último escaque.

ENTER avanza entre campos.

ESC limpia formulario y sale de modo edición.

El campo "tipo" NO se limpia al guardar ni al editar.

Formato del campo Peso por ración:

Siempre se muestra con dos decimales (ej: 240.00).

Al recibir foco, el valor completo se selecciona para reemplazo directo.

Al perder foco, se normaliza a dos decimales.

Visualización:

Tabla ordenada alfabéticamente por nombre.

Scroll interno en la tabla.

Carteles informativos en negrita y mismo tamaño:

"Se guarda con ENTER — ESC cancela"

"Peso por ración"

"gramos"

Arquitectura:

El Plato es solo entidad base.

No contiene ingredientes ni lógica de receta.

Será referenciado por la Receta MASTER por id.

ESTADO DEL MÓDULO:
Nomenclador de Platos aprobado para continuar con el siguiente módulo.

FIN DE DECISIONES
DIA: 16-ENE-2026 — HORA: 3:35 pm

## Líneas de evolución posteriores a la Fase XX

Con la base estable del MASTER de Recetas, se consideran como posibles extensiones futuras:

- 🔎 Búsqueda y/o filtrado de recetas por Plato en el listado.
- 📄 Pantalla de consulta rápida de recetas existentes sin entrar en edición.
- 🧭 Mejoras de navegación entre:
  - Captura de recetas
  - Listado de recetas
  - Detalle de receta

Estas mejoras se abordarán **sin romper** el flujo de captura ya estabilizado.

## Actualización de plan — MASTER de Recetas Web

El módulo MASTER de Recetas queda establecido con:

- Pantalla de Captura independiente.
- Pantalla de Listado independiente.
- Flujo de captura optimizado para teclado.
- Validaciones clave implementadas:
  - Raciones (> 0, entero).
  - Duplicidad de receta por Plato.
  - Duplicidad de ingredientes dentro de la receta.

A partir de este punto:
- Se prioriza no romper el flujo existente.
- Las nuevas funcionalidades (búsqueda, filtros, edición, etc.) se agregarán sobre esta base estable.
- Cualquier cambio debe respetar el comportamiento de ENTER, ESC y las validaciones actuales.






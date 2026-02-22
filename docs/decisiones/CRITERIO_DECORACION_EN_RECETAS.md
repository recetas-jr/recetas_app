# Decisión: Criterio de “Tiene decoración” en Recetas

**Fecha:** 2026-02-21  
**Contexto:** Sistema de Recetas Web — Master y Listado de Recetas

---

## 🧭 Contexto

En el sistema, algunos ingredientes pueden cumplir un **rol de decoración** dentro de una receta.  
Durante las pruebas se detectaron inconsistencias en el listado: recetas sin decoración aparecían marcadas como si la tuvieran.

Era necesario **definir un criterio único, simple y verificable** para determinar cuándo una receta **realmente** tiene decoración.

---

## ✅ Decisión

Se establece el siguiente **criterio único y oficial**:

> Una receta **tiene decoración** si y solo si **existe al menos un ingrediente con `rol > 0`**.

Implicaciones directas:

- Si **todos** los ingredientes tienen `rol = 0` → **La receta NO tiene decoración**.
- Si **al menos uno** tiene `rol > 0` → **La receta SÍ tiene decoración**.
- El valor `rol = 0` indica explícitamente: *el ingrediente no participa en decoración*.

---

## 🖥️ Representación en el Listado

- El listado de recetas:
  - Muestra el **icono/indicador de decoración** únicamente cuando se cumple `rol > 0` en algún ingrediente.
  - En caso contrario, **no debe** mostrar dicho indicador.
- Se acompaña con una **leyenda visual**: “Tiene decoración”.

---

## 🚫 Alcance y Restricciones

- Este criterio:
  - No depende del nombre del ingrediente.
  - No depende del plato.
  - No depende de metadatos externos.
- Depende **exclusivamente** del valor numérico del campo `rol` en `recetas_ingredientes`.

---

## 🎯 Consecuencias

- Se elimina la ambigüedad sobre qué es una receta “con decoración”.
- Se evitan falsos positivos en el listado.
- Se establece una **regla de negocio clara y comprobable** para futuras vistas, reportes o filtros.

---

## 📌 Notas de Implementación

- Las validaciones del Master aseguran:
  - `rol >= 0`
  - `rol <= cantidad`
- El cálculo de “tiene decoración” debe basarse en una consulta o agregación que verifique:
  - `MAX(rol) > 0` o `SUM(CASE WHEN rol > 0 THEN 1 ELSE 0 END) > 0`
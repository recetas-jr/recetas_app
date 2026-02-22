# Decisión: Ergonomía del Master de Recetas — Variante B + Barra de Acciones Sticky

**Fecha:** 2026-02-21  
**Contexto:** Sistema de Recetas Web — Módulo Master de Recetas

---

## 🧭 Contexto

El formulario **Master de Recetas** es la pantalla de trabajo principal del operador.  
Durante las pruebas de uso se detectó:

- Exceso de scroll vertical.
- Poca visibilidad de la parte inferior del formulario (ingredientes y acciones).
- Desaprovechamiento del ancho de pantalla.
- Necesidad de acceso rápido y permanente a las acciones principales.

Se evaluaron dos variantes de maquetación:

- **Variante A:** Una columna, más ancho y textareas más bajos.
- **Variante B:** Dos columnas para textos + reducción de altura de textareas.

---

## ✅ Decisión

Se adopta **Variante B** como diseño definitivo del Master de Recetas, con los siguientes cambios de UI:

1. **Textos en dos columnas:**
   - Columna izquierda: Preparación / Presentación  
   - Columna derecha: Elaboración / Nutrición  
   - Objetivo: aprovechar el ancho de pantalla y reducir scroll vertical.

2. **Textareas más bajos:**
   - Mantienen ancho completo de su columna.
   - Permiten que la zona de ingredientes y botones quede visible antes.

3. **Barra de acciones fija (sticky) en la parte superior derecha:**
   - Botones: `Guardar receta`, `Ir al Listado`, `Cancelar`.
   - Permanecen visibles al hacer scroll.
   - Mejora la velocidad de operación y reduce desplazamientos del cursor.

4. **Resaltado de foco en violeta claro:**
   - Para mejorar la orientación visual del operador durante la captura.

---

## 🚫 Alcance y Restricciones

- Esta decisión **solo afecta la presentación (UI/UX)**.
- **No** modifica:
  - Lógica de negocio
  - Validaciones
  - Persistencia en base de datos
  - Flujo funcional existente

El criterio es realizar cambios **ergonómicos y no disruptivos**.

---

## 🎯 Consecuencias

- Mejora significativa de la ergonomía y productividad del operador.
- Menor necesidad de scroll.
- Acciones principales siempre accesibles.
- Se establece un **estándar visual** para futuras pantallas de captura intensiva.

---

## 📌 Pendientes

- Ajuste fino del ancho del campo **Raciones base** para permitir 3 cifras con comodidad.
- Mantener consistencia visual en futuras pantallas administrativas.
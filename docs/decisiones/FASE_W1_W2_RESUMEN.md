# 🟦 Proyecto Recetas Web — Resumen Fase W1 y comienzo W2

## 📅 Fecha
Enero 2026

## 🎯 Objetivo de la Fase W1
Crear una versión web funcional de la app de recetas, usando Flask, con:
- listado de recetas
- vista de detalle por receta
- cálculo dinámico de raciones
- separación correcta entre backend y frontend

---

## ✅ Estado Actual del Proyecto

La aplicación web funciona correctamente con:

- Ruta principal:
  - `/` → listado de recetas

- Ruta de detalle:
  - `/receta/<id>` → ficha técnica de la receta

- Cálculo de raciones dinámico por formulario POST

---

## 🧱 Arquitectura Actual

### Backend (Flask)
Archivo:
- `web_app.py`

Responsabilidades:
- Cargar datos desde JSON
- Calcular factor de raciones
- Preparar lista de ingredientes calculados
- Enviar datos a los templates

NO contiene HTML embebido (se eliminó `html = """ ... """`).

---

### Templates (HTML)

Carpeta:
- `templates/`

Archivos:
- `index.html` → listado de recetas
- `receta_detalle.html` → vista detallada de receta

Se usa:
```python
render_template("index.html", recetas=recetas)
render_template("receta_detalle.html", receta=..., ingredientes=..., raciones=...)
Estilos (CSS)
Carpeta:

static/

Archivo:

styles.css

Contiene:

estilos generales de body

contenedor central .container

listas de ingredientes

botones

ajustes para hacer la vista más compacta

Se aplican mediante:

html
Copiar código
<link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
🧠 Decisiones Técnicas Importantes
Se eliminó el uso de render_template_string.

Todo el HTML vive únicamente en /templates.

Python solo contiene lógica y control de flujo.

Se usa JSON como fuente de datos de recetas publicadas.

Se mantiene debug=True durante desarrollo para recarga automática.

⚠️ Problemas Relevantes Resueltos
Error de rutas duplicadas (AssertionError: endpoint index already exists)

Error de indentación (IndentationError: unexpected unindent)

Mezcla de HTML en Python y templates (refactor completo)

Confusión por bloques html = """ sin uso

🚧 Inicio de Fase W2 — Interfaz y UX
Se comienza a trabajar en:

hacer la interfaz más compacta

reducir tamaños de fuente

mejorar presentación visual del listado de recetas

mejorar legibilidad de ingredientes y secciones

⏭️ Próximos Pasos Planificados
Rediseñar index.html con tarjetas de recetas (cards).

Mejorar secciones visuales en receta_detalle.html.

Refinar UX del selector de raciones.

Preparar estructura para despliegue futuro (hosting).

🧑‍🍳 Nota de Proyecto
El desarrollo se realiza paso a paso, con énfasis en:

comprensión de arquitectura

buenas prácticas

control total del flujo de la app

aprendizaje consciente, no solo copiar/pegar

yaml
Copiar código

---

# ✅ PASO 3 — GUARDA EL ARCHIVO

Ctrl + S ✔️

Ya tienes **bitácora técnica del proyecto**.  
Eso vale ORO en cualquier desarrollo.

---

# 🚀 PASO 4 — ABRIMOS NUEVA PESTAÑA

Ahora sí, nos mudamos a una conversación limpia y rápida.

### 🟦 Título de la nueva pestaña:
**VI — Recetas Web (UI & Estilos)**

### ✍️ Primer mensaje ahí:
Nueva pestaña abierta.
Estamos en Fase W2: ajustes visuales y UX.
Ya funciona Flask, rutas / y /receta/1.
Queremos hacer la interfaz más compacta y profesional.
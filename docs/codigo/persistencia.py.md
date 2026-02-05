# persistencia.py

## 1. Rol del archivo

`persistencia.py` centraliza **toda la lógica de persistencia** del sistema
**recetas_app**.

Es el **único módulo autorizado** a:
- definir rutas de archivos de datos
- leer archivos JSON
- escribir archivos JSON
- asegurar la existencia del directorio de datos

Ningún otro módulo debe acceder directamente al sistema de archivos.

---

## 2. Principios de diseño

- Fuente única de verdad para rutas
- Sin lógica de negocio
- Sin conocimiento del dominio (recetas, ingredientes, etc.)
- Reutilizable por cualquier módulo
- Diseño defensivo (archivos inexistentes no rompen el sistema)

---

## 3. Estructura de directorios

El módulo define y utiliza el directorio:

data/

yaml
Copiar código

Dentro de él se almacenan todos los archivos JSON del sistema:

- `recetas.json`
- `recetas_ingredientes.json`
- `ingredientes.json`
- `unidades.json`
- `config.json`

---

## 4. Constantes de rutas

El archivo define constantes para cada archivo de datos, por ejemplo:

- `RECETAS_FILE`
- `INGREDIENTES_FILE`
- `UNIDADES_FILE`
- `CONFIG_FILE`

Estas constantes se importan en otros módulos, evitando rutas duplicadas
o inconsistentes.

---

## 5. Funciones principales

### 5.1 `asegurar_directorio()`

- Verifica si existe el directorio `data/`
- Lo crea automáticamente si no existe
- Evita errores al guardar datos por primera vez

---

### 5.2 `cargar_datos(ruta, por_defecto)`

- Intenta cargar un archivo JSON
- Si el archivo no existe:
  - devuelve el valor `por_defecto`
- Garantiza que el sistema pueda arrancar sin datos previos

---

### 5.3 `guardar_datos(ruta, datos)`

- Asegura la existencia del directorio `data/`
- Escribe los datos en formato JSON
- Usa codificación UTF-8
- Aplica indentación para legibilidad
- No altera el contenido semántico de los datos

---

## 6. Manejo de errores

- Archivos inexistentes no generan excepción
- El sistema se comporta de forma predecible
- La validación de datos se delega a módulos de negocio

---

## 7. Alcance y límites

`persistencia.py`:
- NO valida reglas de negocio
- NO transforma datos
- NO conoce estados de recetas
- NO interactúa con el usuario

Su responsabilidad termina en **guardar y recuperar estructuras de datos**.

---

## 8. Estado actual

- Estable
- Cerrado
- Reutilizado por todos los módulos del sistema

Cualquier cambio en persistencia debe evaluarse cuidadosamente,
ya que impacta a todo el proyecto.
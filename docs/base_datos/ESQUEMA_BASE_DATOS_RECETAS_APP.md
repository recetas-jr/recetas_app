I - ESQUEMA BASE DE DATOS — SISTEMA RECETAS_APP
1. Propósito del documento

Este documento describe la estructura de datos del sistema recetas_app.

Su objetivo es documentar:

las fuentes de datos del sistema

la estructura de los archivos de datos

la relación entre entidades

las reglas de integridad

El sistema actualmente utiliza archivos JSON como mecanismo de persistencia.

Los datos se almacenan en:

data_compartida/data/
2. Arquitectura general de datos

El sistema se basa en tres entidades principales:

RECETAS
INGREDIENTES
UNIDADES DE MEDIDA

Relación conceptual:

RECETA
   │
   │ 1
   │
   └──────────────∞
        INGREDIENTE_EN_RECETA
                │
                │
                ▼
            INGREDIENTE

Una receta puede tener múltiples ingredientes.

Cada ingrediente dentro de una receta tiene:

cantidad

unidad de medida

3. Ubicación de los datos

Los datos del sistema se encuentran en:

data_compartida/data/

Archivos principales:

recetas.json
recetas_maestro.json
unidades.json

Archivos auxiliares:

recetas_catalogo.json
recetas_detalle_version.json
recetas_ingredientes.json
recetas_ingredientes_v2.json
4. Archivo recetas_maestro.json

Este archivo contiene la lista principal de recetas del sistema.

Cada registro representa una receta.

Campos principales
id
nombre
descripcion
categoria
raciones_base
Ejemplo conceptual
{
  "id": 1,
  "nombre": "Arroz con pollo",
  "descripcion": "Receta tradicional",
  "categoria": "Plato principal",
  "raciones_base": 4
}
5. Archivo recetas_ingredientes.json

Este archivo define los ingredientes asociados a cada receta.

Representa la relación entre recetas e ingredientes.

Campos principales
receta_id
ingrediente
cantidad
unidad
Ejemplo conceptual
{
  "receta_id": 1,
  "ingrediente": "arroz",
  "cantidad": 200,
  "unidad": "g"
}
6. Archivo unidades.json

Este archivo contiene el nomenclador de unidades de medida.

Ejemplos:

g
kg
ml
l
taza
cucharada
Campos típicos
codigo
descripcion

Ejemplo conceptual:

{
  "codigo": "g",
  "descripcion": "gramos"
}
7. Integridad de datos

El sistema aplica las siguientes reglas de integridad:

Recetas

cada receta debe tener un id único

el nombre no debe estar vacío

Ingredientes en receta

cantidad > 0

unidad válida

ingrediente válido

Unidades

códigos únicos

descripción obligatoria

8. Relaciones entre datos

Relaciones principales:

recetas.json
      │
      │ receta_id
      ▼
recetas_ingredientes.json

Cada registro en recetas_ingredientes.json pertenece a una receta existente.

9. Evolución del modelo de datos

El sistema ha evolucionado desde una estructura inicial simple hacia una estructura más organizada.

Archivos históricos:

recetas_ingredientes.json
recetas_ingredientes_v2.json

Estos reflejan etapas de evolución del modelo de datos.

10. Consideraciones arquitectónicas

Actualmente el sistema utiliza JSON como almacenamiento principal.

Ventajas:

simplicidad

facilidad de edición

portabilidad

Limitaciones:

falta de transacciones

control limitado de integridad

escalabilidad reducida

11. Futuras mejoras

Posibles evoluciones del sistema:

migración a SQLite

control de integridad referencial

versionado de datos

validaciones más robustas

12. Documento relacionado

Este documento se relaciona con:

MAPA_ARQUITECTONICO_RECETAS_APP.md
SUPER_MAPA_ARQUITECTONICO_RECETAS_APP.md
MAPA_DE_SEGURIDAD_RECETAS_APP.md
13. Estado del documento
Documento activo
Parte de la documentación arquitectónica del sistema recetas_app
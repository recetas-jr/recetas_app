FASE DEL PROYECTO — CAPA DE USUARIO
Proyecto
recetas_app
Estado del sistema al iniciar esta fase

MASTER DE RECETAS ESTABLE

Nomencladores completamente blindados:

Tipos de Plato

Unidades de Medida

Ingredientes

Platos

Validaciones frontend y backend coherentes.

Integridad referencial activa.

Mensajes institucionales normalizados.

Flujo UX consistente en todos los módulos administrativos.

El sistema permite actualmente:

crear recetas

validar recetas

listar recetas

proteger integridad de datos

El módulo MASTER ha sido probado y estabilizado.

Documentación del sistema disponible

El proyecto cuenta con documentación estructural completa.

Ubicada en:

docs/

Documentos principales:

docs/START_HERE.md
docs/MAPA_DEL_SISTEMA.md
docs/ARQUITECTURA_DEL_SISTEMA.md
docs/INDICE_DOCUMENTACION.md

Documentación técnica adicional:

docs/arquitectura/
docs/base_datos/
docs/operacion/
docs/decisiones/

La arquitectura del sistema está completamente documentada.

Objetivo de esta fase

Construir la interfaz de usuario del sistema de recetas.

Esta capa permitirá a los usuarios:

consultar recetas

visualizar ingredientes

leer preparación y elaboración

navegar recetas por diferentes criterios

Principio arquitectónico de esta fase

Separación clara entre:

ADMINISTRACIÓN
USUARIO

Administración:

/admin/*

Permite:

crear datos

modificar datos

validar datos

Usuario:

/recetas

Permite únicamente:

consultar datos

La capa de usuario no modifica la base de datos.

Restricciones técnicas

Durante esta fase NO se permite:

Modificar tablas de base de datos.

Modificar validaciones del MASTER.

Modificar nomencladores.

Modificar lógica de negocio del sistema.

La capa de usuario solo realiza lectura de datos.

Primera funcionalidad a implementar

Listado público de recetas.

Ruta prevista:

/recetas

Mostrará una tabla con:

Receta
Tipo de Plato
Ración Base
Cantidad de Ingredientes

Desde este listado el usuario podrá acceder a:

/receta/<id>

donde se mostrará el detalle completo de la receta.

Funcionalidades previstas en la capa de usuario

Visualización de receta completa.

Escalado de receta según número de raciones.

Consulta de recetas por ingrediente.

Consulta de recetas por múltiples ingredientes.

Conversión automática de unidades en cantidades grandes.

Principio de evolución del sistema

La capa de usuario se desarrollará de forma incremental.

Cada funcionalidad deberá:

ser pequeña

ser probada inmediatamente

no afectar el MASTER

Cada avance estable será registrado en Git.

Estado del sistema al iniciar la fase

Sistema completamente funcional en modo administración.

Documentación estructural completa.

Repositorio Git limpio.

Respaldo físico del proyecto realizado.

Punto de inicio de esta fase

Rama activa:

fase-ingredientes-blindaje

Base estable del sistema:

master-ui-final-estable

Tag relevante:

DOCS_BASE_ESTABLE
Próximo paso inmediato

Construcción de la primera ruta pública:

/recetas

FIN DEL DOCUMENTO
Ruta: docs/operacion/FASE_CAPA_USUARIO.md
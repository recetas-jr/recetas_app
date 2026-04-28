V-MAPA DE SEGURIDAD DEL SISTEMA — RECETAS_APP
1. Propósito del documento
Este documento define los componentes críticos del sistema recetas_app y establece las reglas que permiten proteger su integridad.
El objetivo principal del mapa de seguridad es identificar:
los elementos fundamentales del sistema
las áreas sensibles de la arquitectura
los componentes que no deben modificarse sin análisis previo
Este documento forma parte de la arquitectura de protección del sistema.
2. Núcleo crítico del sistema
El sistema recetas_app se basa en tres componentes fundamentales.
RECETASINGREDIENTESRELACION RECETA–INGREDIENTES
Estos tres elementos constituyen el núcleo funcional del sistema.
La relación conceptual es la siguiente:
RECETA │ │ 1 │ └──────────────∞ INGREDIENTE_EN_RECETA
Si esta relación se rompe, el sistema pierde coherencia.
3. Componentes críticos del sistema
Los siguientes elementos se consideran críticos.
Recetas
Las recetas constituyen la entidad principal del sistema.
Cada receta contiene:
nombre
descripción
categoría
raciones base
Las recetas se almacenan en archivos de datos del sistema.
Ingredientes
Los ingredientes representan los elementos que componen una receta.
Cada ingrediente posee:
nombre
cantidad
unidad de medida
Los ingredientes se relacionan con las recetas mediante archivos de datos específicos.
Unidades de medida
Las unidades permiten expresar las cantidades de ingredientes.
Ejemplos de unidades:
gkgmlltazacucharada
Estas unidades forman parte del nomenclador del sistema.
4. Zonas de seguridad del sistema
El sistema puede dividirse en tres zonas de seguridad.
Zona crítica
Corresponde a los componentes esenciales del sistema.
Incluye:
archivos de datos principales
relaciones entre recetas e ingredientes
nomencladores de unidades
Las modificaciones en esta zona deben realizarse con extremo cuidado.
Zona lógica
Incluye la lógica de funcionamiento del sistema.
En esta zona se encuentran:
funciones de gestión de recetas
control de ingredientes
validaciones
Las modificaciones en esta zona requieren pruebas previas.
Zona de interfaz
Corresponde a la interfaz web del sistema.
Incluye:
formularios
visualización de datos
interacción con el usuario
Las modificaciones en esta zona presentan menor riesgo estructural.
5. Reglas de seguridad arquitectónica
Para mantener la estabilidad del sistema se aplican las siguientes reglas.
No modificar la estructura de los archivos de datos sin análisis previo.
No eliminar relaciones entre recetas e ingredientes.
Mantener la coherencia entre ingredientes y unidades.
Verificar validaciones antes de guardar datos.
Estas reglas ayudan a prevenir errores estructurales.
6. Riesgos principales del sistema
Los principales riesgos identificados son:
pérdida de relación entre recetas e ingredientes
inconsistencias en cantidades o unidades
eliminación accidental de recetas
La documentación y las validaciones ayudan a mitigar estos riesgos.
7. Importancia del mapa de seguridad
El mapa de seguridad permite:
identificar los elementos críticos del sistema
prevenir modificaciones peligrosas
mantener la estabilidad del sistema
facilitar el mantenimiento futuro
Este documento actúa como una guía de protección arquitectónica del sistema recetas_app.
docs/arquitectura/MAPA_DE_SEGURIDAD_RECETAS_APP.md

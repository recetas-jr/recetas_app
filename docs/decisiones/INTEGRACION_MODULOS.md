📁 docs/decisiones/INTEGRACION_MODULOS.md
Integración entre módulos
Regla general

Cada módulo cumple una sola responsabilidad.

main.py

Muestra menú

Orquesta navegación

No contiene lógica de negocio

recetas_raciones.py

Contiene toda la lógica del cálculo

No escribe archivos

Expone una función pública:

ejecutar_calculo_raciones()

Regla de dependencias

main.py puede importar módulos

Los módulos no deben importarse entre sí de forma circular
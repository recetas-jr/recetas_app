"""
==========================================================
ARQUITECTURA DINÁMICA
==========================================================

Proyecto:
    recetas_app

Versión:
    1.0

Estado:
    En construcción

==========================================================
"""

OBJETIVO

La Arquitectura Dinámica documenta el recorrido real que
siguen los datos durante la ejecución de recetas_app.

Su propósito es permitir comprender, mantener, depurar y
evolucionar el sistema siguiendo el comportamiento de los
datos, y no únicamente la organización del código fuente.

==========================================================
ALCANCE
==========================================================

La Arquitectura Dinámica documenta exclusivamente el
comportamiento funcional del sistema durante su ejecución.

No sustituye la documentación técnica existente ni la
documentación del código fuente.

Su alcance comprende los flujos funcionales que recorren
los datos desde un evento disparador hasta un resultado
verificable.

Cada flujo constituye una unidad independiente de
documentación y puede evolucionar sin afectar la
documentación de los demás flujos.

==========================================================
CONVENCIONES GENERALES
==========================================================

La Arquitectura Dinámica se organiza por FLUJOS.

Cada flujo representa un proceso funcional completo del
sistema.

Cada flujo se identifica mediante un código único.

Ejemplos:

    F-ED-001   Edición de Recetas

    F-NR-001   Nueva Receta

    F-CNV-001  Motor de Conversión

Cada flujo se desarrolla mediante una secuencia ordenada
de EVENTOS.

Los eventos representan cambios verificables en el estado
del sistema durante la ejecución de un flujo.

La documentación sigue el recorrido real de los datos.

Nunca el recorrido de los archivos.

==========================================================
ESTRUCTURA OFICIAL DE UN FLUJO
==========================================================

Todo flujo documentado dentro de la Arquitectura Dinámica
deberá utilizar la siguiente estructura:

1. Identificación

2. Objetivo

3. Evento disparador

4. Resultado esperado

5. Componentes participantes

6. Mapa general del flujo

7. Desarrollo de los eventos

8. Instrumentación (Ratoneras)

9. Observaciones

10. Historial de modificaciones

==========================================================
F-ED-001
EDICIÓN DE RECETAS
==========================================================

Estado

    En construcción.

Descripción

    Este flujo documenta el recorrido completo de los datos
    durante la modificación de una receta existente, desde
    que el usuario abre la pantalla de edición hasta que la
    información queda almacenada correctamente en la base
    de datos.

Fases

    Fase I   Preparación del formulario

    Fase II  Captura de modificaciones

    Fase III Envío del formulario

    Fase IV  Procesamiento en Flask

    Fase V   Persistencia

    Fase VI  Finalización
    
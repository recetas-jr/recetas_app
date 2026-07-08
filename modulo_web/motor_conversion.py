"""
==========================================================
MOTOR DE CONVERSIÓN DE UNIDADES
==========================================================

Proyecto:
    recetas_app

Propósito:
    Implementar el Motor de Conversión de Unidades utilizado
    por recetas_app.

Filosofía:

    El Motor no administra información.

    El Motor no modifica datos.

    El Motor responde consultas realizadas por otros módulos
    del sistema.

    La base de datos conserva la representación canónica.

    El Motor decide cómo expresar dicha información utilizando
    otras unidades.

Consumidores previstos:

    - Visualización de recetas
    - Impresión
    - Exportaciones
    - Listas de compra
    - Costos
    - Nutrición
    - API futura

Estado:
    En construcción.

==========================================================
"""
# ==========================================================
# IMPORTACIONES
# ==========================================================
from modulo_web.persistencia_db import db_cargar_equivalencias

# ==========================================================
# EXCEPCIONES DEL MOTOR
# ==========================================================


class ErrorConversion(Exception):
    """
    Excepción base del Motor de Conversión.
    """
    pass


class IngredienteSinEquivalencias(ErrorConversion):
    """
    El ingrediente no posee equivalencias registradas.
    """
    pass


class UnidadOrigenNoEncontrada(ErrorConversion):
    """
    La unidad de origen no existe entre las equivalencias
    del ingrediente.
    """
    pass


class UnidadDestinoNoEncontrada(ErrorConversion):
    """
    La unidad de destino no existe entre las equivalencias
    del ingrediente.
    """
    pass

# ==========================================================
# API PÚBLICA DEL MOTOR
# ==========================================================

# Servicios públicos:
#
# - puede_convertir()
# - obtener_equivalencias()
# - obtener_unidades_disponibles()
# - convertir()

# Funciones privadas previstas:
#
# - _buscar_equivalencia()

# Función principal prevista:
#
# convertir(
#     ingrediente_id,
#     cantidad,
#     unidad_origen,
#     unidad_destino
# )

# Flujo general previsto:
#
# 1. Validar parámetros.
# 2. Cargar equivalencias.
# 3. Verificar si existen equivalencias.
# 4. Localizar unidad de origen.
# 5. Localizar unidad destino.
# 6. Calcular conversión.
# 7. Devolver cantidad convertida.


def puede_convertir(ingrediente_id):
    """
    Indica si un ingrediente dispone de
    equivalencias registradas.
    """
    equivalencias = db_cargar_equivalencias(ingrediente_id)

    return len(equivalencias) > 0


def obtener_equivalencias(ingrediente_id):
    """
    Obtiene las equivalencias registradas para un ingrediente.
    """
    equivalencias = db_cargar_equivalencias(ingrediente_id)

    if not equivalencias:
        raise IngredienteSinEquivalencias

    return equivalencias


def obtener_unidades_disponibles(ingrediente_id):
    """
    Obtiene las unidades disponibles para un ingrediente.
    """
    equivalencias = obtener_equivalencias(ingrediente_id)

    unidades = []

    for equivalencia in equivalencias:
        unidades.append({
            "codigo": equivalencia["codigo"],
            "nombre": equivalencia["nombre"]
        })

    return unidades


def convertir(
    ingrediente_id,
    cantidad,
    unidad_origen,
    unidad_destino
):
    """
    Convierte una cantidad de un ingrediente desde una
    unidad de origen hacia una unidad de destino.

    La conversión se realiza utilizando la unidad
    canónica del ingrediente como punto de referencia.
    """
    # Obtener las equivalencias registradas para el ingrediente.
    equivalencias = obtener_equivalencias(ingrediente_id)

    # Localizar la equivalencia de la unidad de origen.

    equivalencia_origen = _buscar_equivalencia(
        equivalencias,
        unidad_origen
    )

    if equivalencia_origen is None:
        raise UnidadOrigenNoEncontrada

    # Localizar la equivalencia de la unidad de destino.

    equivalencia_destino = _buscar_equivalencia(
        equivalencias,
        unidad_destino
    )

    if equivalencia_destino is None:
        raise UnidadDestinoNoEncontrada

    cantidad_canonica = (
        cantidad *
        equivalencia_origen["factor"]
    )

    cantidad_convertida = (
        cantidad_canonica /
        equivalencia_destino["factor"]
    )

    return cantidad_convertida


def _buscar_equivalencia(equivalencias, unidad):
    """
    Localiza la equivalencia correspondiente a una unidad
    dentro del conjunto de equivalencias del ingrediente.
    """
    for equivalencia in equivalencias:
        if equivalencia["codigo"] == unidad:
            return equivalencia

    return None

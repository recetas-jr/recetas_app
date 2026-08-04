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
from modulo_web.persistencia_db import (
    db_cargar_equivalencias,
    db_cargar_ingrediente_por_id
)

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

# Servicios públicos previstos:
#
# - puede_convertir()
#       Indica si el ingrediente posee equivalencias registradas.
#
# - obtener_equivalencias()
#       Devuelve las equivalencias del ingrediente.
#
# - obtener_unidades_disponibles()
#       Devuelve las unidades en las que el ingrediente puede representarse.
#
# - representar()
#       Recibe una cantidad expresada en la unidad canónica del ingrediente
#       y la representa en la unidad solicitada.
#
# - normalizar()
#       Recibe una cantidad expresada en cualquier unidad válida del
#       ingrediente y devuelve su representación en la unidad canónica.
#
# Flujo conceptual:
#
# Captura del usuario
#          │
#          ▼
#   normalizar()
#          │
#          ▼
# Cantidad canónica
#          │
#          ▼
# Persistencia
#          │
#          ▼
# representar()
#          │
#          ▼
# Visualización al usuario


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
    Obtiene las unidades disponibles para representar un
    ingrediente.

    Esta función no realiza conversiones.

    Su propósito es informar a los consumidores del Motor
    cuáles unidades pueden utilizarse posteriormente mediante
    representar() o normalizar().
    """
    equivalencias = obtener_equivalencias(ingrediente_id)

    unidades = []

    for equivalencia in equivalencias:
        unidades.append({
            "codigo": equivalencia["codigo"],
            "nombre": equivalencia["nombre"]
        })

    return unidades


def representar(
    ingrediente_id,
    cantidad,
    unidad_origen,
    unidad_destino
):
    """
    Representa una cantidad de un ingrediente desde su
    unidad canónica hacia una unidad de visualización.

    La cantidad recibida ya se encuentra expresada en la
    unidad canónica del ingrediente.
    """
    # Obtener las equivalencias registradas para el ingrediente.
    equivalencias = obtener_equivalencias(ingrediente_id)

    # La cantidad recibida debe encontrarse expresada
    # en la unidad canónica del ingrediente.

    cantidad_canonica = cantidad

    # Localizar la equivalencia de la unidad de destino.

    # Si la representación solicitada es la unidad
    # canónica, no es necesario convertir.

    if unidad_destino == unidad_origen:
        return cantidad_canonica

    # Localizar la equivalencia de la unidad de destino.

    equivalencia_destino = _buscar_equivalencia(
        equivalencias,
        unidad_destino
    )

    if equivalencia_destino is None:
        raise UnidadDestinoNoEncontrada

    cantidad_convertida = (
        cantidad_canonica /
        equivalencia_destino["factor"]
    )

    return cantidad_convertida


def convertir(  # Compatibilidad temporal (DEPRECATED)
    ingrediente_id,
    cantidad,
    unidad_origen,
    unidad_destino
):
    """
    Función mantenida temporalmente por compatibilidad.

    DEPRECATED.
    Utilizar representar().
    """

    return representar(
        ingrediente_id,
        cantidad,
        unidad_origen,
        unidad_destino
    )


def normalizar(
    ingrediente_id,
    cantidad,
    unidad_origen
):
    """
    Convierte una cantidad expresada en cualquier unidad válida
    del ingrediente hacia su unidad canónica.
    """

    ingrediente = db_cargar_ingrediente_por_id(
        ingrediente_id
    )

    if (
        ingrediente is not None
        and
        ingrediente["unidad_codigo"].upper() == unidad_origen.upper()
    ):
        return cantidad

    equivalencias = obtener_equivalencias(ingrediente_id)

    equivalencia_origen = _buscar_equivalencia(
        equivalencias,
        unidad_origen
    )

    if equivalencia_origen is None:
        raise UnidadOrigenNoEncontrada

    cantidad_canonica = (
        cantidad *
        equivalencia_origen["factor"]
    )

    return cantidad_canonica


def _buscar_equivalencia(equivalencias, unidad):
    """
    Localiza la equivalencia correspondiente a una unidad
    dentro del conjunto de equivalencias del ingrediente.
    """
    for equivalencia in equivalencias:

        print(
            "COMPARANDO:",
            equivalencia["codigo"],
            "==",
            unidad
        )

        if equivalencia["codigo"].upper() == unidad.upper():

            print("COINCIDENCIA ENCONTRADA")

            return equivalencia

    return None

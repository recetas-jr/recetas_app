print("🔥 ESTE ES EL EXPORTADOR CORRECTO 🔥")

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data_compartida", "data")
WEB_DIR = os.path.join(BASE_DIR, "web_data")

# -------------------------
# ARCHIVOS FUENTE
# -------------------------
CATALOGO_FILE = os.path.join(DATA_DIR, "recetas_catalogo.json")
MAESTRO_FILE = os.path.join(DATA_DIR, "recetas_maestro.json")
ING_REL_FILE = os.path.join(DATA_DIR, "recetas_ingredientes.json")
DETALLE_FILE = os.path.join(DATA_DIR, "recetas_detalle_version.json")
ING_FILE = os.path.join(DATA_DIR, "ingredientes.json")
UM_FILE = os.path.join(DATA_DIR, "unidades.json")

# -------------------------
# ARCHIVO DESTINO
# -------------------------
WEB_FILE = os.path.join(WEB_DIR, "recetas_publicadas.json")


def cargar(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def exportar():
    print("📤 Exportando recetas para la web...")

    catalogo = cargar(CATALOGO_FILE)
    maestro = cargar(MAESTRO_FILE)
    relaciones = cargar(ING_REL_FILE)
    detalles = cargar(DETALLE_FILE)
    ingredientes = cargar(ING_FILE)
    unidades = cargar(UM_FILE)

    # --- solo versiones activas
    versiones_activas = [v for v in maestro if v.get("estado") == "activa"]

    print("MAESTRO:", maestro)
    print("VERSIONES ACTIVAS:", versiones_activas)

    publicadas = []

    for v in versiones_activas:

    


        receta_id = v["receta_id"]
        receta_maestro_id = v["id"]

        plato = next((c for c in catalogo if c["id"] == receta_id), None)
        if not plato:
            continue

        # --- ingredientes de esta versión
        rel_ver = [
            r for r in relaciones
            if r.get("receta_maestro_id") == receta_maestro_id
               or r.get("receta_id") == receta_id
        ]

        print("RELACIONES:", rel_ver)
        if not rel_ver:
            print(f"⚠ Omitida (sin ingredientes): {plato['nombre']}")
            continue

        ingredientes_web = []

        for r in rel_ver:
            ing = next((i for i in ingredientes if i["id"] == r["ingrediente_id"]), None)
            um = next((u for u in unidades if u["id"] == r["unidad_id"]), None)

            if not ing or not um:
                continue

            ingredientes_web.append({
                "nombre": ing.get("descripcion") or ing.get("nombre"),
                "cantidad": r["cantidad"],
                "unidad": um.get("simbolo") or um.get("codigo") or um.get("nombre"),
                "rol": r.get("uso", "principal")
            })

        # --- detalle (preparación y nutrición)
        det = next(
            (d for d in detalles if d["receta_maestro_id"] == receta_maestro_id),
            None
        )

        print("DETALLE:", det)
        if not det or not det.get("preparacion"):
            print(f"⚠ Omitida (sin preparación): {plato['nombre']}")
            continue

        receta_web = {
            "id": receta_maestro_id,
            "nombre": plato["nombre"],
            "tipo_plato": plato.get("tipo_plato", ""),
            "raciones_base": v["raciones_base"],
            "ingredientes": ingredientes_web,
            "preparacion": det.get("preparacion", ""),
            "presentacion": det.get("presentacion", ""),
            "nutricion": {
                "proteinas": det.get("proteinas"),
                "carbohidratos": det.get("carbohidratos"),
                "grasas": det.get("grasas"),
                "fibra": det.get("fibra"),
                "sodio": det.get("sodio"),
                "comentario": det.get("comentario", "")
            }
        }

        publicadas.append(receta_web)

    guardar(WEB_FILE, publicadas)

    print("✅ Exportación terminada")
    print(f"   Recetas publicadas: {len(publicadas)}")
    print(f"   Archivo: {WEB_FILE}")


if __name__ == "__main__":
    exportar()
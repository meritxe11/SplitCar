import os
import json
import uuid
from datetime import date

DATA_FILE_PATH = "data/data.json"

def ensure_data_file(path=DATA_FILE_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({"cars": {}}, f, indent=2)
    return path

def load_data(path=DATA_FILE_PATH):
    with open(path, "r") as f:
        return json.load(f)

def save_data(data, path=DATA_FILE_PATH):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def generate_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def add_car(data, nom, emoji="🚗"):
    car_id = generate_id("car")
    data["cars"][car_id] = {
        "id": car_id,
        "nom": nom,
        "emoji": emoji,
        "usuaris": [],
        "despeses": [],
        "usos": [],
        "historial": []
    }
    return data, car_id

def add_user_to_car(data, car_id, nom):
    usuari_id = generate_id("u")
    car = data["cars"][car_id]
    car["usuaris"].append({"id": usuari_id, "nom": nom})
    return data, usuari_id

def add_despesa(data, car_id, usuari_nom, import_, descripcio, data_d=None):
    if data_d is None:
        data_d = date.today().isoformat()
    despesa_id = generate_id("d")
    data["cars"][car_id]["despeses"].append({
        "id": despesa_id,
        "usuari": usuari_nom,  # ← guardem el nom directament
        "import": import_,
        "descripcio": descripcio,
        "data": data_d
    })
    return data


def add_usu(data, car_id, usuari_nom, km_, descripcio, data_u=None):
    if data_u is None:
        data_u = date.today().isoformat()
    usu_id = generate_id("km")
    data["cars"][car_id]["usos"].append({
        "id": usu_id,
        "usuari": usuari_nom,
        "km": km_,
        "descripcio": descripcio,
        "data": data_u
    })
    return data

def calcular_balanc(despeses, usos, usuaris=None):
    total_despesa = sum(d["import"] for d in despeses)
    total_km = sum(u["km"] for u in usos) or 1  # evitar divisió per zero

    # Calcular km fets per cada usuari
    km_per_persona = {}
    for u in usos:
        km_per_persona[u["usuari"]] = km_per_persona.get(u["usuari"], 0) + u["km"]

    # Calcular % de km
    percentatge_km = {k: v / total_km for k, v in km_per_persona.items()}

    # Calcular quant hauria de pagar segons % km
    hauria_de_pagar = {k: round(p * total_despesa, 2) for k, p in percentatge_km.items()}

    # Calcular quant ha pagat
    ha_pagado = {}
    for d in despeses:
        ha_pagado[d["usuari"]] = ha_pagado.get(d["usuari"], 0) + d["import"]

    # Si passem llista d'usuaris, forcem que apareguin encara que tinguin 0
    totes_les_persones = set(km_per_persona.keys()) | set(ha_pagado.keys())
    if usuaris:
        totes_les_persones |= set([u["nom"] for u in usuaris])

    resum_per_usuari = []
    for p in sorted(totes_les_persones):
        km = km_per_persona.get(p, 0)
        percent = round((km / total_km) * 100, 2)
        pagat = round(ha_pagado.get(p, 0), 2)
        hauria = round(hauria_de_pagar.get(p, 0), 2)
        resum_per_usuari.append({
            "usuari": p,
            "km_fets": km,
            "percentatge_km": percent,
            "ha_pagat": pagat,
            "hauria_de_pagar": hauria,
            "diferencia": round(pagat - hauria, 2)
        })

    resum_general = {
        "total_despesa": round(total_despesa, 2),
        "total_km": total_km
    }

    return resum_general, resum_per_usuari


def tancar_periode(data, car_id):
    car = data["cars"][car_id]
    balanc = calcular_balanc(car["despeses"], car["usos"])
    history_entry = {
        "id": generate_id("h"),
        "data": date.today().isoformat(),
        "balanc": balanc
    }
    car["historial"].append(history_entry)
    car["despeses"] = []
    car["usos"] = []
    return data
import pickle
import pandas as pd
import json

with open('logic/modelo_ia_automotriz.pkl', 'rb') as f:
    modelo = pickle.load(f)

columnas = [
    "humo_negro", "humo_blanco", "humo_azul", "fuga_aceite", "fuga_refrigerante",
    "fuga_frenos", "fuga_combustible", "golpeteo_metalico", "silbido_turbo",
    "chirrido_correa", "clack_giro", "zumbido_rodamiento", "perdida_potencia",
    "tirones_aceleracion", "ralenti_inestable", "no_arranca", "se_cala_solo",
    "vibracion_volante", "pedal_freno_blando", "direccion_dura", "cambio_marchas_duro",
    "sobrecalentamiento", "aguja_temperatura_baja", "luz_check_engine", "luz_abs",
    "luz_bateria", "luz_aceite", "luz_airbag", "olor_quemado", "olor_combustible",
    "chirrido_frenos", "traqueteo_motor"
]

caso = pd.DataFrame([[
    1, 0, 0, 0, 0,
    0, 0, 0, 1,
    0, 0, 0, 1,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 0, 0,
    0, 0
]], columns=columnas)

pred = int(modelo.predict(caso)[0])

resultado = {
    "prediccion_principal": pred,
    "top3": []
}

if hasattr(modelo, "predict_proba"):
    proba = modelo.predict_proba(caso)[0]
    clases = modelo.classes_
    top = sorted(zip(clases, proba), key=lambda x: x[1], reverse=True)[:3]
    for clase, p in top:
        resultado["top3"].append({
            "codigo": int(clase),
            "probabilidad": round(float(p) * 100, 2)
        })

print(json.dumps(resultado, ensure_ascii=False, indent=2))
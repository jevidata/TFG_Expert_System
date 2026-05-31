from flask import Flask, request, jsonify
from sklearn.tree import DecisionTreeClassifier
import pickle
import os

app = Flask(__name__)

# 🔹 LISTA EXACTA DE 73 COLUMNAS (Debe coincidir 1:1 con el dataset de entrenamiento)
COLUMNAS = [
    "humo_negro", "humo_blanco", "humo_azul", "fuga_aceite", "fuga_refrigerante",
    "fuga_frenos", "fuga_combustible", "golpeteo_metalico", "silbido_turbo",
    "chirrido_correa", "clack_giro", "zumbido_rodamiento", "perdida_potencia",
    "tirones_aceleracion", "ralenti_inestable", "no_arranca", "se_cala_solo",
    "vibracion_volante", "pedal_freno_blando", "direccion_dura", "cambio_marchas_duro",
    "sobrecalentamiento", "aguja_temperatura_baja", "luz_check_engine", "luz_abs",
    "luz_bateria", "luz_aceite", "luz_airbag", "olor_quemado", "olor_combustible",
    "chirrido_frenos", "traqueteo_motor", "consumo_elevado", "consumo_aceite",
    "arranque_lento", "ruido_metalico", "ruido_escape", "suspension_ruidosa",
    "embrague_patina", "AC_no_enfria", "vibracion_aceleracion", "ruido_direccion",
    "ruido_embrague", "fuga_liquido", "silbido_freno", "clic_giro", "asistencia_intermitente",
    "bateria_sobrecarga", "ruido_ventilador", "pedal_freno_duro", "luz_direccion",
    "codigo_error", "freno_tira", "correa_ruido", "ruido_bomba", "freno_asistencia_baja",
    "juego_rueda", "testigo_parpadea", "silbido_admision", "testigo_seguridad",
    "sin_flujo_aire", "pedal_freno_vibracion", "calor_rueda", "manchas_aceite",
    "componente_no_funciona", "circuito_muerto", "ruido_electrico", "presion_baja",
    "liquido_direccion_bajo", "luces_parpadean", "juego_volante", "luz_testigo_temperatura",
    "ruido_compresor"
]

# Cargar el modelo entrenado
print("🤖 Cargando modelo de IA (73 features)...")
ruta_modelo = os.path.join(os.path.dirname(__file__), "..", "logic", "modelo_ia_automotriz.pkl")
with open(ruta_modelo, "rb") as f:
    modelo = pickle.load(f)
print("✅ Modelo cargado correctamente")

@app.route("/predecir", methods=["POST"])
def predecir():
    try:
        datos = request.json
        
        # 🔹 Binarizar síntomas de entrada (rellena con 0 lo que no venga en el JSON)
        vector_entrada = [1 if datos.get(col, 0) == 1 else 0 for col in COLUMNAS]
        
        # Predecir probabilidad
        probabilidades = modelo.predict_proba([vector_entrada])[0]
        clases = modelo.classes_
        
        # Obtener Top 3
        indices_top3 = probabilidades.argsort()[-3:][::-1]
        top3 = []
        for idx in indices_top3:
            if probabilidades[idx] > 0:
                top3.append({
                    "codigo_averia": int(clases[idx]),
                    "probabilidad": round(probabilidades[idx] * 100, 2)
                })
        
        return jsonify({
            "prediccion_principal": top3[0] if top3 else None,
            "top3": top3,
            "mensaje": "Diagnóstico generado correctamente"
        })
        
    except Exception as e:
        print(f" Error en API: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 API Flask iniciada en http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
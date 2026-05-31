import pandas as pd
import numpy as np
import random

# Definimos las familias de averías y sus síntomas lógicos
familias = {
    "100": {"nombre": "Inyeccion", "sintomas": ["tirones_aceleracion", "luz_check_engine", "olor_combustible"]},
    "200": {"nombre": "Turbo", "sintomas": ["silbido_turbo", "perdida_potencia", "humo_negro"]},
    "300": {"nombre": "Refrigeracion", "sintomas": ["sobrecalentamiento", "humo_blanco", "fuga_refrigerante"]},
    "400": {"nombre": "Encendido", "sintomas": ["no_arranca", "luz_bateria", "traqueteo_motor"]},
    "500": {"nombre": "Frenos", "sintomas": ["pedal_freno_blando", "luz_abs", "chirrido_frenos"]}
}

# Lista completa de columnas (32 síntomas)
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

data = []

# Generamos 5.000 registros
for _ in range(5000):
    cod_familia = random.choice(list(familias.keys()))
    info = familias[cod_familia]
    
    fila = {col: 0 for col in columnas}
    
    # Corregido: 'in' en lugar de 'en'
    for s in info["sintomas"]:
        if random.random() < 0.8:
            fila[s] = 1
            
    if random.random() < 0.2:
        fila[random.choice(columnas)] = 1
        
    fila["codigo_averia"] = int(cod_familia) + random.randint(1, 20)
    data.append(fila)

df = pd.DataFrame(data)
# Lo guardamos directamente en la carpeta data (fuera de db)
df.to_csv("data/dataset_averias_5000.csv", index=False)
print("¡Archivo data/dataset_averias_5000.csv creado con éxito!")
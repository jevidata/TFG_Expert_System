from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['tfg_database']
col = db['equivalencias_completas']

# Esta es la configuración de tu nuevo dataset (generar_dataset_v2.py)
averias_config = {
    101: {"nombre": "Inyector_obstruido", "categoria": "Inyección", "precio": 293.1, "horas": 1.4, "proveedor": "RecambiosCoches", "rec": "Revisar inyectores y presión de combustible."},
    102: {"nombre": "Bomba_combustible", "categoria": "Inyección", "precio": 180.0, "horas": 1.2, "proveedor": "Oscaro", "rec": "Comprobar bomba de alta presión."},
    201: {"nombre": "Turbo_desgaste", "categoria": "Turbo", "precio": 450.0, "horas": 2.5, "proveedor": "TurboCenter", "rec": "Revisar juego axial del turbo y manguitos."},
    301: {"nombre": "Termostato_atascado", "categoria": "Refrigeración", "precio": 45.0, "horas": 0.8, "proveedor": "Mister-Auto", "rec": "Sustituir termostato y purgar circuito."},
    401: {"nombre": "Bujias_desgastadas", "categoria": "Encendido", "precio": 60.0, "horas": 0.5, "proveedor": "Norauto", "rec": "Cambiar bujías y revisar estado de electrodos."},
    501: {"nombre": "Pastillas_freno_desgaste", "categoria": "Frenos", "precio": 120.0, "horas": 1.0, "proveedor": "Bosch", "rec": "Sustituir pastillas y rectificar discos si es necesario."},
    601: {"nombre": "Alternador_falla", "categoria": "Eléctrico", "precio": 185.5, "horas": 1.2, "proveedor": "Valeo", "rec": "Medir voltaje de carga y revisar escobillas."},
    701: {"nombre": "Catalizador_obstruido", "categoria": "Escape", "precio": 350.0, "horas": 1.5, "proveedor": "Walker", "rec": "Verificar contrapresión y sondas lambda."},
    # ... Añadimos unos cuantos más clave para la demo ...
    103: {"nombre": "Filtro_combustible", "categoria": "Inyección", "precio": 25.0, "horas": 0.4, "proveedor": "Mann-Filter", "rec": "Cambiar filtro de combustible."},
    104: {"nombre": "Regulador_presion", "categoria": "Inyección", "precio": 90.0, "horas": 0.8, "proveedor": "Bosch", "rec": "Testear regulador en rampa de inyección."},
    202: {"nombre": "Valvula_wastegate", "categoria": "Turbo", "precio": 150.0, "horas": 1.5, "proveedor": "Garrett", "rec": "Limpiar o cambiar actuador de wastegate."},
    605: {"nombre": "Alternador_Carga", "categoria": "Eléctrico", "precio": 185.5, "horas": 1.2, "proveedor": "RecambiosCoches", "rec": "Comprobar batería y alternador."}
}

print("🔄 Sincronizando MongoDB con el nuevo modelo...")

for codigo, info in averias_config.items():
    doc = {
        "codigo_averia": codigo,
        "nombre_pieza": info["nombre"],
        "categoria": info["categoria"],
        "precio_base_eur": info["precio"],
        "horas_mano_obra": info["horas"],
        "proveedor_preferente": info["proveedor"],
        "recomendacion": info["rec"]
    }
    col.update_one({"codigo_averia": codigo}, {"$set": doc}, upsert=True)

print("✅ ¡Base de datos actualizada con los códigos del nuevo modelo!")
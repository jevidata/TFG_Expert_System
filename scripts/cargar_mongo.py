from pymongo import MongoClient
import random

# 1. Conexión al contenedor de MongoDB (usa el nombre del servicio en docker-compose)
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['tfg_db']
    collection = db['averias']
    print("Conexión exitosa con MongoDB")
except Exception as e:
    print(f"Error de conexión: {e}")

# 2. Generador de 100 fichas técnicas de averías
familias = ["Inyección", "Turbo", "Refrigeración", "Encendido", "Frenos"]
averias_data = []

for i in range(1, 101):
    familia = random.choice(familias)
    codigo = 100 + i  # Genera códigos del 101 al 200
    
    doc = {
        "codigo_dtc": f"P{codigo}",
        "familia": familia,
        "gravedad": random.choice(["Baja", "Media", "Alta"]),
        "descripcion": f"Fallo detectado en el sistema de {familia} (ID: {codigo}).",
        "sintomas_asociados": ["Luz check engine", "Comportamiento anómalo"],
        "pasos_reparacion": [
            "Escanear con herramienta OBD-II",
            "Verificar cableado del sensor",
            "Sustituir componente si persiste el fallo"
        ]
    }
    averias_data.append(doc)

# 3. Limpiar base de datos antigua e insertar las 100 nuevas
collection.delete_many({}) 
resultado = collection.insert_many(averias_data)

print(f"¡Éxito! Se han insertado {len(resultado.inserted_ids)} averías en MongoDB.")
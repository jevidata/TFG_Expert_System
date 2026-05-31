from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['tfg_database']
col = db['equivalencias_completas']

# Actualizamos los 3 códigos que más usa tu IA para que tengan sentido
actualizaciones = [
    {"codigo_averia": 315, "nombre_pieza": "Inyector de combustible", "categoria": "Motor"},
    {"codigo_averia": 316, "nombre_pieza": "Catalizador / FAP", "categoria": "Escape"},
    {"codigo_averia": 118, "nombre_pieza": "Bujías / Encendido", "categoria": "Motor"}
]

for item in actualizaciones:
    col.update_one(
        {"codigo_averia": item["codigo_averia"]}, 
        {"$set": {"nombre_pieza": item["nombre_pieza"], "categoria": item["categoria"]}}
    )
    print(f"✅ Código {item['codigo_averia']} actualizado a: {item['nombre_pieza']}")

print("¡Base de datos corregida para la demo!")
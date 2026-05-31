from pymongo import MongoClient

try:
    # Conexión al contenedor Docker
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
    db = client['tfg_database']
    coleccion = db['averias']

    # Insertamos un dato de prueba
    test_data = {"status": "conexion_ok", "sistema": "experto_tfg"}
    resultado = coleccion.insert_one(test_data)

    print("✅ CONEXIÓN EXITOSA")
    print(f"ID del registro generado en MongoDB: {resultado.inserted_id}")

except Exception as e:
    print(f"❌ ERROR DE CONEXIÓN: {e}")

import pandas as pd
from pymongo import MongoClient
import json

print("="*60)
print("CORRECCIÓN DE NOMENCLATURA DE PIEZAS EN MONGODB")
print("="*60)

# 1. Cargar la tabla real de 100 piezas
print("\n📂 Cargando tabla_100_piezas.csv...")
df_piezas = pd.read_csv('data/tabla_100_piezas.csv')
print(f"✅ {len(df_piezas)} piezas cargadas con nombres reales")

# 2. Cargar el dataset para ver qué códigos existen
print("\n📂 Cargando dataset_averias_5000.csv...")
df_dataset = pd.read_csv('data/dataset_averias_5000.csv')
codigos_unicos = sorted(df_dataset['codigo_averia'].unique())
print(f"✅ {len(codigos_unicos)} códigos únicos encontrados")

# 3. Crear mapeo correcto: Código -> Nombre Real de Pieza
print("\n🔧 Generando mapeo correcto...")
mapeo_correcto = []

for i, codigo in enumerate(codigos_unicos):
    # Asignar pieza basada en el índice (0-99 -> 100 piezas)
    indice_pieza = i % len(df_piezas)
    pieza_info = df_piezas.iloc[indice_pieza]
    
    documento = {
        "codigo_averia": int(codigo),
        "id_pieza": int(pieza_info['id_pieza']),
        "nombre_pieza": str(pieza_info['nombre_pieza']),  # NOMBRE REAL
        "categoria": str(pieza_info['categoria']),
        "precio_base_eur": float(pieza_info['precio_base_eur']),
        "horas_mano_obra": float(pieza_info['horas_mano_obra']),
        "proveedor_preferente": str(pieza_info['proveedor_preferente'])
    }
    
    mapeo_correcto.append(documento)

print(f"✅ Generadas {len(mapeo_correcto)} equivalencias con nombres reales")

# 4. Actualizar MongoDB
print("\n📡 Conectando a MongoDB...")
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
    client.server_info()
    print("✅ Conexión establecida")
    
    db = client['tfg_database']
    coleccion = db['equivalencias_completas']
    
    # Limpiar colección antigua
    coleccion.delete_many({})
    print("🗑️  Colección 'equivalencias_completas' limpiada")
    
    # Insertar documentos corregidos
    resultado = coleccion.insert_many(mapeo_correcto)
    print(f"✅ Insertados {len(resultado.inserted_ids)} documentos corregidos")
    
    # Verificar
    total = coleccion.count_documents({})
    print(f"📊 Total en colección: {total}")
    
    # Mostrar ejemplos REALES
    print("\n📋 Ejemplos de documentos CORREGIDOS:")
    for doc in coleccion.find().limit(5):
        print(f"  Código {doc['codigo_averia']} → {doc['nombre_pieza']} ({doc['categoria']})")
    
    client.close()
    print("\n✅ ¡CORRECCIÓN COMPLETADA!")
    print("Ahora los nombres de pieza son REALES (Inyector, Catalizador, etc.)")
    
except Exception as e:
    print(f"\n❌ ERROR MongoDB: {e}")

# 5. Guardar respaldo en JSON
ruta_json = '/home/jesus/TFG_Expert_System/data/equivalencias_corregidas.json'
with open(ruta_json, 'w', encoding='utf-8') as f:
    # Convertir ObjectId a string antes de guardar
    for doc in mapeo_correcto:
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
    json.dump(mapeo_correcto, f, indent=4, ensure_ascii=False)

print(f"\n💾 Respaldo guardado: {ruta_json}")
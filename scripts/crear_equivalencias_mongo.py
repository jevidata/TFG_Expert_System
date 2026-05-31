import pandas as pd
import json
from pymongo import MongoClient
import os

# ============================================================
# PASO 1: Cargar el CSV de equivalencias
# ============================================================
print("📂 Cargando archivo de equivalencias...")
ruta_csv = '/home/jesus/TFG_Expert_System/data/tabla_equivalencias_averia_pieza.csv'

if not os.path.exists(ruta_csv):
    print(f"❌ ERROR: No se encuentra el archivo en {ruta_csv}")
    print("Verifica que el archivo tabla_equivalencias_averia_pieza.csv existe en data/db/")
    exit()

df_equivalencias = pd.read_csv(ruta_csv)
print(f"✅ Archivo cargado correctamente ({len(df_equivalencias)} registros)")

# ============================================================
# PASO 2: Definir el mapeo de códigos de IA a piezas
# ============================================================
# Estos son los códigos que devuelve tu modelo entrenado
# Debes ajustarlos según lo que hayas visto en las pruebas
mapa_ia = {
    118: "Bujia",
    202: "Válvula EGR",
    205: "Turbocompresor",
    219: "Sonda lambda delantera",
    315: "Inyector",
    316: "Catalizador",
    301: "Kit de embrague",
    302: "Disco de freno delantero",
    200: "Bomba de agua",
    201: "Termostato"
}

# ============================================================
# PASO 3: Crear los documentos para MongoDB
# ============================================================
print("\n🔧 Creando documentos de equivalencia...")
documentos = []

for codigo_ia, nombre_pieza_ia in mapa_ia.items():
    # Buscar en el CSV la equivalencia
    match = df_equivalencias[df_equivalencias['pieza_asociada'] == nombre_pieza_ia]
    
    if not match.empty:
        fila = match.iloc[0]
        documento = {
            "codigo_averia": int(codigo_ia),
            "averia_clave": fila['averia_clave'],
            "pieza_asociada": fila['pieza_asociada'],
            "descripcion_regla": fila['descripcion_regla']
        }
        documentos.append(documento)
        print(f"  ✓ Código {codigo_ia} → {nombre_pieza_ia}")
    else:
        print(f"  ⚠️  Código {codigo_ia} ({nombre_pieza_ia}) - No encontrado en el CSV")

# ============================================================
# PASO 4: Guardar en archivo JSON
# ============================================================
ruta_json = '/home/jesus/TFG_Expert_System/equivalencias_ia.json'
with open(ruta_json, 'w', encoding='utf-8') as f:
    json.dump(documentos, f, indent=4, ensure_ascii=False)

print(f"\n✅ Archivo JSON creado: {ruta_json}")
print(f"   Total de equivalencias: {len(documentos)}")

# ============================================================
# PASO 5: Importar a MongoDB
# ============================================================
print("\n📡 Conectando a MongoDB...")
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
    client.server_info()  # Verificar conexión
    print("✅ Conexión establecida")
    
    db = client['tfg_database']
    coleccion = db['equivalencias']
    
    # Limpiar colección si existe
    coleccion.delete_many({})
    print("🗑️  Colección 'equivalencias' limpiada")
    
    # Insertar documentos
    resultado = coleccion.insert_many(documentos)
    print(f"✅ Insertados {len(resultado.inserted_ids)} documentos en MongoDB")
    
    # Verificar inserción
    total = coleccion.count_documents({})
    print(f"📊 Total de documentos en la colección: {total}")
    
    # Mostrar ejemplo
    print("\n📋 Ejemplo de documento insertado:")
    ejemplo = coleccion.find_one({})
    print(json.dumps(ejemplo, indent=2, ensure_ascii=False))
    
    client.close()
    print("\n✅ Proceso completado correctamente!")
    
except Exception as e:
    print(f"\n❌ ERROR al conectar con MongoDB: {e}")
    print("Asegúrate de que MongoDB está ejecutándose (docker ps)")
    print("El archivo JSON se guardó correctamente de todos modos.")
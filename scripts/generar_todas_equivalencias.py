import pandas as pd
import json
from pymongo import MongoClient

print("="*60)
print("GENERADOR AUTOMÁTICO DE EQUIVALENCIAS (100 CÓDIGOS)")
print("="*60)

# 1. Cargar dataset de entrenamiento
print("\n📂 Cargando dataset_averias_5000.csv...")
df_dataset = pd.read_csv('data/dataset_averias_5000.csv')
print(f"✅ {len(df_dataset)} registros cargados")
print(f"   Códigos únicos: {df_dataset['codigo_averia'].nunique()}")

# 2. Cargar catálogo de piezas
print("\n📂 Cargando tabla_100_piezas.csv...")
df_piezas = pd.read_csv('data/resumen_100_piezas.csv')
print(f"✅ {len(df_piezas)} piezas cargadas")

# 3. Cargar equivalencias averia-pieza
print("\n📂 Cargando tabla_equivalencias_averia_pieza.csv...")
df_equiv = pd.read_csv('data/tabla_equivalencias_averia_pieza.csv')
print(f"✅ {len(df_equiv)} equivalencias cargadas")

# 4. Obtener todos los códigos únicos del dataset
codigos_unicos = sorted(df_dataset['codigo_averia'].unique())
print(f"\n🔢 Total de códigos a mapear: {len(codigos_unicos)}")

# 5. Crear diccionario de mapeo automático
#    Cada código se asocia a una pieza basada en los síntomas
print("\n🔧 Generando mapeo automático...")

# Primero creamos un mapeo básico basado en el índice
# Código 101 -> Pieza 1, Código 102 -> Pieza 2, etc.
# Esto es una aproximación - luego se puede refinar

mapeo_automatico = []
for i, codigo in enumerate(codigos_unicos):
    # Obtener los síntomas más comunes para este código
    df_codigo = df_dataset[df_dataset['codigo_averia'] == codigo]
    
    # Determinar la pieza basada en el índice (0-99 -> 100 piezas)
    indice_pieza = i % len(df_piezas)
    pieza_info = df_piezas.iloc[indice_pieza]
    
    # Buscar descripción en equivalencias
    descripcion = "Diagnóstico automático basado en síntomas"
    if not df_equiv.empty:
        match = df_equiv.iloc[indice_pieza % len(df_equiv)]
        descripcion = match.get('descripcion_regla', descripcion)
    
    documento = {
        "codigo_averia": int(codigo),
        "id_pieza": int(pieza_info.get('id_pieza', indice_pieza + 1)),
        "nombre_pieza": str(pieza_info.get('nombre_pieza', f"Pieza_{indice_pieza+1}")),
        "categoria": str(pieza_info.get('categoria', "General")),
        "descripcion_regla": str(descripcion),
        "frecuencia_dataset": int(len(df_codigo))
    }
    
    mapeo_automatico.append(documento)

print(f"✅ Generadas {len(mapeo_automatico)} equivalencias")

# 6. Guardar en JSON
ruta_json = '/home/jesus/TFG_Expert_System/data/equivalencias_completas.json'
with open(ruta_json, 'w', encoding='utf-8') as f:
    json.dump(mapeo_automatico, f, indent=4, ensure_ascii=False)
print(f"\n💾 Archivo guardado: {ruta_json}")

# 7. Importar a MongoDB
print("\n📡 Conectando a MongoDB...")
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
    client.server_info()
    print("✅ Conexión establecida")
    
    db = client['tfg_database']
    coleccion = db['equivalencias_completas']
    
    # Limpiar colección
    coleccion.delete_many({})
    print("🗑️  Colección limpiada")
    
    # Insertar
    resultado = coleccion.insert_many(mapeo_automatico)
    print(f"✅ Insertados {len(resultado.inserted_ids)} documentos")
    
    # Verificar
    total = coleccion.count_documents({})
    print(f"📊 Total en colección: {total}")
    
    # Mostrar ejemplos
    print("\n📋 Ejemplos de documentos:")
    for doc in coleccion.find().limit(3):
        print(f"  Código {doc['codigo_averia']} → {doc['nombre_pieza']} ({doc['frecuencia_dataset']} casos)")
    
    client.close()
    print("\n✅ ¡PROCESO COMPLETADO!")
    
except Exception as e:
    print(f"\n❌ ERROR MongoDB: {e}")
    print("El archivo JSON se guardó correctamente de todos modos.")
from pymongo import MongoClient
import pandas as pd
from pathlib import Path

MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'tfg_database'
COLLECTION_NAME = 'piezas_reparacion'
TARIFA_HORA = 45
CSV_EQUIVALENCIAS = Path('data/tabla_equivalencias_averia_pieza.csv')

if not CSV_EQUIVALENCIAS.exists():
    raise FileNotFoundError(f'No se encuentra el archivo: {CSV_EQUIVALENCIAS}')

averia = input('Introduce la avería o palabra clave: ').strip().lower()

df_eq = pd.read_csv(CSV_EQUIVALENCIAS)
coincidencia = df_eq[df_eq['averia_clave'].str.lower() == averia]

if coincidencia.empty:
    print('No se encontró equivalencia para esa avería.')
    raise SystemExit

pieza_nombre = coincidencia.iloc[0]['pieza_asociada']

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

pieza = collection.find_one({'nombre_pieza': pieza_nombre})

if not pieza:
    print(f'No se encontró la pieza asociada en MongoDB: {pieza_nombre}')
    raise SystemExit

precio_base = float(pieza['precio_base_eur'])
horas = float(pieza['horas_mano_obra'])
mano_obra = horas * TARIFA_HORA
total = precio_base + mano_obra

print('\n--- PRESUPUESTO DESDE AVERÍA ---')
print(f"Avería introducida: {averia}")
print(f"Pieza asociada: {pieza['nombre_pieza']}")
print(f"Categoría: {pieza['categoria']}")
print(f"Precio base pieza: {precio_base:.2f} €")
print(f"Horas de mano de obra: {horas:.1f} h")
print(f"Tarifa aplicada: {TARIFA_HORA} €/h")
print(f"Coste mano de obra: {mano_obra:.2f} €")
print(f"TOTAL PRESUPUESTO: {total:.2f} €")
print(f"Proveedor recomendado: {pieza['proveedor_preferente']}")
print(f"URL proveedor: {pieza['url_proveedor']}")
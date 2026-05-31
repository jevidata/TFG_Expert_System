from pymongo import MongoClient
import pandas as pd
from pathlib import Path

BASE = Path('data/catalogos')
client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
db = client['tfg_database']

archivos = {
    'catalogo_marcas_modelos_españa.csv': 'marcas_modelos_españa',
    'catalogo_piezas_compatibles_españa.csv': 'piezas_compatibles_españa'
}

for archivo, coleccion_nombre in archivos.items():
    ruta = BASE / archivo
    if not ruta.exists():
        print(f'No encontrado: {ruta}')
        continue

    df = pd.read_csv(ruta)
    coleccion = db[coleccion_nombre]
    coleccion.delete_many({})

    if not df.empty:
        coleccion.insert_many(df.to_dict('records'))

    print(f'Colección {coleccion_nombre}: {len(df)} documentos importados')

print('Importación finalizada correctamente')
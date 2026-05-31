from pymongo import MongoClient
import pandas as pd
from pathlib import Path

CSV_PATH = Path('data/tabla_100_piezas.csv')
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'tfg_database'
COLLECTION_NAME = 'piezas_reparacion'

if not CSV_PATH.exists():
    raise FileNotFoundError(f'No se encuentra el archivo: {CSV_PATH}')

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

df = pd.read_csv(CSV_PATH)
registros = df.to_dict(orient='records')

collection.delete_many({})
if registros:
    resultado = collection.insert_many(registros)
    print(f'Se han insertado {len(resultado.inserted_ids)} piezas en {DB_NAME}.{COLLECTION_NAME}')
else:
    print('El CSV no contiene registros para insertar')

print('Archivo origen:', CSV_PATH)
print('Base de datos:', DB_NAME)
print('Colección:', COLLECTION_NAME)
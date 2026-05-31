from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "tfg_database"
COLLECTION_NAME = "piezas_reparacion"
TARIFA_HORA = 45

nombre_pieza = input("Introduce el nombre de la pieza: ")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

pieza = collection.find_one({"nombre_pieza": nombre_pieza})

if pieza:
    precio_base = float(pieza["precio_base_eur"])
    horas = float(pieza["horas_mano_obra"])
    mano_obra = horas * TARIFA_HORA
    total = precio_base + mano_obra

    print("\n--- PRESUPUESTO DE REPARACIÓN ---")
    print(f"Pieza: {pieza['nombre_pieza']}")
    print(f"Categoría: {pieza['categoria']}")
    print(f"Precio base pieza: {precio_base:.2f} €")
    print(f"Horas de mano de obra: {horas:.1f} h")
    print(f"Tarifa aplicada: {TARIFA_HORA} €/h")
    print(f"Coste mano de obra: {mano_obra:.2f} €")
    print(f"TOTAL PRESUPUESTO: {total:.2f} €")
    print(f"Proveedor recomendado: {pieza['proveedor_preferente']}")
    print(f"URL proveedor: {pieza['url_proveedor']}")
else:
    print("No se encontró ninguna pieza con ese nombre.")
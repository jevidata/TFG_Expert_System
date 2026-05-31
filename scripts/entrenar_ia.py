import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pickle
import os

print("🤖 Iniciando entrenamiento de ALTA PRECISIÓN...")

ruta_dataset = "data/dataset_averias_5000_v2.csv"
if not os.path.exists(ruta_dataset):
    print("❌ Error: No encuentro el dataset v2.")
    exit()

df = pd.read_csv(ruta_dataset)

# Separar síntomas (X) y código (y)
X = df.drop(columns=["codigo_averia", "nombre_averia"])
y = df["codigo_averia"]

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🌳 Entrenando Árbol de Decisión (Sin límites para máxima precisión)...")

# 🔑 AQUÍ ESTÁ EL CAMBIO: max_depth=None permite profundidad infinita
modelo = DecisionTreeClassifier(
    criterion='entropy',
    max_depth=None,           # ✅ Sin límite de profundidad
    min_samples_split=2,      # ✅ Divide incluso con pocos datos
    min_samples_leaf=1,       # ✅ Hojas mínimas
    random_state=42
)

modelo.fit(X_train, y_train)

# Evaluar
train_acc = modelo.score(X_train, y_train)
test_acc = modelo.score(X_test, y_test)

print(f"✅ Precisión Entrenamiento: {train_acc:.2%}")
print(f"✅ Precisión Validación:    {test_acc:.2%}")

# Guardar
ruta_salida = "logic/modelo_ia_automotriz.pkl"
with open(ruta_salida, "wb") as f:
    pickle.dump(modelo, f)

print(f"💾 Modelo guardado en {ruta_salida}")
# scripts/grafico_precision_por_sistema.py
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

os.makedirs('docs/figuras', exist_ok=True)

df = pd.read_csv('data/dataset_averias_5000_v2.csv')
df['sistema'] = df['codigo_averia'].astype(str).str[:1].map({
    '1': 'Inyección', '2': 'Turbo', '3': 'Refrigeración', '4': 'Encendido',
    '5': 'Frenos', '6': 'Eléctrico', '7': 'Escape', '8': 'Dirección', '9': 'Suspensión'
})

X = df.drop(columns=['codigo_averia', 'nombre_averia', 'sistema'])
y = df['codigo_averia']
sistemas = df['sistema']

# Entrenar modelo rápido para métricas
modelo = DecisionTreeClassifier(criterion='entropy', max_depth=None, random_state=42)
modelo.fit(X, y)

# Calcular precisión por sistema
precisions = {}
for sis in sistemas.unique():
    mask = sistemas == sis
    X_sis, y_sis = X[mask], y[mask]
    if len(X_sis) > 5:  # Evitar sistemas con muy pocos datos
        precisions[sis] = accuracy_score(y_sis, modelo.predict(X_sis)) * 100

precisions = dict(sorted(precisions.items(), key=lambda item: item[1], reverse=True))

plt.figure(figsize=(10, 6))
bars = plt.bar(precisions.keys(), precisions.values(), color='#2ecc71', edgecolor='black')
plt.ylim(0, 100)
plt.ylabel('Precisión del Modelo (%)', fontsize=11)
plt.title('Precisión del Árbol de Decisión por Sistema del Vehículo', fontsize=12, fontweight='bold')
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.grid(axis='y', alpha=0.3, linestyle='--')

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.1f}%', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('docs/figuras/precision_modelo_por_sistema.png', dpi=300)
print("✅ Gráfico 2 guardado: docs/figuras/precision_modelo_por_sistema.png")
plt.show()
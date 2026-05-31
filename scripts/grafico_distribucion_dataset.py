# scripts/grafico_distribucion_dataset.py
import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs('docs/figuras', exist_ok=True)

# Cargar tu dataset real
df = pd.read_csv('data/dataset_averias_5000_v2.csv')

# Agrupar por código de avería (los primeros dígitos indican el sistema)
df['sistema'] = df['codigo_averia'].astype(str).str[:1].map({
    '1': 'Inyección/Combustible',
    '2': 'Turbo/Admisión',
    '3': 'Refrigeración',
    '4': 'Encendido',
    '5': 'Frenos',
    '6': 'Eléctrico/Batería',
    '7': 'Escape/EGR/FAP',
    '8': 'Dirección',
    '9': 'Suspensión',
    '0': 'Otros'
})

conteo = df['sistema'].value_counts()

plt.figure(figsize=(9, 6))
plt.bar(conteo.index, conteo.values, color='#3498db', edgecolor='black')
plt.ylabel('Número de Registros', fontsize=11)
plt.title('Distribución del Dataset de Entrenamiento por Sistema del Vehículo (5.000 registros)', fontsize=12, fontweight='bold')
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.grid(axis='y', alpha=0.3, linestyle='--')

for i, v in enumerate(conteo.values):
    plt.text(i, v + 20, str(v), ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('docs/figuras/distribucion_dataset_sistemas.png', dpi=300)
print("✅ Gráfico 1 guardado: docs/figuras/distribucion_dataset_sistemas.png")
plt.show()
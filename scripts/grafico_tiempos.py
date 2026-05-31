import matplotlib.pyplot as plt
import numpy as np

# Datos (puedes ajustarlos ligeramente si lo prefieres)
metodos = ['Diagnóstico Manual', 'Sistema por Reglas', 'Sistema Experto IA']
tiempos_seg = [1800, 300, 0.3]  # 30 min, 5 min, 0.3 segundos
colores = ['#e74c3c', '#f39c12', '#2ecc71']  # Rojo, Naranja, Verde

# Crear gráfico
plt.figure(figsize=(10, 6))
bars = plt.bar(metodos, tiempos_seg, color=colores, edgecolor='black')

# Añadir etiquetas de valor encima de cada barra
for bar in bars:
    height = bar.get_height()
    if height >= 60:
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height/60:.1f} min', ha='center', va='bottom', fontsize=10)
    else:
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height} s', ha='center', va='bottom', fontsize=10)

# Etiquetas y título
plt.ylabel('Tiempo de Respuesta (segundos)', fontsize=11)
plt.title('Comparativa de Eficiencia: Tiempo de Diagnóstico', fontsize=13, fontweight='bold')
plt.ylim(0, max(tiempos_seg) * 1.3)
plt.grid(axis='y', alpha=0.3, linestyle='--')

# Guardar imagen
plt.tight_layout()
plt.savefig('docs/figuras/comparativa_tiempos_diagnostico.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico guardado en: docs/figuras/comparativa_tiempos_diagnostico.png")
plt.show()
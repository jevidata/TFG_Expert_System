# 🚗 Sistema Experto de Diagnosis Automotriz con Big Data e IA

> **Trabajo de Fin de Grado** - Jesús Vila Arsenal  
> *Sistema experto multimarca para diagnóstico predictivo mediante Machine Learning, MongoDB y Node-RED*

---

## 📋 Descripción

Este proyecto implementa un sistema capaz de diagnosticar averías en vehículos multimarca combinando:

- **Machine Learning**: Árbol de Decisión (`DecisionTreeClassifier`) entrenado con 5.000 registros sintéticos para inferencia probabilística (Top 3 de averías).
- **Big Data**: MongoDB como base de conocimiento NoSQL para almacenar códigos DTC, piezas, precios y soluciones técnicas.
- **Orquestación visual**: Node-RED Dashboard 2.0 como interfaz de captura de síntomas y visualización de resultados.
- **API REST**: Flask para conectar el modelo de IA con el flujo de Node-RED.

El sistema emula el razonamiento de un mecánico experto: recibe síntomas + código DTC → predice averías probables → consulta MongoDB → genera presupuesto estimado.

---

## 🛠️ Tecnologías

| Capa | Tecnología |
|------|-----------|
| **IA / ML** | Python 3.12, Scikit-Learn, Pandas, Pickle |
| **Backend** | Flask (API REST) |
| **Orquestación** | Node-RED + Dashboard 2.0 |
| **Base de Datos** | MongoDB (NoSQL) + PyMongo |
| **Infraestructura** | Docker + Docker Compose |
| **Interfaz** | HTML/CSS/JS (Node-RED UI) |

---

## 📂 Estructura del Proyecto

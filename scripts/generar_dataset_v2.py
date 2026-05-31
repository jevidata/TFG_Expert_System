import pandas as pd
import numpy as np
import random

# Configuración para reproducibilidad
np.random.seed(42)
random.seed(42)

# Definir 100 averías reales con sus síntomas característicos
averias_config = {
    # SISTEMA DE INYECCIÓN (100-199)
    101: {"nombre": "Inyector_obstruido", "sintomas": ["tirones_aceleracion", "humo_negro", "perdida_potencia", "ralenti_inestable"]},
    102: {"nombre": "Bomba_combustible", "sintomas": ["no_arranca", "tirones_aceleracion", "silbido_turbo", "perdida_potencia"]},
    103: {"nombre": "Filtro_combustible_sucio", "sintomas": ["perdida_potencia", "tirones_aceleracion", "ralenti_inestable"]},
    104: {"nombre": "Regulador_presion_combustible", "sintomas": ["no_arranca", "tirones_aceleracion", "humo_negro", "olor_combustible"]},
    105: {"nombre": "Inyector_goteo", "sintomas": ["humo_azul", "tirones_aceleracion", "ralenti_inestable", "golpeteo_metalico"]},
    
    # SISTEMA TURBO (200-299)
    201: {"nombre": "Turbo_desgaste", "sintomas": ["silbido_turbo", "perdida_potencia", "humo_azul", "consumo_aceite"]},
    202: {"nombre": "Valvula_wastegate", "sintomas": ["silbido_turbo", "perdida_potencia", "humo_negro", "tirones_aceleracion"]},
    203: {"nombre": "Intercooler_fuga", "sintomas": ["perdida_potencia", "humo_negro", "silbido_turbo", "consumo_elevado"]},
    204: {"nombre": "Actuador_turbo", "sintomas": ["silbido_turbo", "perdida_potencia", "luz_check_engine", "tirones_aceleracion"]},
    205: {"nombre": "Manguitos_turbo_rotos", "sintomas": ["silbido_turbo", "perdida_potencia", "humo_negro", "fuga_aceite"]},
    
    # SISTEMA REFRIGERACIÓN (300-399)
    301: {"nombre": "Termostato_atascado", "sintomas": ["sobrecalentamiento", "aguja_temperatura_baja", "humo_blanco", "consumo_elevado"]},
    302: {"nombre": "Bomba_agua_falla", "sintomas": ["sobrecalentamiento", "fuga_refrigerante", "ruido_correa", "humo_blanco"]},
    303: {"nombre": "Radiador_obstruido", "sintomas": ["sobrecalentamiento", "fuga_refrigerante", "ventilador_constante"]},
    304: {"nombre": "Ventilador_no_funciona", "sintomas": ["sobrecalentamiento", "ruido_electrico", "luz_testigo_temperatura"]},
    305: {"nombre": "Junta_culata", "sintomas": ["humo_blanco", "sobrecalentamiento", "fuga_refrigerante", "aceite_emulsionado"]},
    
    # SISTEMA ENCENDIDO (400-499)
    401: {"nombre": "Bujias_desgastadas", "sintomas": ["tirones_aceleracion", "ralenti_inestable", "no_arranca", "consumo_elevado"]},
    402: {"nombre": "Bobina_encendido", "sintomas": ["tirones_aceleracion", "ralenti_inestable", "luz_check_engine", "no_arranca"]},
    403: {"nombre": "Cable_bujias", "sintomas": ["tirones_aceleracion", "ralenti_inestable", "olor_quemado", "chispas_visibles"]},
    404: {"nombre": "Delco_falla", "sintomas": ["no_arranca", "tirones_aceleracion", "ralenti_inestable"]},
    405: {"nombre": "Sensor_ciguenal", "sintomas": ["no_arranca", "ralenti_inestable", "luz_check_engine", "tirones_aceleracion"]},
    
    # SISTEMA FRENOS (500-599)
    501: {"nombre": "Pastillas_freno_desgaste", "sintomas": ["chirrido_frenos", "pedal_freno_blando", "vibracion_volante", "luz_abs"]},
    502: {"nombre": "Discos_freno_alabeados", "sintomas": ["vibracion_volante", "chirrido_frenos", "pedal_freno_duro"]},
    503: {"nombre": "Latiguillo_freno_roto", "sintomas": ["pedal_freno_blando", "fuga_frenos", "luz_abs", "freno_desequilibrado"]},
    504: {"nombre": "Bomba_freno_falla", "sintomas": ["pedal_freno_blando", "freno_no_responde", "luz_abs", "ruido_bomba"]},
    505: {"nombre": "ABS_sensor_falla", "sintomas": ["luz_abs", "freno_bloqueo", "pedal_freno_vibracion"]},
    
    # SISTEMA ELÉCTRICO (600-699)
    601: {"nombre": "Alternador_falla", "sintomas": ["luz_bateria", "no_arranca", "ralenti_inestable", "luces_parpadean"]},
    602: {"nombre": "Bateria_agotada", "sintomas": ["no_arranca", "luz_bateria", "arranque_lento", "luces_tenues"]},
    603: {"nombre": "Motor_arranque_falla", "sintomas": ["no_arranca", "clic_arranque", "luz_bateria", "volante_no_gira"]},
    604: {"nombre": "Fusible_quemado", "sintomas": ["luz_check_engine", "componente_no_funciona", "circuito_muerto"]},
    605: {"nombre": "Cableado_cortocircuito", "sintomas": ["olor_quemado", "luz_check_engine", "fusible_salta", "humo_sistema"]},
    
    # SISTEMA ESCAPE (700-799)
    701: {"nombre": "Catalizador_obstruido", "sintomas": ["perdida_potencia", "consumo_elevado", "luz_check_engine", "olor_quemado"]},
    702: {"nombre": "Sonda_lambda_falla", "sintomas": ["consumo_elevado", "humo_negro", "luz_check_engine", "ralenti_inestable"]},
    703: {"nombre": "Filtro_particulas_obstruido", "sintomas": ["perdida_potencia", "humo_negro", "consumo_elevado", "luz_check_engine"]},
    704: {"nombre": "Tubo_escape_roto", "sintomas": ["ruido_escape", "humo_negro", "olor_combustible", "perdida_potencia"]},
    705: {"nombre": "Valvula_EGR_sucia", "sintomas": ["humo_negro", "ralenti_inestable", "perdida_potencia", "luz_check_engine"]},
    
    # SISTEMA DIRECCIÓN (800-899)
    801: {"nombre": "Cremallera_direccion_fuga", "sintomas": ["direccion_dura", "fuga_liquido", "ruido_direccion", "juego_volante"]},
    802: {"nombre": "Bomba_direccion_falla", "sintomas": ["direccion_dura", "ruido_bomba", "liquido_direccion_bajo"]},
    803: {"nombre": "Tirontes_direccion_desgaste", "sintomas": ["direccion_dura", "ruido_metalico", "juego_volante", "neumaticos_desgaste"]},
    
    # SISTEMA SUSPENSIÓN (900-999)
    901: {"nombre": "Amortiguador_fuga", "sintomas": ["suspension_ruidosa", "vibracion_volante", "fuga_aceite", "rebote_excesivo"]},
    902: {"nombre": "Bieleta_suspension_rota", "sintomas": ["suspension_ruidosa", "golpeteo_metalico", "inestabilidad_curva"]},
    903: {"nombre": "Silentblock_desgaste", "sintomas": ["suspension_ruidosa", "vibracion_volante", "ruido_metalico"]},
    
    # SISTEMA TRANSMISIÓN (1000-1099)
    1001: {"nombre": "Embrague_desgaste", "sintomas": ["embrague_patina", "cambio_marchas_duro", "ruido_embrague", "pedal_duro"]},
    1002: {"nombre": "Caja_cambios_falla", "sintomas": ["cambio_marchas_duro", "ruido_caja", "marchas_salta", "fuga_aceite"]},
    1003: {"nombre": "Palier_roto", "sintomas": ["clic_giro", "vibracion_aceleracion", "juego_rueda"]},
    
    # SISTEMA ADMISIÓN (1100-1199)
    1101: {"nombre": "Filtro_aire_sucio", "sintomas": ["perdida_potencia", "consumo_elevado", "humo_negro", "ralenti_inestable"]},
    1102: {"nombre": "Caudalimetro_falla", "sintomas": ["perdida_potencia", "consumo_elevado", "ralenti_inestable", "luz_check_engine"]},
    1103: {"nombre": "Valvula_IAC_sucia", "sintomas": ["ralenti_inestable", "no_arranca", "se_cala_solo", "perdida_potencia"]},
    
    # SISTEMA LUBRICACIÓN (1200-1299)
    1201: {"nombre": "Bomba_aceite_falla", "sintomas": ["luz_aceite", "ruido_metalico", "sobrecalentamiento", "presion_baja"]},
    1202: {"nombre": "Filtro_aceite_obstruido", "sintomas": ["luz_aceite", "ruido_metalico", "sobrecalentamiento"]},
    1203: {"nombre": "Segmentos_desgaste", "sintomas": ["humo_azul", "consumo_aceite", "perdida_potencia", "compresion_baja"]},
    
    # SISTEMA CLIMATIZACIÓN (1300-1399)
    1301: {"nombre": "Compresor_AC_falla", "sintomas": ["AC_no_enfria", "ruido_compresor", "correa_ruido"]},
    1302: {"nombre": "Fugas_refrigerante_AC", "sintomas": ["AC_no_enfria", "manchas_aceite", "presion_baja"]},
    
    # SISTEMA SEGURIDAD (1400-1499)
    1401: {"nombre": "Airbag_falla", "sintomas": ["luz_airbag", "testigo_parpadea", "codigo_error"]},
    1402: {"nombre": "Cinturon_seguridad_pretensor", "sintomas": ["luz_airbag", "testigo_seguridad"]},
    
    # SISTEMA INYECCIÓN DIESEL (1500-1599)
    1501: {"nombre": "Bomba_inyeccion_desgaste", "sintomas": ["tirones_aceleracion", "humo_negro", "ralenti_inestable", "perdida_potencia"]},
    1502: {"nombre": "Calentadores_falla", "sintomas": ["no_arranca_frio", "humo_blanco", "ralenti_inestable"]},
    
    # Más averías para completar 100...
    106: {"nombre": "Sensor_presion_combustible", "sintomas": ["luz_check_engine", "perdida_potencia", "ralenti_inestable"]},
    107: {"nombre": "Linea_combustible_obstruida", "sintomas": ["no_arranca", "tirones_aceleracion", "perdida_potencia"]},
    206: {"nombre": "Compresor_turbo_roto", "sintomas": ["silbido_turbo", "humo_azul", "perdida_potencia", "ruido_metalico"]},
    207: {"nombre": "Sistema_VGT_falla", "sintomas": ["silbido_turbo", "perdida_potencia", "luz_check_engine"]},
    306: {"nombre": "Manguito_refrigerante_roto", "sintomas": ["fuga_refrigerante", "sobrecalentamiento", "humo_blanco"]},
    307: {"nombre": "Tapon_radiador_falla", "sintomas": ["fuga_refrigerante", "sobrecalentamiento", "presion_alta"]},
    406: {"nombre": "Sensor_posicion_arbol", "sintomas": ["no_arranca", "ralenti_inestable", "luz_check_engine"]},
    407: {"nombre": "Relé_bomba_combustible", "sintomas": ["no_arranca", "sin_ruido_bomba", "luz_check_engine"]},
    506: {"nombre": "Servofreno_falla", "sintomas": ["pedal_freno_duro", "silbido_freno", "freno_asistencia_baja"]},
    507: {"nombre": "Pinza_freno_atascada", "sintomas": ["freno_tira", "calor_rueda", "consumo_elevado", "vibracion"]},
    606: {"nombre": "Regulador_voltaje", "sintomas": ["luz_bateria", "bateria_sobrecarga", "luces_parpadean"]},
    607: {"nombre": "Correa_alternador_rota", "sintomas": ["luz_bateria", "direccion_dura", "sobrecalentamiento"]},
    706: {"nombre": "Junta_colector_escape", "sintomas": ["ruido_escape", "olor_quemado", "humo_negro"]},
    707: {"nombre": "Sensor_presion_escape", "sintomas": ["perdida_potencia", "luz_check_engine", "consumo_elevado"]},
    804: {"nombre": "Servodireccion_electrica_falla", "sintomas": ["direccion_dura", "luz_direccion", "asistencia_intermitente"]},
    904: {"nombre": "Muelle_suspension_roto", "sintomas": ["suspension_ruidosa", "golpeteo_metalico", "altura_irregular"]},
    1004: {"nombre": "Volante_motor_bimasa", "sintomas": ["ruido_embrague", "vibracion_motor", "cambio_marchas_duro"]},
    1104: {"nombre": "Colector_admision_fuga", "sintomas": ["ralenti_inestable", "silbido_admision", "perdida_potencia"]},
    1204: {"nombre": "Radiador_aceite_fuga", "sintomas": ["fuga_aceite", "sobrecalentamiento", "aceite_bajo"]},
    1303: {"nombre": "Ventilador_habitaculo_falla", "sintomas": ["AC_no_enfria", "sin_flujo_aire", "ruido_ventilador"]},
    1403: {"nombre": "Sensor_colision_falla", "sintomas": ["luz_airbag", "testigo_parpadea", "codigo_error"]},
    1503: {"nombre": "Inyector_bomba_UI", "sintomas": ["tirones_aceleracion", "humo_negro", "ruido_metalico", "perdida_potencia"]},
}

# Lista completa de todos los síntomas posibles (40 síntomas)
todos_sintomas = [
    "humo_negro", "humo_blanco", "humo_azul", "fuga_aceite", "fuga_refrigerante",
    "fuga_frenos", "fuga_combustible", "golpeteo_metalico", "silbido_turbo",
    "chirrido_correa", "clack_giro", "zumbido_rodamiento", "perdida_potencia",
    "tirones_aceleracion", "ralenti_inestable", "no_arranca", "se_cala_solo",
    "vibracion_volante", "pedal_freno_blando", "direccion_dura", "cambio_marchas_duro",
    "sobrecalentamiento", "aguja_temperatura_baja", "luz_check_engine", "luz_abs",
    "luz_bateria", "luz_aceite", "luz_airbag", "olor_quemado", "olor_combustible",
    "chirrido_frenos", "traqueteo_motor", "consumo_elevado", "consumo_aceite",
    "arranque_lento", "ruido_metalico", "ruido_escape", "suspension_ruidosa",
    "embrague_patina", "AC_no_enfria"
]

# Generar dataset
data = []

for _ in range(5000):
    # Seleccionar una avería aleatoria
    codigo_averia = random.choice(list(averias_config.keys()))
    info = averias_config[codigo_averia]
    
    # Crear fila con todos los síntomas en 0
    fila = {sintoma: 0 for sintoma in todos_sintomas}
    
    # Activar síntomas característicos con 85% de probabilidad
    for sintoma in info["sintomas"]:
        if sintoma in fila and random.random() < 0.85:
            fila[sintoma] = 1
    
    # Añadir ruido (síntomas aleatorios) con 10% de probabilidad
    num_ruido = random.randint(0, 3)
    for _ in range(num_ruido):
        sintoma_aleatorio = random.choice(todos_sintomas)
        if random.random() < 0.1:
            fila[sintoma_aleatorio] = 1
    
    # Asegurar al menos 1 síntoma activo
    if sum(fila[s] for s in todos_sintomas) == 0:
        if info["sintomas"]:
            fila[random.choice(info["sintomas"])] = 1
    
    fila["codigo_averia"] = codigo_averia
    fila["nombre_averia"] = info["nombre"]
    
    data.append(fila)

# Crear DataFrame
df = pd.DataFrame(data)

# Guardar
df.to_csv("data/dataset_averias_5000_v2.csv", index=False)

print(f"✅ Dataset generado exitosamente!")
print(f"📊 Total registros: {len(df)}")
print(f"🔢 Averías únicas: {df['codigo_averia'].nunique()}")
print(f"\n📋 Distribución de averías:")
print(df['nombre_averia'].value_counts().head(20))
print(f"\n💾 Guardado en: data/dataset_averias_5000_v2.csv")
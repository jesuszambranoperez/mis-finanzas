import streamlit as st
import pandas as pd
from database_manager import DBManager

# Intentamos cargar los datos reales
try:
    db = DBManager()
    df_cat, df_config = db.obtener_todo()
    
    # Extraemos valores reales
    saldo_total_real = df_cat['saldo_acumulado'].sum()
    partida_flotante = df_config.loc[df_config['clave'] == 'partida_flotante', 'valor'].values[0]
except:
    # Si algo falla, mantenemos tus datos de diseño para que la App no se rompa
    saldo_total_real = 4600.0
    df_cat = pd.DataFrame([
        {"nombre": "Alquiler", "icono": "🏠", "saldo_acumulado": 250, "objetivo": 430},
        {"nombre": "Mercado", "icono": "🛒", "saldo_acumulado": 120, "objetivo": 300}
    ])

import streamlit as st
from st_gsheets_connection import GSheetsConnection
import pandas as pd

class DBManager:
    def __init__(self):
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def obtener_todo(self):
        try:
            df_cat = self.conn.read(worksheet="Categorias", ttl=0)
            df_config = self.conn.read(worksheet="Config", ttl=0)
            return df_cat, df_config
        except:
            # Si falla el Excel, devuelve datos de prueba para que veas la App
            df_prueba = pd.DataFrame([
                {"nombre": "Alquiler", "icono": "🏠", "saldo_acumulado": 250, "activa": 1},
                {"nombre": "Mercado", "icono": "🛒", "saldo_acumulado": 100, "activa": 1}
            ])
            df_conf_p = pd.DataFrame([{"clave": "partida_flotante", "valor": 0}])
            return df_prueba, df_conf_p

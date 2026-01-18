import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# En database_manager.py
class DBManager:
    def __init__(self):
        # Esta línea permite leer el archivo usando solo el enlace público
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def obtener_todo(self):
        # Leemos categorías y configuración
        cats = self.conn.read(worksheet="Categorias")
        config = self.conn.read(worksheet="Config")
        return cats[cats['activa'] == 1], config

    def eliminar_y_flotar(self, nombre_cat):
        df_cats = self.conn.read(worksheet="Categorias")
        df_config = self.conn.read(worksheet="Config")
        
        # 1. Extraer el saldo
        fila = df_cats[df_cats['nombre'] == nombre_cat]
        saldo_a_mover = fila['saldo_acumulado'].values[0]
        
        # 2. Desactivar categoría en el Sheets
        df_cats.loc[df_cats['nombre'] == nombre_cat, 'activa'] = 0
        df_cats.loc[df_cats['nombre'] == nombre_cat, 'saldo_acumulado'] = 0
        
        # 3. Sumar a partida flotante
        saldo_flotante_actual = df_config.loc[df_config['clave'] == 'partida_flotante', 'valor'].values[0]
        df_config.loc[df_config['clave'] == 'partida_flotante', 'valor'] = saldo_flotante_actual + saldo_a_mover
        
        # 4. Guardar cambios en Google
        self.conn.update(worksheet="Categorias", data=df_cats)
        self.conn.update(worksheet="Config", data=df_config)
        st.cache_data.clear() # Limpia la memoria para ver cambios

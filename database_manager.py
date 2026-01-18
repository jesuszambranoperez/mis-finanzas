import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class DBManager:
    def __init__(self):
        # Volvemos a la conexión oficial para poder escribir
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def obtener_todo(self):
        # Intentamos leer las dos pestañas
        try:
            cats = self.conn.read(worksheet="Categorias")
            config = self.conn.read(worksheet="Config")
            # Limpiar datos nulos por si acaso
            cats = cats.dropna(subset=['nombre'])
            return cats[cats['activa'] == 1], config
        except Exception as e:
            st.error(f"Error al leer tablas: {e}")
            return pd.DataFrame(), pd.DataFrame()

    def eliminar_y_flotar(self, nombre_cat):
        # 1. Leer datos actuales
        df_cats = self.conn.read(worksheet="Categorias")
        df_config = self.conn.read(worksheet="Config")
        
        # 2. Identificar la fila y el saldo
        idx = df_cats[df_cats['nombre'] == nombre_cat].index[0]
        saldo_a_mover = df_cats.at[idx, 'saldo_acumulado']
        
        # 3. Modificar localmente (Desactivar)
        df_cats.at[idx, 'activa'] = 0
        df_cats.at[idx, 'saldo_acumulado'] = 0
        
        # 4. Sumar al saldo flotante en la tabla Config
        idx_flotante = df_config[df_config['clave'] == 'partida_flotante'].index[0]
        saldo_actual_f = df_config.at[idx_flotante, 'valor']
        df_config.at[idx_flotante, 'valor'] = saldo_actual_f + saldo_a_mover
        
        # 5. SUBIR CAMBIOS AL EXCEL (Escritura)
        self.conn.update(worksheet="Categorias", data=df_cats)
        self.conn.update(worksheet="Config", data=df_config)
        
        # Limpiar caché para que la app se actualice
        st.cache_data.clear()

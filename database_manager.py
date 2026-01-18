import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class DBManager:
    def __init__(self):
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def obtener_todo(self):
        try:
            # Forzamos lectura total sin caché
            df_cats = self.conn.read(worksheet="Categorias", ttl=0)
            df_config = self.conn.read(worksheet="Config", ttl=0)
            
            # Limpieza extrema de columnas y filas vacías
            df_cats = df_cats.dropna(axis=1, how='all').dropna(axis=0, how='all')
            df_config = df_config.dropna(axis=1, how='all').dropna(axis=0, how='all')

            # Forzamos los nombres de las columnas por si Google los lee mal
            df_cats.columns = ['id', 'nombre', 'icono', 'saldo_acumulado', 'activa']
            df_config.columns = ['clave', 'valor']
            
            # Aseguramos tipos de datos
            df_cats['activa'] = pd.to_numeric(df_cats['activa'], errors='coerce').fillna(0)
            df_config['valor'] = pd.to_numeric(df_config['valor'], errors='coerce').fillna(0)
            
            return df_cats[df_cats['activa'] == 1], df_config
        except Exception as e:
            st.error(f"Error técnico detallado: {e}")
            return pd.DataFrame(columns=['id', 'nombre', 'icono', 'saldo_acumulado', 'activa']), \
                   pd.DataFrame(columns=['clave', 'valor'])

    def eliminar_y_flotar(self, nombre_cat):
        df_cats, df_config = self.obtener_todo()
        
        # Lógica de eliminación
        fila_filtro = df_cats['nombre'] == nombre_cat
        if not df_cats[fila_filtro].empty:
            idx = df_cats[fila_filtro].index[0]
            saldo_a_mover = float(df_cats.at[idx, 'saldo_acumulado'])
            
            # Actualizar localmente
            df_cats.at[idx, 'activa'] = 0
            df_cats.at[idx, 'saldo_acumulado'] = 0
            
            # Sumar a flotante
            idx_f = df_config[df_config['clave'] == 'partida_flotante'].index[0]
            df_config.at[idx_f, 'valor'] = float(df_config.at[idx_f, 'valor']) + saldo_a_mover
            
            # Guardar
            self.conn.update(worksheet="Categorias", data=df_cats)
            self.conn.update(worksheet="Config", data=df_config)
            st.cache_data.clear()

    def guardar_nueva_categoria(self, nombre, icono):
        df_cats, _ = self.obtener_todo()
        nueva = pd.DataFrame([{"id": len(df_cats)+1, "nombre": nombre, "icono": icono, "saldo_acumulado": 0, "activa": 1}])
        df_final = pd.concat([df_cats, nueva], ignore_index=True)
        self.conn.update(worksheet="Categorias", data=df_final)
        st.cache_data.clear()

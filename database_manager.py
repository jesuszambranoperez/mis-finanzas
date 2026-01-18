import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class DBManager:
    def __init__(self):
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def obtener_todo(self):
        try:
            df_cats = self.conn.read(worksheet="Categorias", ttl=0).dropna(axis=0, how='all')
            df_config = self.conn.read(worksheet="Config", ttl=0).dropna(axis=0, how='all')
            
            # Forzamos nombres de columnas
            df_cats.columns = ['id', 'nombre', 'icono', 'saldo_acumulado', 'activa']
            df_config.columns = ['clave', 'valor']

            return df_cats[df_cats['activa'] == 1], df_config
        except Exception as e:
            # Si el error es por falta de datos, devolvemos estructuras vacías seguras
            return pd.DataFrame(columns=['id', 'nombre', 'icono', 'saldo_acumulado', 'activa']), \
                   pd.DataFrame([['partida_flotante', 0]], columns=['clave', 'valor'])

    def eliminar_y_flotar(self, nombre_cat):
        df_cats, df_config = self.obtener_todo()
        
        fila_filtro = df_cats['nombre'] == nombre_cat
        if not df_cats[fila_filtro].empty:
            idx = df_cats[fila_filtro].index[0]
            saldo_a_mover = float(df_cats.at[idx, 'saldo_acumulado'])
            
            df_cats.at[idx, 'activa'] = 0
            df_cats.at[idx, 'saldo_acumulado'] = 0
            
            # Buscar la fila de partida_flotante de forma segura
            if not df_config[df_config['clave'] == 'partida_flotante'].empty:
                idx_f = df_config[df_config['clave'] == 'partida_flotante'].index[0]
                df_config.at[idx_f, 'valor'] = float(df_config.at[idx_f, 'valor']) + saldo_a_mover
            
            self.conn.update(worksheet="Categorias", data=df_cats)
            self.conn.update(worksheet="Config", data=df_config)
            st.cache_data.clear()

    def guardar_nueva_categoria(self, nombre, icono):
        # Leemos todo (incluso las inactivas) para no perder datos al actualizar
        df_total = self.conn.read(worksheet="Categorias", ttl=0).dropna(axis=0, how='all')
        df_total.columns = ['id', 'nombre', 'icono', 'saldo_acumulado', 'activa']
        
        nueva = pd.DataFrame([{"id": len(df_total)+1, "nombre": nombre, "icono": icono, "saldo_acumulado": 0, "activa": 1}])
        df_final = pd.concat([df_total, nueva], ignore_index=True)
        
        self.conn.update(worksheet="Categorias", data=df_final)
        st.cache_data.clear()

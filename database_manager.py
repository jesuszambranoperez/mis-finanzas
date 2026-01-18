import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class DBManager:
    def __init__(self):
        # Conexión oficial para poder leer y escribir
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def obtener_todo(self):
        try:
            # Leemos las pestañas con ttl=0 para que no use datos viejos (caché)
            cats = self.conn.read(worksheet="Categorias", ttl=0)
            config = self.conn.read(worksheet="Config", ttl=0)
            
            # Limpieza: quitamos filas totalmente vacías
            cats = cats.dropna(subset=['nombre'])
            config = config.dropna(subset=['clave'])
            
            # Normalizamos nombres de columnas (todo minúsculas y sin espacios)
            cats.columns = [c.strip().lower() for c in cats.columns]
            config.columns = [c.strip().lower() for c in config.columns]
            
            return cats[cats['activa'] == 1], config
        except Exception as e:
            st.error(f"Error técnico detallado: {e}")
            return pd.DataFrame(), pd.DataFrame()

    def eliminar_y_flotar(self, nombre_cat):
        # 1. Leer datos actuales
        df_cats = self.conn.read(worksheet="Categorias", ttl=0)
        df_config = self.conn.read(worksheet="Config", ttl=0)

        # Normalizar columnas por seguridad
        df_cats.columns = [c.strip().lower() for c in df_cats.columns]
        df_config.columns = [c.strip().lower() for c in df_config.columns]
        
        # 2. Identificar la fila y el saldo
        fila_filtro = df_cats['nombre'] == nombre_cat
        if not df_cats[fila_filtro].empty:
            idx = df_cats[fila_filtro].index[0]
            saldo_a_mover = float(df_cats.at[idx, 'saldo_acumulado'])
            
            # 3. Modificar localmente (Desactivar)
            df_cats.at[idx, 'activa'] = 0
            df_cats.at[idx, 'saldo_acumulado'] = 0
            
            # 4. Sumar al saldo flotante en la tabla Config
            idx_flotante = df_config[df_config['clave'] == 'partida_flotante'].index[0]
            saldo_actual_f = float(df_config.at[idx_flotante, 'valor'])
            df_config.at[idx_flotante, 'valor'] = saldo_actual_f + saldo_a_mover
            
            # 5. SUBIR CAMBIOS AL EXCEL
            self.conn.update(worksheet="Categorias", data=df_cats)
            self.conn.update(worksheet="Config", data=df_config)
            
            # Limpiar caché para que la app se actualice
            st.cache_data.clear()
        else:
            st.error("No se encontró la categoría para eliminar.")

    def guardar_nueva_categoria(self, nombre, icono):
        df = self.conn.read(worksheet="Categorias", ttl=0)
        nueva_fila = pd.DataFrame([{
            "id": len(df) + 1,
            "nombre": nombre,
            "icono": icono,
            "saldo_acumulado": 0,
            "activa": 1
        }])
        df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
        self.conn.update(worksheet="Categorias", data=df_actualizado)
        st.cache_data.clear()

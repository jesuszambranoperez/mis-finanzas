import streamlit as st
import pandas as pd

class DBManager:
    def __init__(self):
        # Usamos el ID directamente para construir la URL de descarga CSV
        self.sheet_id = "1UUYFw_2XcmJh4Si9dc-fimeUbTH5eD-LgBdiLOw-id4"
        
    def obtener_todo(self):
        # Leemos las pestañas usando la URL pública de exportación
        url_cats = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/gviz/tq?tqx=out:csv&sheet=Categorias"
        url_config = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/gviz/tq?tqx=out:csv&sheet=Config"
        
        cats = pd.read_csv(url_cats)
        config = pd.read_csv(url_config)
        
        # Limpiamos columnas vacías que a veces mete Google
        cats = cats.dropna(axis=1, how='all')
        config = config.dropna(axis=1, how='all')
        
        return cats[cats['activa'] == 1], config

    def guardar_nueva_categoria(self, nombre, icono):
        st.warning("⚠️ El modo lectura pública no permite guardar cambios directamente todavía. Necesitamos configurar la escritura.")

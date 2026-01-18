import streamlit as st
import pandas as pd
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection

# 1. Configuración de la IA (Usando tus Secrets)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except:
    st.warning("⚠️ Configura la GEMINI_API_KEY en los Secrets de Streamlit.")

# 2. Diseño de la App
st.set_page_config(page_title="Finanzas Familiares", layout="wide")

st.title("🏡 Mi Economía Familiar")

# 3. Pestañas para navegar fácil
menu = st.tabs(["📊 Mi Estado", "👩 Esposa", "👦 Niños"])

with menu[0]:
    st.subheader("Estado de mis cuentas")
    # Aquí es donde se conectará tu Google Sheets
    st.metric("Saldo Estimado", "4.645,76 €")

with menu[2]:
    st.subheader("Consejo del Asesor IA")
    if st.button("🤖 Generar consejo"):
        try:
            response = model.generate_content("Dame un consejo corto de ahorro para un niño.")
            st.write(response.text)
        except:
            st.error("Revisa tu clave de IA en los Secrets.")

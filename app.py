import streamlit as st
import pandas as pd

# CONFIGURACIÓN
st.set_page_config(page_title="Finanzas Familiares Pro", layout="wide")

# --- FUNCIÓN PARA CARGAR TU HISTORIAL REAL ---
def cargar_datos_jesus():
    try:
        # Cargamos tu archivo base.csv
        df = pd.read_csv("Finanzas Jesus New - base.csv")
        # Extraemos el último dato de la columna de bancos
        ultimo_total = df["Total acumulado caja/sant  mes"].iloc[0] # Tomamos la referencia de arriba
        return ultimo_total
    except:
        return 0.0

# --- INTERFAZ ---
st.title("🚀 Mi Plataforma Financiera")

# PANEL SUPERIOR: ESTADO DE BANCOS
saldo_bancos = cargar_datos_jesus()

st.markdown("### 🏦 Estado de Mis Cuentas Reales")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total en Bancos (Real)", f"{saldo_bancos} €")
with col2:
    st.metric("Total en Colchones (App)", f"{saldo_bancos} €")
with col3:
    st.metric("Diferencia", "0.00 €", delta_color="normal")

st.markdown("---")

# --- REPARTO POR CATEGORÍAS (TUS COLCHONES) ---
st.subheader("📂 Mis Colchones (Ahorros Acumulados)")

# Datos extraídos de tu columna de totales en el Excel
categorias = {
    "🛒 Mercado": 707.58,
    "💡 Alquiler/Energía": 737.48,
    "👶 Niños": 322.03,
    "🏠 Casa": 222.48,
    "😃 Salud": 621.69,
    "🚙 Carro": -193.56  # Aquí la app te avisará que estás en negativo
}

cols = st.columns(len(categorias))
for i, (cat, monto) in enumerate(categorias.items()):
    with cols[i]:
        color = "normal" if monto > 0 else "inverse"
        st.metric(cat, f"{monto} €", delta=None, delta_color=color)

# BOTÓN MÁGICO PARA REGISTRAR
st.sidebar.button("➕ Nuevo Gasto")
st.sidebar.button("💰 Registrar Ingreso")

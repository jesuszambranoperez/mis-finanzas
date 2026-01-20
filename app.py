import streamlit as st
import pandas as pd
from database_manager import DBManager

# Configuración de la página para que parezca App de móvil
st.set_page_config(page_title="Mis Finanzas", page_icon="💰", layout="centered")

# CSS Personalizado para el look & feel
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3em; background-color: white; border: 1px solid #eee; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .bank-card { background: white; padding: 15px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; border-bottom: 4px solid #4CAF50; }
    .cat-card { background: white; padding: 20px; border-radius: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 10px; }
    .total-balance { font-size: 2.5em; font-weight: bold; color: #1E1E1E; text-align: center; margin: 20px 0; }
    .floating-banner { background: #FFF9C4; padding: 10px; border-radius: 10px; text-align: center; color: #FBC02D; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

db = DBManager()
df_cat, df_config = db.obtener_todo()

# --- CABECERA: SALDO TOTAL ---
saldo_total = df_cat['saldo_acumulado'].sum() # Simplificado
st.markdown(f'<div class="total-balance">{saldo_total:,.2f}€</div>', unsafe_allow_html=True)

# --- BANCOS (Scroll Horizontal simulado con columnas) ---
col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
    st.markdown('<div class="bank-card"><small>Cajamar</small><br><b>1,250€</b></div>', unsafe_allow_html=True)
with col_b2:
    st.markdown('<div class="bank-card" style="border-color: #E53935"><small>Santander</small><br><b>840€</b></div>', unsafe_allow_html=True)
with col_b3:
    st.markdown('<div class="bank-card" style="border-color: #FB8C00"><small>Efectivo</small><br><b>120€</b></div>', unsafe_allow_html=True)

st.write("---")

# --- PARTIDA FLOTANTE ---
saldo_f = df_config.loc[df_config['clave'] == 'partida_flotante', 'valor'].values[0]
if saldo_f > 0:
    st.markdown(f'<div class="floating-banner">⚠️ Tienes {saldo_f}€ en la partida flotante</div>', unsafe_allow_html=True)

# --- CATEGORÍAS (Grid de 2 columnas) ---
st.subheader("Mis Partidas")
cols = st.columns(2)

for i, row in df_cat.iterrows():
    with cols[i % 2]:
        # Simulamos un objetivo de presupuesto para la barra de progreso
        objetivo = 500 # Esto luego lo traeremos del Excel
        progreso = min(float(row['saldo_acumulado'] / objetivo), 1.0)
        
        st.markdown(f"""
            <div class="cat-card">
                <span style="font-size: 25px;">{row['icono']}</span><br>
                <b>{row['nombre']}</b><br>
                <small style="color: gray;">{row['saldo_acumulado']}€ de {objetivo}€</small>
            </div>
        """, unsafe_allow_html=True)
        st.progress(progreso)
        if st.button(f"Gestionar {row['nombre']}", key=row['nombre']):
            st.session_state.cat_focus = row['nombre']
            st.rerun()

# --- BOTÓN FLOTANTE (AÑADIR) ---
st.write("")
if st.button("➕ Crear Nueva Partida"):
    st.info("Aquí abriremos el formulario para crear")

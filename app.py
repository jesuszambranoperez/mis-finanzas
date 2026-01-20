import streamlit as st
import pandas as pd
from database_manager import DBManager

# Configuración de página estilo móvil
st.set_page_config(page_title="Mis Finanzas", layout="centered")

# CSS para imitar tu diseño de Illustrator
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .total-header { text-align: center; padding: 20px; font-size: 42px; font-weight: bold; color: #333; }
    .bank-box { background: white; border-radius: 10px; padding: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .cajamar { color: #00a896; border-bottom: 3px solid #00a896; }
    .santander { color: #ec1c24; border-bottom: 3px solid #ec1c24; }
    .efectivo { color: #8bc34a; border-bottom: 3px solid #8bc34a; }
    .card { background: white; border-radius: 15px; padding: 15px; margin-bottom: 10px; border: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

db = DBManager()
df_cat, df_config = db.obtener_todo()

# 1. SALDO TOTAL (Maqueta 2)
st.markdown('<div class="total-header">4600 €</div>', unsafe_allow_html=True)

# 2. BANCOS (Maqueta 2)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="bank-box cajamar"><small>4200€</small><br><b>Cajamar</b></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="bank-box santander"><small>250€</small><br><b>Santander</b></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="bank-box efectivo"><small>150€</small><br><b>Efectivo</b></div>', unsafe_allow_html=True)

st.write("---")

# 3. CATEGORÍAS (Tu lista de Alquiler, Mercado, etc.)
st.subheader("Categorías")

for _, row in df_cat.iterrows():
    with st.container():
        # Usamos columnas para los botones de subir/bajar de tu diseño
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            st.markdown(f"""
                <div style="line-height:1">
                    <b style="font-size:18px">{row['nombre']}</b><br>
                    <small style="color:gray">Disponible: {row['saldo_acumulado']}€</small>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.button("↗️", key=f"up_{row['nombre']}") # Botón Egreso
        with c3:
            st.button("↙️", key=f"down_{row['nombre']}") # Botón Ingreso
        st.markdown('<hr style="margin:10px 0">', unsafe_allow_html=True)

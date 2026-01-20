import streamlit as st

# 1. ESTILO VISUAL (Colores y formas de tus diseños)
st.set_page_config(page_title="Mi App Financiera", layout="centered")

st.markdown("""
    <style>
    .balance-header { text-align: center; font-size: 40px; font-weight: bold; color: #333; margin: 10px 0; }
    .bank-card { background: white; border-radius: 12px; padding: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-bottom: 5px solid; }
    .cat-card { background: white; border-radius: 15px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# 2. CABECERA
st.markdown('<div class="balance-header">4.600 €</div>', unsafe_allow_html=True)

# 3. TUS BANCOS
c1, c2, c3 = st.columns(3)
c1.markdown('<div class="bank-card" style="border-color:#00a896"><small>4.200€</small><br><b>Cajamar</b></div>', unsafe_allow_html=True)
c2.markdown('<div class="bank-card" style="border-color:#ec1c24"><small>250€</small><br><b>Santander</b></div>', unsafe_allow_html=True)
c3.markdown('<div class="bank-card" style="border-color:#8bc34a"><small>150€</small><br><b>Efectivo</b></div>', unsafe_allow_html=True)

st.write("---")

# 4. TUS CATEGORÍAS
st.subheader("Mis Partidas")

# Datos de prueba para que veas el resultado
categorias = [
    {"n": "Alquiler", "i": "🏠", "m": 250},
    {"n": "Mercado", "i": "🛒", "m": 120},
    {"n": "Salud", "i": "💊", "m": 45},
    {"n": "Sexo", "i": "🥒", "m": 45000000}
]

for cat in categorias:
    with st.container():
        col_info, col_btn = st.columns([4, 1])
        with col_info:
            st.markdown(f'<div class="cat-card"><span>{cat["i"]} <b>{cat["n"]}</b></span> <span style="color:#00a896">{cat["m"]}€</span></div>', unsafe_allow_html=True)
        with col_btn:
            st.button("↗️", key=cat["n"])

# 5. BOTÓN AÑADIR
st.button("➕ Crear Nueva Partida", use_container_width=True)

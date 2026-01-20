import streamlit as st

# Configuración de estilo móvil
st.set_page_config(page_title="Mis Finanzas", layout="centered")

# CSS para imitar tu diseño de Illustrator al detalle
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #F2F2F2; }
    .main-balance { text-align: center; font-size: 3rem; font-weight: 700; color: #333; margin: 10px 0; }
    .bank-card { background: white; border-radius: 12px; padding: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .cajamar { border-bottom: 5px solid #00a896; color: #00a896; }
    .santander { border-bottom: 5px solid #ec1c24; color: #ec1c24; }
    .efectivo { border-bottom: 5px solid #8bc34a; color: #8bc34a; }
    .cat-card { background: white; border-radius: 18px; padding: 15px; margin-bottom: 10px; border: 1px solid #E0E0E0; }
    .btn-action { border-radius: 50% !important; width: 40px; height: 40px; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA (Tu diseño de Illustrator) ---
st.markdown('<div class="main-balance">4.600 €</div>', unsafe_allow_html=True)

# BANCOS
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="bank-card cajamar"><small>4.200€</small><br><b>Cajamar</b></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="bank-card santander"><small>250€</small><br><b>Santander</b></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="bank-card efectivo"><small>150€</small><br><b>Efectivo</b></div>', unsafe_allow_html=True)

st.write("##")

# --- CATEGORÍAS ---
st.subheader("Categorías")

# Datos de ejemplo basados en tu Excel
categorias = [
    {"n": "Alquiler", "i": "🏠", "s": 250, "m": 430},
    {"n": "Mercado", "i": "🛒", "s": 120, "m": 300},
    {"n": "Salud", "i": "💊", "s": 50, "m": 100}
]

for cat in categorias:
    with st.container():
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            st.markdown(f"""
                <div class="cat-card">
                    <span style="font-size:1.2rem">{cat['i']} <b>{cat['n']}</b></span><br>
                    <small style="color:gray">Disponible: {cat['s']}€ / {cat['m']}€</small>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            if st.button("↗️", key=f"eg_{cat['n']}"):
                st.toast(f"Registrar gasto en {cat['n']}")
        with c3:
            if st.button("↙️", key=f"in_{cat['n']}"):
                st.toast(f"Registrar ingreso en {cat['n']}")

# BOTÓN FLOTANTE
st.write("##")
st.button("➕ Crear Nueva Partida", use_container_width=True)

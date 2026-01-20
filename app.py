import streamlit as st

# 1. CONFIGURACIÓN DE LA APP
st.set_page_config(page_title="Mi App Financiera", layout="centered")

# 2. EL "MAQUILLAJE" (CSS para que se vea como tu diseño)
st.markdown("""
    <style>
    .main { background-color: #f2f2f2; }
    .balance-header { text-align: center; font-size: 45px; font-weight: 800; color: #333; margin-bottom: 5px; }
    .bank-row { display: flex; justify-content: space-between; margin-bottom: 25px; }
    .bank-card { background: white; border-radius: 12px; padding: 10px; width: 30%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .cajamar { border-bottom: 5px solid #00a896; }
    .santander { border-bottom: 5px solid #ec1c24; }
    .efectivo { border-bottom: 5px solid #8bc34a; }
    .card-category { background: white; border-radius: 15px; padding: 15px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .symbol { font-size: 24px; margin-right: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. CABECERA: SALDO TOTAL
st.markdown('<div class="balance-header">4.600 €</div>', unsafe_allow_html=True)

# 4. BANCOS (Como en tus cuadros de Illustrator)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="bank-card cajamar"><small>4.200€</small><br><b>Cajamar</b></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="bank-card santander"><small>250€</small><br><b>Santander</b></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="bank-card efectivo"><small>150€</small><br><b>Efectivo</b></div>', unsafe_allow_html=True)

st.write("---")

# 5. CATEGORÍAS (Tus "sobres")
st.subheader("Mis Partidas")

# Lista de tus categorías (Datos de prueba para ver el diseño)
categorias = [
    {"nombre": "Alquiler", "icono": "🏠", "monto": 250},
    {"nombre": "Mercado", "icono": "🛒", "monto": 120},
    {"nombre": "Salud", "icono": "💊", "monto": 45},
    {"nombre": "Ocio", "icono": "🍿", "monto": 80},
]

for cat in categorias:
    # Contenedor visual
    with st.container():
        c1, c2, c3 = st.columns([4, 1, 1])
        with c1:
            st.markdown(f"""
                <div class="card-category">
                    <div><span class="symbol">{cat['icono']}</span><b>{cat['nombre']}</b></div>
                    <div style="color: #00a896;">{cat['monto']}€</div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            # Botón de Gasto (Flecha de tu diseño)
            if st.button("↗️", key=f"out_{cat['nombre']}"):
                st.warning(f"Registrando gasto en {cat['nombre']}...")
        with c3:
            # Botón de Ingreso (Flecha de tu diseño)
            if st.button("↙️", key=f"in_{cat['nombre']}"):
                st.success(f"Añadiendo dinero a {cat['nombre']}...")

# 6. BOTÓN FLOTANTE AL FINAL
st.write("##")
if st.button("➕ Crear Nueva Partida", use_container_width=True):
    st.info("¡Aquí abriríamos el formulario para crear una nueva!")

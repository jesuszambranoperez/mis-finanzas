import streamlit as st

# Configuración inicial
st.set_page_config(page_title="Mi Control Financiero", layout="wide")

# Cargar el CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- CABECERA: SALDO GLOBAL ---
st.markdown('<div class="main-balance">', unsafe_allow_html=True)
st.markdown("### Saldo Disponible Total")
st.markdown("## 4.645,76 €")
st.markdown("</div>", unsafe_allow_html=True)

# --- CUENTAS BANCARIAS ---
col_b1, col_b2, col_b3 = st.columns(3)
col_b1.metric("🏦 Banco A", "2.100 €")
col_b2.metric("🏦 Banco B", "2.445 €")
col_b3.metric("💵 Efectivo", "100 €")

st.markdown("---")

# --- GRID DE PARTIDAS (UX intuitiva) ---
st.subheader("Tus Partidas")

# Definimos las partidas con sus iconos y nombres
partidas = [
    ("🏠", "Alquiler/Energía"), ("🛒", "Mercado"), ("🏡", "Casa"),
    ("🥂", "Gustos"), ("🏥", "Salud"), ("💰", "Ahorros"),
    ("⚠️", "Imprevistos"), ("🚗", "Carro"), ("👴", "Mamá/Papá"),
    ("👫", "Hermanos"), ("👦", "Niños")
]

# Creamos una cuadrícula de 2 columnas para móvil
cols = st.columns(2)
for i, (icon, name) in enumerate(partidas):
    with cols[i % 2]:
        if st.button(f"{icon}\n{name}\n450 €", key=name):
            st.session_state.partida_seleccionada = name

# --- PANEL DE ACCIÓN (Aparece al tocar una partida) ---
if 'partida_seleccionada' in st.session_state:
    st.markdown(f"### ✏️ Registrar en: {st.session_state.partida_seleccionada}")
    c1, c2 = st.columns(2)
    monto = c1.number_input("Monto (€)", min_value=0.0, step=1.0)
    tipo = c2.radio("Tipo", ["Gasto (-)", "Ingreso (+)"])
    
    if st.button(f"Guardar en {st.session_state.partida_seleccionada}"):
        st.success(f"Registrado: {monto}€ como {tipo}")

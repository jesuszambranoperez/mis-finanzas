import streamlit as st
import google.generativeai as genai

# Esto busca la clave que pegaste en Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

# --- CONFIGURACIÓN ESTÉTICA (CSS) ---
st.set_page_config(page_title="Finanzas Familiares", layout="wide")

st.markdown("""
    <style>
    /* Estilo para que parezca una App de móvil */
    .main { background-color: #f0f2f6; }
    div.stButton > button {
        border-radius: 15px;
        height: 60px;
        font-weight: bold;
        font-size: 18px;
        background-color: #ffffff;
        border: 2px solid #007bff;
        transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #007bff; color: white; }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN PRIVADA A DRIVE ---
# Nota: Usaremos el link de Google Sheets de forma segura más adelante
conn = st.connection("gsheets", type=GSheetsConnection)

# --- MENÚ DE NAVEGACIÓN (Diseño intuitivo) ---
st.title("🏡 Mi Economía Familiar")
menu = st.tabs(["📊 Mi Estado", "👩 Ingreso Variable", "👦 Modo Aprendiz"])

# --- PESTAÑA 1: ESTADO REAL (JESÚS) ---
with menu[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Tu Dinero Hoy")
    c1, c2 = st.columns(2)
    c1.metric("Bancos Total", "4.645,76 €")
    c2.metric("Ahorro del Mes", "+120 €", delta="12%")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### Mis Colchones")
    col_a, col_b, col_c = st.columns(3)
    with col_a: st.info("🛒 Mercado: 700€")
    with col_b: st.info("🏠 Alquiler: 730€")
    with col_c: st.warning("🚙 Coche: -193€")

# --- PESTAÑA 2: ESPOSA (VARIABLE) ---
with menu[1]:
    st.subheader("Reparto Proporcional")
    monto = st.number_input("¿Cuánto ingresó este mes?", min_value=0.0)
    if monto > 0:
        st.write("Sugerencia de reparto (Basado en tus reglas):")
        st.write(f"✅ Ahorro (30%): {monto*0.3:.2f}€")
        st.write(f"✅ Gastos (70%): {monto*0.7:.2f}€")

# --- PESTAÑA 3: NIÑOS (INTELIGENCIA FINANCIERA) ---
with menu[2]:
    st.subheader("👦 ¡Hola! Vamos a aprender")
    st.write("¿Qué quieres conseguir hoy?")
    meta = st.selectbox("Mi meta es:", ["Un juguete", "Ahorrar para el futuro", "Ayudar a alguien"])
    
    # Aquí es donde conectaremos la IA de Google Gemini
    if st.button("Pedir consejo a mi Guía Financiero"):
        st.write("🤖 *La IA está analizando tu hucha...*")
        st.success("Consejo: Si guardas la mitad de tu paga este domingo, ¡llegarás a tu meta antes del próximo cumpleaños!")

st.sidebar.markdown("---")
st.sidebar.write("Versión Gratuita 1.0")

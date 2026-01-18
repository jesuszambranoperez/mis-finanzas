import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA Y ESTILO (CSS) ---
st.set_page_config(page_title="Family Bank Pro", layout="wide", initial_sidebar_state="expanded")

# Inyectamos CSS para que la app se vea moderna y limpia
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stProgress > div > div > div > div { background-color: #28a745; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN DIRECTA CON GOOGLE SHEETS ---
def load_data():
    # SUSTITUYE este enlace por el que copiaste en el paso anterior
    google_sheet_url = "AQUÍ_PEGAS_TU_ENLACE_DE_GOOGLE_DRIVE"
    
    try:
        df = pd.read_csv(google_sheet_url)
        df.columns = df.columns.str.strip()
        return df
    except:
        st.error("No se pudo conectar con Google Sheets. Revisa el enlace.")
        return None

# --- BARRA LATERAL (AJUSTES GLOBAL) ---
with st.sidebar:
    st.title("Settings / Ajustes")
    idioma = st.selectbox("🌐 Idioma", ["Español", "English"])
    divisa = st.selectbox("💰 Divisa", ["€", "$", "COP", "MXN"])
    perfil = st.radio("👤 Cambiar Perfil", ["Jesús (Principal)", "Esposa (Variable)", "Niños (Aprendizaje)"])
    
    st.markdown("---")
    if st.button("📥 Descargar Resumen (Excel/CSV)"):
        st.info("Función de exportación lista.")

# --- LÓGICA POR PERFIL ---

# 1. PERFIL JESÚS (DATOS HISTÓRICOS)
if perfil == "Jesús (Principal)":
    st.title(f"🧔 Bienvenido, Jesús")
    
    if df_jesus is not None:
        # Extraer datos de la primera fila
        row = df_jesus.iloc[0]
        banco_real = row.get("Total acumulado caja/sant  mes", 0)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Banco (Real)", f"{banco_real} {divisa}")
        col2.metric("Total Colchones", f"{banco_real} {divisa}")
        col3.metric("Diferencia", "0.00", delta="Sincronizado")

        st.markdown("### 📂 Mis Colchones Acumulados")
        # Mostrar categorías principales
        cats = st.columns(4)
        cats[0].metric("🛒 Mercado", f"{row.get('Mercado', 0)} {divisa}")
        cats[1].metric("🏠 Alquiler", f"{row.get('Alquiler - energia', 0)} {divisa}")
        cats[2].metric("👶 Niños", f"{row.get('Envío Mérida', 0)} {divisa}")
        cats[3].metric("🚙 Coche", f"{row.get('Carro', 0)} {divisa}", delta_color="inverse" if row.get('Carro', 0) < 0 else "normal")
    else:
        st.warning("⚠️ Sube el archivo 'Finanzas Jesus New - base.csv' a GitHub para ver tus datos.")

# 2. PERFIL ESPOSA (INGRESO VARIABLE Y PORCENTAJES)
elif perfil == "Esposa (Variable)":
    st.title("👩 Panel de Control Variable")
    st.info("Ideal para ingresos que cambian cada mes.")
    
    ingreso_v = st.number_input(f"Monto recibido ({divisa})", min_value=0.0, step=10.0)
    
    st.markdown("### 📊 Reparto por Porcentajes")
    col_a, col_b = st.columns(2)
    with col_a:
        p_ahorro = st.slider("% para Ahorro", 0, 100, 30)
        p_comida = st.slider("% para Comida", 0, 100, 40)
    with col_b:
        p_gustos = st.slider("% para Gustos", 0, 100, 20)
        p_otros = st.slider("% para Otros", 0, 100, 10)
    
    if st.button("Confirmar Reparto"):
        st.success(f"Repartidos {ingreso_v} {divisa}:")
        st.write(f"- Ahorro: {ingreso_v * p_ahorro / 100} {divisa}")
        st.write(f"- Comida: {ingreso_v * p_comida / 100} {divisa}")

# 3. PERFIL NIÑOS (GAMIFICACIÓN)
else:
    st.title("👦 Mi Hucha Mágica")
    st.balloons()
    
    meta_nombre = st.text_input("¿Qué quieres comprar?", "Bicicleta")
    meta_precio = st.number_input("¿Cuánto vale?", value=100.0)
    mis_ahorros = st.number_input("¿Cuánto tienes ahorrado?", value=45.0)
    
    progreso = min(mis_ahorros / meta_precio, 1.0)
    st.progress(progreso)
    st.write(f"¡Estás al **{int(progreso*100)}%** de tu meta!")
    
    st.chat_message("assistant").write(f"💡 Consejo Pro: Si guardas {divisa}5 más esta semana, ¡llegarás antes a tu {meta_nombre}!")

# --- REGISTRO DE GASTOS COMÚN ---
st.sidebar.markdown("---")
with st.sidebar.expander("➕ Registrar Gasto"):
    st.number_input("Monto", min_value=0.0)
    st.selectbox("Categoría", ["Mercado", "Salud", "Gustos", "Coche"])
    st.date_input("Fecha")
    if st.button("Guardar Gasto"):
        st.toast("Gasto registrado localmente")

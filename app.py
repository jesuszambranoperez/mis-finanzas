import streamlit as st
import pandas as pd
from database_manager import DBManager

# 1. CONFIGURACIÓN E INTERFAZ
st.set_page_config(page_title="Family Bank Pro", layout="wide", initial_sidebar_state="collapsed")

# Estilo personalizado (puedes moverlo a styles.css si prefieres)
st.markdown("""
    <style>
    .stButton > button {
        border-radius: 15px;
        height: 120px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #3b82f6;
    }
    .floating-banner {
        background-color: #fef3c7;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #f59e0b;
        margin-bottom: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZACIÓN
# Busca esta parte y déjala así:
try:
    db = DBManager()
    df_cat, df_config = db.obtener_todo()
    saldo_flotante = df_config.loc[df_config['clave'] == 'partida_flotante', 'valor'].values[0]
except Exception as e:
    st.error(f"Error real detectado: {e}") # Esto nos dirá qué pasa exactamente
    st.stop()

# 3. CABECERA: SALDO GLOBAL
st.title("🛡️ Mi Control Financiero")
total_disponible = df_cat['saldo_acumulado'].sum() + saldo_flotante
st.metric("Saldo Global Disponible", f"{total_disponible:,.2f} €")

# 4. ALERTA: PARTIDA FLOTANTE
if saldo_flotante > 0:
    st.markdown(f'''
        <div class="floating-banner">
            <h4 style="margin:0;color:#92400e;">📦 Dinero en Tránsito: {saldo_flotante:,.2f} €</h4>
            <p style="margin:0;color:#b45309;">Este dinero proviene de categorías eliminadas o ajustes.</p>
        </div>
    ''', unsafe_allow_html=True)
    
    with st.expander("🔄 Repartir Dinero en Tránsito"):
        col_t1, col_t2 = st.columns(2)
        destino = col_t1.selectbox("Enviar a:", df_cat['nombre'].tolist())
        monto_t = col_t2.number_input("Cantidad a mover", min_value=0.0, max_value=float(saldo_flotante))
        if st.button("Confirmar Transferencia"):
            # Aquí llamaríamos a una función de transferencia en db_manager
            st.success("Transferencia realizada (pendiente vincular lógica)")

# 5. CUADRÍCULA DE PARTIDAS
st.write("### Mis Partidas")
cols = st.columns(2) # Ideal para vista móvil

for i, (index, row) in enumerate(df_cat.iterrows()):
    with cols[i % 2]:
        # Botón con Icono, Nombre y Saldo
        label = f"{row['icono']} {row['nombre']}\n\n{row['saldo_acumulado']:.2f} €"
        if st.button(label, key=f"btn_{row['nombre']}"):
            st.session_state.cat_focus = row['nombre']

# 6. PANEL DE ACCIÓN (Aparece al tocar una partida)
if 'cat_focus' in st.session_state:
    st.markdown("---")
    st.subheader(f"Gestión: {st.session_state.cat_focus}")
    
    c1, c2, c3 = st.columns([2, 1, 1])
    monto = c1.number_input("Monto", min_value=0.0)
    
    if c2.button("➕ Ingreso"):
        st.success(f"Sumado a {st.session_state.cat_focus}")
        # Aquí llamarías a db.actualizar_saldo(cat, monto)
        
    if c3.button("🗑️ Borrar Categoría"):
        db.eliminar_y_flotar(st.session_state.cat_focus)
        st.warning(f"Categoría eliminada. Dinero movido a tránsito.")
        st.rerun()

# 7. BARRA LATERAL: ADMIN
with st.sidebar:
    st.header("⚙️ Configuración")
    new_name = st.text_input("Nombre nueva categoría")
    new_icon = st.text_input("Icono (Emoji)", value="💰")
    if st.button("➕ Crear Categoría"):
        db.guardar_nueva_categoria(new_name, new_icon)
        st.rerun()

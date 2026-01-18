import streamlit as st

# Configuración básica
st.set_page_config(page_title="Finanzas Familiares", page_icon="💰")

# Título y bienvenida
st.title("💰 Mi App de Finanzas Familiar")
st.write("¡Bienvenido Jesús! Esta es la base de tu nueva herramienta.")

# Menú lateral para elegir quién usa la app
perfil = st.sidebar.radio("¿Quién está usando la App?", ["Jesús", "Esposa", "Niños"])

if perfil == "Jesús":
    st.header("🧔 Panel de Jesús")
    st.metric("Saldo Estimado", "4.645,76 €")
    st.info("Aquí verás tus colchones del Excel pronto.")

elif perfil == "Esposa":
    st.header("👩 Panel de Control Variable")
    ingreso = st.number_input("Ingresa el monto de este mes", value=0.0)
    st.write(f"Si ingresas {ingreso}, se repartirá según tus porcentajes.")

else:
    st.header("👦 Mi Hucha Mágica")
    st.write("¡Ahorra para tus juguetes!")
    st.progress(60)
    st.success("¡Vas por muy buen camino!")

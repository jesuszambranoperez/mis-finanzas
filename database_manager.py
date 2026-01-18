import requests # Asegúrate de tener 'requests' en tu requirements.txt

def guardar_nueva_categoria(self, nombre, icono):
    # La URL que copiaste en el paso anterior
    script_url = "TU_URL_DE_APPS_SCRIPT_AQUI"
    
    # Obtenemos el último ID para el nuevo registro
    df_cats, _ = self.obtener_todo()
    nuevo_id = int(df_cats['id'].max() + 1) if not df_cats.empty else 1
    
    payload = {
        "accion": "crear",
        "pestaña": "Categorias",
        "id": nuevo_id,
        "nombre": nombre,
        "icono": icono
    }    
    try:
        response = requests.post(script_url, json=payload)
        if response.status_code == 200:
            st.success("¡Categoría creada con éxito!")
            st.cache_data.clear()
            st.rerun()
    except Exception as e:
        st.error(f"Error al enviar datos: {e}")

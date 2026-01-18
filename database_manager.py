import requests # Asegúrate de tener 'requests' en tu requirements.txt

def guardar_nueva_categoria(self, nombre, icono):
   # Dentro de la función guardar_nueva_categoria
script_url = "https://script.google.com/macros/s/AKfycbzoRD9xRb0aNWW4DgxKh9J9vzQ0a_lrsN3-it7G0LrWE4v2wstPU5X5rU9GUAjt7_4F/exec"
    
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

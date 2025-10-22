# src/streamlit_app.py

import streamlit as st
import requests

# ----------------------------------------------------
# 1. CONFIGURACIÓN DEL FRONTEND
# ----------------------------------------------------
st.set_page_config(
    page_title="Predictor de Costos de Seguro",
    layout="wide"
)

st.title("🏥 Predictor de Costos de Seguro Médico")
st.markdown("Modelo de Random Forest para estimar el gasto anual de póliza.")

# Definir la URL de la API de FastAPI que se desplegará en Render
# NOTA: Reemplazar 'YOUR_RENDER_URL' con la URL real de tu API de Render (Paso 2)
API_URL = "https://predictor-costos-aseguradora.onrender.com" # Temporalmente local

# ----------------------------------------------------
# 2. FORMULARIO DE ENTRADA DE DATOS
# ----------------------------------------------------

with st.form("prediction_form"):
    st.header("Datos del Paciente")
    
    # Filas de la interfaz para organizar mejor los inputs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Edad", min_value=18, max_value=100, value=30, step=1)
        bmi = st.number_input("Índice de Masa Corporal (BMI)", min_value=15.0, max_value=50.0, value=25.0, step=0.1)
        
    with col2:
        sex = st.selectbox("Género", ["male", "female"])
        smoker = st.selectbox("Fumador", ["no", "yes"])
        
    with col3:
        children = st.number_input("Hijos", min_value=0, max_value=5, value=0, step=1)
        region = st.selectbox("Región", ["southwest", "southeast", "northwest", "northeast"])
        
    # Botón de predicción
    submitted = st.form_submit_button("Estimar Costo")

# ----------------------------------------------------
# 3. LÓGICA DE PREDICCIÓN
# ----------------------------------------------------
if submitted:
    # 1. Construir el JSON de datos
    data_to_send = {
        "age": age,
        "sex": sex,
        "bmi": bmi,
        "children": children,
        "smoker": smoker,
        "region": region
    }
    
    try:
        # 2. Enviar la solicitud POST a la API de FastAPI
        # IMPORTANTE: En el despliegue real, esta URL será tu API de Render
        response = requests.post(API_URL, json=data_to_send)
        
        if response.status_code == 200:
            result = response.json()
            cost = result.get("predicted_charge_usd")
            
            # 3. Mostrar el resultado
            st.success("Predicción Exitosa")
            st.metric(label="Costo Anual Estimado", value=f"${cost:,.2f}")
            
            # Sugerencia basada en tu feature importance (Subtema 2)
            if smoker == "yes":
                st.warning("🚨 Recordatorio: Ser fumador es el factor más importante en el costo de la póliza.")
                
        else:
            st.error(f"Error en la API: {response.status_code}. Mensaje: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Error de Conexión. Asegúrate de que la API de FastAPI esté desplegada y la URL sea correcta.")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
from .utils import load_artifacts, preprocess_data 

# Inicializar FastAPI
app = FastAPI(
    title="Insurance Cost Predictor API",
    description="API para predecir costos de seguro médico usando un modelo Random Forest (Log-Transformado)."
)

# ----------------------------------------------------
# 1. ESQUEMA DE DATOS (Pydantic)
# Define la estructura y tipos de datos esperados para la entrada de la API.
# ----------------------------------------------------
class PatientData(BaseModel):
    age: int
    sex: str  # 'male' o 'female'
    bmi: float
    children: int
    smoker: str  # 'yes' o 'no'
    region: str  # 'southwest', 'southeast', 'northwest', 'northeast'
    
# ----------------------------------------------------
# 2. CARGA DE ARTEFACTOS DEL MODELO
# Carga el modelo y las columnas al inicio para evitar recargar en cada solicitud.
# ----------------------------------------------------
model, model_columns = load_artifacts()

# ----------------------------------------------------
# 3. ENDPOINT DE PREDICCIÓN
# ----------------------------------------------------
@app.post("/predict_cost")
def predict_insurance_cost(data: PatientData):
    """
    Realiza una predicción del costo del seguro médico (Charges)
    basada en la información del paciente.
    """
    if model is None or model_columns is None:
        return {"error": "Modelo no cargado. Revisa la ruta de los artefactos."}

    try:
        # Convertir datos de entrada a diccionario y preprocesar
        input_data = data.dict()
        
        # Usar la función de preprocesamiento de utils.py
        processed_df = preprocess_data(input_data, model_columns)
        
        # 1. Predicción en escala logarítmica (El modelo fue entrenado con log(charges))
        prediction_log = model.predict(processed_df)
        
        # 2. Deshacer la transformación logarítmica para obtener el valor original (np.expm1)
        # np.expm1(x) = exp(x) - 1. Es la inversa de np.log1p(x) = log(1+x)
        prediction_charge = np.expm1(prediction_log)[0]
        
        return {
            "predicted_charge_usd": round(prediction_charge, 2),
            "model_used": "Random Forest Regressor (Log-Transform)",
            "input_data": input_data
        }
    
    except Exception as e:
        return {"error": f"Ocurrió un error durante la predicción: {e}"}

# ----------------------------------------------------
# 4. RUTA DE INICIO (Opcional, para verificar salud de la API)
# ----------------------------------------------------
@app.get("/")
def read_root():
    return {"message": "API de Predicción de Costos de Seguro (FastAPI) está funcionando."}
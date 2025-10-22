import pandas as pd
import numpy as np
import joblib

# Definición de la lógica de categorización de BMI
def categorize_bmi(bmi):
    """Categoriza el valor de BMI en 'bajo peso', 'normal', 'sobrepeso' u 'obesidad'."""
    if bmi < 18.5:
        return 'bajo peso'
    elif 18.5 <= bmi < 25:
        return 'normal'
    elif 25 <= bmi < 30:
        return 'sobrepeso'
    else:
        return 'obesidad'

def load_artifacts(path='model_artifacts/'):
    """Carga el modelo entrenado y la lista de columnas usadas para el entrenamiento."""
    try:
        model = joblib.load(path + 'modelo_rf_log.pkl')
        columns = joblib.load(path + 'columnas_modelo.pkl')
        return model, columns
    except FileNotFoundError:
        print("Error: Asegúrate de que los archivos 'modelo_rf_log.pkl' y 'columnas_modelo.pkl' estén en la carpeta especificada.")
        return None, None

def preprocess_data(data: dict, model_columns: list) -> pd.DataFrame:
    """
    Realiza todas las transformaciones necesarias a los datos de entrada
    para que coincidan con el formato usado durante el entrenamiento del modelo.
    """
    # ----------------------------------------------------
    # 1. Convertir el diccionario de entrada a un DataFrame
    # ----------------------------------------------------
    df = pd.DataFrame([data])

    # ----------------------------------------------------
    # 2. Mapeo de variables binarias
    # ----------------------------------------------------
    df['sex'] = df['sex'].map({'male': 0, 'female': 1})
    df['smoker'] = df['smoker'].map({'yes': 1, 'no': 0})

    # ----------------------------------------------------
    # 3. Creación de bmi_category (solo si el modelo lo hubiera requerido)
    # ----------------------------------------------------
    df['bmi_category'] = df['bmi'].apply(categorize_bmi)
    df.drop('bmi_category', axis=1, inplace=True) # El modelo entrenado no la usa

    # ----------------------------------------------------
    # 4. One-Hot Encoding para la región
    # ----------------------------------------------------
    df = pd.get_dummies(df, columns=['region'], prefix='region', drop_first=True)

    # ----------------------------------------------------
    # 5. Estandarización de columnas
    # Asegura que el DataFrame de entrada tenga las mismas columnas que el modelo vio en el entrenamiento.
    # ----------------------------------------------------

    # Crea un DataFrame vacío con las columnas del modelo
    final_df = pd.DataFrame(columns=model_columns, index=df.index)
    
    # Copia los valores de las columnas existentes
    for col in final_df.columns:
        if col in df.columns:
            # Asegura que las columnas booleanas de get_dummies sean 0 o 1
            if df[col].dtype == 'bool':
                final_df[col] = df[col].astype(int)
            else:
                final_df[col] = df[col]
        else:
            # Rellena con 0 las columnas de región que no existen en la entrada
            # (Ej: si la entrada no tiene 'region_northwest', se asume 0)
            final_df[col] = 0
            
    # Convierte todas las columnas a tipo numérico para la predicción
    final_df = final_df.astype(float)
    
    return final_df
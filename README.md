# 🏥 Predictor de Costos de Seguro Médico (MLOps End-to-End)

Este proyecto demuestra un flujo de trabajo completo de Machine Learning (MLOps), desde el análisis de datos hasta el despliegue de un microservicio RESTful en la nube. El objetivo es predecir los costos de póliza de seguro médico anuales utilizando datos demográficos y de salud.

---

## 🎯 Demostración e Interacción

| Enlace | Descripción |
| :--- | :--- |
| **🔗 DEMO INTERACTIVA** | **[Haz clic aquí para interactuar con la aplicación](https://predictorcostosaseguradora-kom2nuhrstxlprhcimkhjg.streamlit.app/)** |
| **💻 Repositorio** | [Haz clic aquí para interactuar ir al repositorio](https://github.com/cdavidps/Predictor_costos_aseguradora/tree/main) |

---

## 🚀 Arquitectura MLOps y Stack Tecnológico

El proyecto está diseñado con una arquitectura desacoplada para demostrar un flujo de trabajo de microservicios:

| Componente | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Entrenamiento** | Python (Pandas, Scikit-learn) | Limpieza de datos, Ingeniería de Características y Modelado. |
| **Backend/API** | **FastAPI** | Servicio RESTful de predicción. Carga el modelo y aplica el preprocesamiento necesario a la entrada. Desplegado en **Render**. |
| **Frontend/UI** | **Streamlit** | Interfaz de usuario interactiva para facilitar la entrada de datos y la visualización del resultado. Desplegado en **Streamlit Cloud**. |
| **Infraestructura** | **Render & Streamlit Cloud** | Plataformas *cloud-native* utilizadas para el despliegue gratuito y escalable. |
| **Gestión de Entorno**| **Conda / .python-version (3.9)** | Garantiza entornos de ejecución estables y aislados para evitar conflictos de dependencias. |

---

## 📈 Resultados y Conclusiones del Modelo

### Rendimiento del Modelo

Se utilizó un **Random Forest Regressor** con una **Transformación Logarítmica** en la variable objetivo (`charges`) para mejorar la linealidad de los datos.

| Métrica | Valor |
| :--- | :--- |
| **Modelo Final** | Random Forest Regressor |
| **R² (Coeficiente de Determinación)** | **0.8770** (En datos transformados) |
| **MAE (Error Absoluto Medio)** | $2085.10$ USD (En escala original) |

### 🔍 Descubrimiento Clave

El análisis de la **Importancia de Variables** reveló que el factor con el mayor impacto en la predicción del costo del seguro es:

1.  **Smoker (Fumador):** 38% de importancia relativa.
2.  **Age (Edad):** 36% de importancia relativa.

Esto subraya el valor de la Ciencia de Datos para identificar y cuantificar los principales *drivers* de riesgo en la industria de seguros.

---

## 🛠️ Guía de Ejecución Local

Si deseas probar o extender el código de la API localmente:

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/cdavidps/Predictor_costos_aseguradora.git
    ```

2.  **Crear y Activar el Entorno Conda (Recomendado):**
    ```bash
    conda create -n fastapi-deploy-39 python=3.9
    conda activate fastapi-deploy-39
    ```

3.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la API:**
    ```bash
    python -m uvicorn src.app:app --reload --app-dir src
    ```
    La API estará disponible en `http://127.0.0.1:8000/docs`.

---

### 📂 Estructura del Proyecto

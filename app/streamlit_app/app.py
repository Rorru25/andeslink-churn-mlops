import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


st.set_page_config(
    page_title="AndesLink - Predicción de Churn",
    page_icon="📊",
    layout="centered",
)


st.title("AndesLink - Predicción de Churn")

st.write(
    "Completá los datos del cliente para estimar "
    "la probabilidad de abandono."
)


with st.form("churn_form"):
    st.subheader("Datos del cliente")

    customer_age = st.number_input(
        "Edad del cliente",
        min_value=18,
        max_value=100,
        value=40,
        step=1,
    )

    tenure_months = st.number_input(
        "Antigüedad en meses",
        min_value=0,
        max_value=120,
        value=12,
        step=1,
    )

    monthly_charge = st.number_input(
        "Cargo mensual",
        min_value=0.0,
        value=60.0,
        step=1.0,
    )

    total_charges = st.number_input(
        "Cargos totales",
        min_value=0.0,
        value=720.0,
        step=10.0,
    )

    avg_monthly_usage_gb = st.number_input(
        "Uso mensual promedio en GB",
        min_value=0.0,
        value=80.0,
        step=1.0,
    )

    num_products = st.number_input(
        "Cantidad de productos contratados",
        min_value=1,
        value=2,
        step=1,
    )

    support_tickets = st.number_input(
        "Cantidad de tickets de soporte",
        min_value=0,
        value=1,
        step=1,
    )

    late_payments = st.number_input(
        "Cantidad de pagos atrasados",
        min_value=0,
        value=0,
        step=1,
    )

    contract_type = st.selectbox(
        "Tipo de contrato",
        ["mensual", "anual", "bianual"],
    )

    payment_method = st.selectbox(
        "Método de pago",
        [
            "credito",
            "debito",
            "efectivo",
            "transferencia",
        ],
    )

    internet_service = st.selectbox(
        "Servicio de internet",
        [
            "cable",
            "fibra",
            "movil",
            "ninguno",
        ],
    )

    region = st.selectbox(
        "Región",
        [
            "centro",
            "norte",
            "oeste",
            "sur",
        ],
    )

    has_streaming = st.selectbox(
        "¿Tiene servicio de streaming?",
        ["No", "Sí"],
    )

    has_security_pack = st.selectbox(
        "¿Tiene paquete de seguridad?",
        ["No", "Sí"],
    )

    is_promo = st.selectbox(
        "¿Tiene promoción activa?",
        ["No", "Sí"],
    )

    submitted = st.form_submit_button(
        "Predecir riesgo de churn"
    )


if submitted:
    customer_data = {
        "tenure_months": int(tenure_months),
        "monthly_charge": float(monthly_charge),
        "total_charges": float(total_charges),
        "support_tickets": int(support_tickets),
        "late_payments": int(late_payments),
        "avg_monthly_usage_gb": float(avg_monthly_usage_gb),
        "contract_type": contract_type,
        "payment_method": payment_method,
        "internet_service": internet_service,
        "has_streaming": 1 if has_streaming == "Sí" else 0,
        "has_security_pack": (
            1 if has_security_pack == "Sí" else 0
        ),
        "num_products": int(num_products),
        "region": region,
        "customer_age": int(customer_age),
        "is_promo": 1 if is_promo == "Sí" else 0,
    }

    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=customer_data,
            timeout=10,
        )

        if response.status_code == 200:
            result = response.json()

            prediction = result["prediction"]
            probability = result["churn_probability"]
            risk_level = result["risk_level"]
            model_name = result["model_name"]

            st.success("Predicción realizada correctamente")

            st.metric(
                "Probabilidad de churn",
                f"{probability * 100:.2f}%",
            )

            st.write(
                f"**Predicción:** "
                f"{'Abandona' if prediction == 1 else 'Permanece'}"
            )

            st.write(
                f"**Nivel de riesgo:** {risk_level.capitalize()}"
            )

            st.write(
                f"**Modelo utilizado:** {model_name}"
            )

            if risk_level == "alto":
                st.error(
                    "El cliente presenta un riesgo alto de abandono."
                )

            elif risk_level == "medio":
                st.warning(
                    "El cliente presenta un riesgo medio de abandono."
                )

            else:
                st.info(
                    "El cliente presenta un riesgo bajo de abandono."
                )

        else:
            st.error(
                f"La API devolvió un error "
                f"{response.status_code}: {response.text}"
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "No se pudo conectar con la API. "
            "Verificá que FastAPI esté ejecutándose "
            "en http://127.0.0.1:8000"
        )

    except requests.exceptions.Timeout:
        st.error(
            "La API tardó demasiado en responder."
        )

    except Exception as error:
        st.error(
            f"Ocurrió un error inesperado: {error}"
        )
        
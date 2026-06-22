from typing import Literal

from pydantic import BaseModel, Field


class ChurnInput(BaseModel):
    """
    Datos de entrada requeridos para realizar una predicción de churn.
    Los campos coinciden con las variables utilizadas durante el entrenamiento.
    """

    tenure_months: int = Field(
        ge=0,
        le=120,
        description="Antigüedad del cliente en meses",
        examples=[7],
    )

    monthly_charge: float = Field(
        ge=0,
        description="Cargo mensual del servicio",
        examples=[58.23],
    )

    total_charges: float = Field(
        ge=0,
        description="Importe total acumulado",
        examples=[326.50],
    )

    support_tickets: int = Field(
        ge=0,
        description="Cantidad de contactos o reclamos con soporte",
        examples=[2],
    )

    late_payments: int = Field(
        ge=0,
        description="Cantidad de pagos atrasados",
        examples=[1],
    )

    avg_monthly_usage_gb: float = Field(
        ge=0,
        description="Uso promedio mensual en GB",
        examples=[81.83],
    )

    contract_type: Literal["mensual", "anual", "bianual"] = Field(
        description="Tipo de contrato",
        examples=["mensual"],
    )

    payment_method: Literal[
        "credito",
        "debito",
        "efectivo",
        "transferencia",
    ] = Field(
        description="Método de pago",
        examples=["transferencia"],
    )

    internet_service: Literal[
        "cable",
        "fibra",
        "movil",
        "ninguno",
    ] = Field(
        description="Tipo de servicio de internet",
        examples=["cable"],
    )

    has_streaming: int = Field(
        ge=0,
        le=1,
        description="Indica si posee streaming: 0 = no, 1 = sí",
        examples=[0],
    )

    has_security_pack: int = Field(
        ge=0,
        le=1,
        description="Indica si posee paquete de seguridad: 0 = no, 1 = sí",
        examples=[1],
    )

    num_products: int = Field(
        ge=1,
        description="Cantidad de productos contratados",
        examples=[3],
    )

    region: Literal["centro", "norte", "oeste", "sur"] = Field(
        description="Región del cliente",
        examples=["centro"],
    )

    customer_age: int = Field(
        ge=18,
        le=100,
        description="Edad del cliente",
        examples=[53],
    )

    is_promo: int = Field(
        ge=0,
        le=1,
        description="Indica si posee promoción: 0 = no, 1 = sí",
        examples=[1],
    )


class ChurnPrediction(BaseModel):
    """
    Respuesta entregada por el endpoint de predicción.
    """

    prediction: int = Field(
        description="Predicción: 0 = permanece, 1 = churn"
    )

    churn_probability: float = Field(
        ge=0,
        le=1,
        description="Probabilidad estimada de abandono",
    )

    risk_level: Literal["bajo", "medio", "alto"] = Field(
        description="Nivel de riesgo calculado a partir de la probabilidad"
    )

    model_name: str = Field(
        description="Nombre del modelo utilizado"
    )


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    
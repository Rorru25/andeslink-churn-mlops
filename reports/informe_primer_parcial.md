# Informe técnico - Primer parcial

## 1. Introducción

Este informe documenta el desarrollo de una solución inicial de Machine Learning para la empresa ficticia AndesLink Servicios Digitales S.A., orientada a predecir el abandono de clientes (`churn`). La entrega corresponde a la primera etapa del proyecto MLOps local: comprensión del problema, análisis de datos, preparación, entrenamiento, evaluación, serialización y reproducibilidad inicial.

## 2. Contexto de negocio

AndesLink comercializa planes de suscripción mensual para servicios digitales. La cancelación voluntaria de clientes afecta los ingresos recurrentes, incrementa el costo de adquisición de nuevos usuarios y reduce la eficiencia de las campañas comerciales. Por este motivo, la empresa necesita identificar clientes con alta probabilidad de abandono para activar acciones de retención.

## 3. Objetivo analítico

El objetivo analítico es construir un modelo supervisado de clasificación binaria que prediga si un cliente abandonará el servicio. La variable objetivo es `churn`, donde `1` representa abandono y `0` representa permanencia.

## 4. Dataset

Se utiliza el archivo `churn_sintetico.csv`, compuesto por 5000 registros y 16 columnas. El dataset contiene variables relacionadas con antigüedad, facturación, uso del servicio, pagos, soporte, tipo de contrato, método de pago, región y características comerciales.

Variables principales:

- `tenure_months`: antigüedad del cliente en meses.
- `monthly_charge`: cargo mensual.
- `total_charges`: cargos acumulados.
- `support_tickets`: cantidad de reclamos o contactos con soporte.
- `late_payments`: pagos atrasados.
- `avg_monthly_usage_gb`: uso promedio mensual.
- `contract_type`: tipo de contrato.
- `payment_method`: método de pago.
- `internet_service`: tipo de servicio de internet.
- `churn`: variable objetivo.

El dataset es sintético. Esta elección es aceptable en el marco académico porque permite simular un caso de negocio realista y desarrollar un flujo MLOps completo sin utilizar datos sensibles de clientes reales.

## 5. Análisis exploratorio

El análisis exploratorio se encuentra en `notebooks/01_eda_churn.ipynb`. Se revisaron dimensiones del dataset, tipos de datos, valores nulos, distribución de la variable objetivo y relación entre churn y variables comerciales o de comportamiento.

Hallazgos esperados a documentar luego de ejecutar el notebook:

- Distribución de clientes que abandonan y no abandonan.
- Relación entre tipo de contrato y churn.
- Relación entre pagos atrasados, tickets de soporte y churn.
- Distribución de cargos mensuales y antigüedad.

## 6. Preparación de datos

La preparación se implementa mediante un `Pipeline` de scikit-learn. Las variables numéricas se imputan con mediana y se escalan con `StandardScaler`. Las variables categóricas se imputan con la categoría más frecuente y se codifican con `OneHotEncoder`. Esta estrategia permite que el mismo preprocesamiento utilizado en entrenamiento quede serializado junto al modelo final.

## 7. Modelos entrenados

Se compararon tres modelos supervisados de clasificación binaria:

1. Logistic Regression.
2. Random Forest Classifier.
3. Gradient Boosting Classifier.

La regresión logística funciona como modelo base interpretable. Random Forest y Gradient Boosting permiten capturar relaciones no lineales entre variables.

## 8. Métricas de evaluación

Se utilizaron las siguientes métricas:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- ROC-AUC.

Para el caso de churn, el recall es especialmente relevante porque permite evaluar qué proporción de clientes que abandonan logra detectar el modelo. También se usa F1-score como métrica de selección, porque balancea precision y recall.

## 9. Resultados

Los resultados se generan automáticamente al ejecutar:

```bash
python -m src.train
python -m src.evaluate
```

Las métricas quedan guardadas en:

- `reports/evaluation_metrics.json`
- `reports/evaluation_report.json`

## 10. Modelo seleccionado

El modelo final se selecciona según F1-score sobre el conjunto de prueba. El artefacto serializado se guarda en:

```text
models/churn_model.joblib
```

Este archivo contiene tanto el preprocesamiento como el modelo, por lo que puede cargarse para inferencia sin repetir manualmente las transformaciones.

## 11. Reproducibilidad y trazabilidad

El proyecto incorpora:

- Estructura modular de carpetas.
- Scripts reutilizables en `src/`.
- Archivo de entorno `environment.yml`.
- Archivo `requirements.txt`.
- Registro opcional de experimentos con MLflow.
- Pipeline documentado en `dvc.yaml`.
- Pruebas mínimas con pytest.

## 12. Limitaciones

La principal limitación es que el dataset es sintético, por lo que los resultados no representan necesariamente el comportamiento real de una empresa. Además, en esta primera etapa no se aborda todavía despliegue como API ni monitoreo operativo del modelo.

## 13. Conclusión

La primera etapa permite obtener un modelo de clasificación binaria entrenado, evaluado y serializado para predecir churn. La solución no queda limitada a un notebook, sino que se organiza como un proyecto reproducible y trazable, alineado con prácticas iniciales de MLOps.

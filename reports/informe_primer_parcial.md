# Informe técnico - Primer parcial

# Proyecto MLOps local para predicción de churn

## 1. Introducción

El presente informe documenta la primera etapa del proyecto de Machine Learning aplicado a la predicción de abandono de clientes, también conocido como *customer churn*. El caso de uso corresponde a AndesLink Servicios Digitales S.A., una empresa de suscripción mensual planteada para el desarrollo del proyecto, cuyo objetivo es anticipar qué clientes presentan mayor probabilidad de cancelar el servicio.

Esta entrega corresponde al primer parcial y se concentra en las etapas iniciales del flujo MLOps: comprensión del problema de negocio, análisis exploratorio de datos, preparación del dataset, entrenamiento de modelos supervisados, evaluación de resultados, selección del modelo final, serialización del artefacto y documentación del proceso.

El objetivo de esta etapa no es solamente obtener un modelo predictivo, sino también organizar el trabajo como un proyecto reproducible y trazable. Por ese motivo, la solución no queda limitada a un notebook, sino que se estructura en carpetas, módulos reutilizables, archivos de configuración, pruebas básicas, reportes y documentación.

---

## 2. Contexto de negocio

AndesLink Servicios Digitales S.A. comercializa planes de suscripción mensual para consumidores finales. En este tipo de negocio, la continuidad de los clientes es un aspecto central, ya que los ingresos dependen de pagos recurrentes a lo largo del tiempo.

Cuando un cliente cancela el servicio, la empresa no solo pierde ingresos mensuales, sino que también debe realizar nuevos esfuerzos comerciales para adquirir o recuperar usuarios. Esto puede implicar mayores costos de marketing, promociones, descuentos o campañas específicas de retención.

Desde el punto de vista del negocio, contar con una herramienta que permita anticipar el abandono puede mejorar la toma de decisiones. Si se detectan clientes con alta probabilidad de churn, la empresa podría priorizar acciones como contactos preventivos, beneficios comerciales, revisión de reclamos, mejoras en la atención o campañas segmentadas.

Por lo tanto, el problema a resolver consiste en transformar datos disponibles sobre los clientes en información útil para estimar el riesgo de abandono y apoyar decisiones comerciales de retención.

---

## 3. Objetivo analítico

El objetivo analítico del proyecto es construir un modelo supervisado de clasificación binaria capaz de predecir si un cliente abandonará o no el servicio.

La variable objetivo es:

```text
churn
```

Donde:

```text
0 = el cliente permanece activo
1 = el cliente abandona el servicio
```

A partir de variables relacionadas con antigüedad, facturación, uso mensual, productos contratados, historial de pagos, soporte, tipo de contrato y características comerciales, el modelo busca estimar la probabilidad de abandono de cada cliente.

Desde el punto de vista técnico, esta primera etapa busca obtener un modelo entrenado, evaluado y serializado, que pueda ser cargado posteriormente para realizar inferencias sin necesidad de reentrenar todo el flujo.

---

## 4. Dataset utilizado

Para el desarrollo del modelo se utilizó el archivo:

```text
data/raw/churn_sintetico.csv
```

El dataset fue provisto como base de trabajo para el caso AndesLink. Contiene 5000 registros y 16 columnas. Cada fila representa un cliente y cada columna describe una característica asociada a su relación con el servicio.

Las variables disponibles permiten analizar distintos aspectos del comportamiento del cliente, como antigüedad, facturación, uso mensual, cantidad de productos contratados, historial de pagos, contactos con soporte, tipo de contrato, método de pago, región y condición promocional.

Las variables principales son:

| Variable               | Descripción                                          |
| ---------------------- | ---------------------------------------------------- |
| `customer_age`         | Edad del cliente                                     |
| `tenure_months`        | Antigüedad del cliente en meses                      |
| `monthly_charge`       | Cargo mensual del servicio                           |
| `total_charges`        | Importe acumulado pagado por el cliente              |
| `avg_monthly_usage_gb` | Uso mensual promedio del servicio                    |
| `num_products`         | Cantidad de productos contratados                    |
| `has_streaming`        | Indica si el cliente posee servicio de streaming     |
| `has_security_pack`    | Indica si el cliente posee paquete de seguridad      |
| `support_tickets`      | Cantidad de reclamos o contactos con soporte         |
| `late_payments`        | Cantidad de pagos atrasados                          |
| `contract_type`        | Tipo de contrato                                     |
| `payment_method`       | Método de pago                                       |
| `internet_service`     | Tipo de servicio de internet                         |
| `region`               | Región del cliente                                   |
| `is_promo`             | Indica si el cliente posee una condición promocional |
| `churn`                | Variable objetivo                                    |

La estructura del dataset resulta adecuada para un problema de clasificación binaria, ya que combina variables numéricas, categóricas y comerciales vinculadas con el abandono de clientes.

---

## 5. Análisis exploratorio de datos

El análisis exploratorio se desarrolló en el notebook:

```text
notebooks/01_eda_churn.ipynb
```

El propósito del análisis exploratorio fue comprender la estructura general de los datos, revisar la calidad del dataset y observar posibles relaciones entre las variables disponibles y la variable objetivo.

Durante esta etapa se analizaron los siguientes aspectos:

* dimensiones del dataset;
* tipos de datos de cada columna;
* existencia de valores nulos;
* distribución de la variable objetivo;
* distribución de variables numéricas;
* frecuencia de variables categóricas;
* relación entre churn y variables comerciales;
* relación entre churn y variables de comportamiento;
* correlaciones entre variables numéricas.

El dataset no presenta valores faltantes en esta primera revisión. De todos modos, el pipeline de modelado incorpora estrategias de imputación para prevenir errores ante futuros datos de entrada que pudieran contener valores ausentes.

La variable objetivo presenta dos clases: clientes que permanecen y clientes que abandonan. La clase mayoritaria corresponde a clientes que no abandonan, aunque existe una cantidad suficiente de casos positivos de churn para entrenar modelos supervisados de clasificación binaria.

Entre las variables relevantes para el análisis se encuentran:

* `tenure_months`, ya que la antigüedad puede estar relacionada con el nivel de fidelización del cliente;
* `monthly_charge`, porque cargos mensuales más altos pueden influir en la decisión de cancelar;
* `total_charges`, porque resume parte del historial económico del cliente;
* `support_tickets`, ya que una mayor cantidad de reclamos puede reflejar problemas de satisfacción;
* `late_payments`, porque los pagos atrasados pueden indicar riesgo comercial;
* `contract_type`, porque el tipo de contrato puede facilitar o dificultar la cancelación;
* `payment_method`, dado que distintos medios de pago pueden asociarse a distintos comportamientos de permanencia;
* `is_promo`, porque las promociones pueden influir en la continuidad del cliente.

El análisis exploratorio permitió confirmar que el dataset cuenta con variables pertinentes para construir un modelo inicial de predicción de churn.

---

## 6. Preparación de datos

La preparación de datos se implementó mediante un `Pipeline` de scikit-learn. Esta decisión permite integrar en un mismo flujo las transformaciones de preprocesamiento y el modelo final.

Usar un pipeline es importante porque evita aplicar transformaciones de manera manual o separada entre entrenamiento e inferencia. Si el preprocesamiento quedara fuera del modelo serializado, podría ocurrir que los datos nuevos fueran transformados de forma distinta a los datos utilizados durante el entrenamiento.

Las variables fueron separadas en dos grupos principales: numéricas y categóricas.

### 6.1 Variables numéricas

Para las variables numéricas se aplicaron dos transformaciones:

1. imputación con la mediana;
2. escalado con `StandardScaler`.

La imputación con mediana permite cubrir posibles valores faltantes de manera robusta. El escalado con `StandardScaler` transforma las variables para que tengan una escala comparable, lo cual resulta especialmente útil para modelos como la regresión logística.

### 6.2 Variables categóricas

Para las variables categóricas se aplicaron dos transformaciones:

1. imputación con la categoría más frecuente;
2. codificación mediante `OneHotEncoder`.

La codificación One-Hot permite convertir variables categóricas en variables numéricas que puedan ser interpretadas por los algoritmos de Machine Learning. Además, se configuró el encoder para ignorar categorías desconocidas, evitando errores si en el futuro aparecen valores no vistos durante el entrenamiento.

---

## 7. Separación entre entrenamiento y prueba

El dataset fue dividido en conjuntos de entrenamiento y prueba. Se utilizó el 80% de los datos para entrenamiento y el 20% restante para prueba.

Además, la separación se realizó de forma estratificada según la variable `churn`. Esto permite conservar una proporción similar de clientes que abandonan y no abandonan tanto en el conjunto de entrenamiento como en el conjunto de prueba.

Esta separación es necesaria para evaluar el desempeño del modelo sobre datos que no fueron utilizados durante el entrenamiento. De esta forma, las métricas obtenidas representan una estimación más realista de la capacidad de generalización del modelo.

---

## 8. Modelos entrenados

Se entrenaron y compararon tres modelos supervisados de clasificación binaria:

1. **Logistic Regression**
2. **Random Forest Classifier**
3. **Gradient Boosting Classifier**

La regresión logística se utilizó como modelo base. Es un algoritmo simple, interpretable y útil para establecer una primera referencia de desempeño.

Random Forest se incorporó como modelo basado en árboles de decisión. Este tipo de modelo permite capturar relaciones no lineales entre variables y suele funcionar bien en datasets tabulares.

Gradient Boosting también se incluyó como alternativa no lineal. Este algoritmo entrena modelos de manera secuencial, intentando corregir errores de modelos anteriores, por lo que puede alcanzar buen rendimiento en problemas de clasificación.

Comparar distintos modelos permite tomar una decisión basada en evidencia y no únicamente en intuición. En este caso, la selección final se realizó a partir de las métricas obtenidas sobre el conjunto de prueba.

---

## 9. Métricas de evaluación

Para evaluar los modelos se utilizaron las siguientes métricas:

| Métrica   | Interpretación                                                          |
| --------- | ----------------------------------------------------------------------- |
| Accuracy  | Proporción total de predicciones correctas                              |
| Precision | Proporción de clientes predichos como churn que efectivamente abandonan |
| Recall    | Proporción de clientes que abandonan y fueron correctamente detectados  |
| F1-score  | Promedio armónico entre precision y recall                              |
| ROC-AUC   | Capacidad general del modelo para separar ambas clases                  |

En un problema de churn, la métrica accuracy puede ser insuficiente si existe diferencia entre la cantidad de clientes que abandonan y los que permanecen. Un modelo podría obtener una accuracy aceptable prediciendo mayormente la clase más frecuente, pero aun así fallar en detectar clientes con riesgo real de abandono.

Por ese motivo, se analizaron también precision, recall y F1-score.

El recall es relevante porque indica cuántos clientes que efectivamente abandonan fueron detectados por el modelo. Desde el punto de vista del negocio, no identificar a un cliente en riesgo puede significar perder una oportunidad de retención.

La precision también es importante porque permite estimar qué tan confiables son las predicciones positivas. Una baja precision implicaría destinar acciones comerciales a muchos clientes que probablemente no iban a abandonar.

El F1-score se utilizó como métrica principal de selección porque resume el equilibrio entre precision y recall. Esta métrica resulta adecuada para una primera versión del modelo, donde interesa balancear la detección de clientes en riesgo con la calidad de las predicciones positivas.

---

## 10. Resultados obtenidos

Luego del entrenamiento y evaluación, los resultados comparativos fueron los siguientes:

| Modelo              | Accuracy | Precision | Recall | F1-score | ROC-AUC |
| ------------------- | -------: | --------: | -----: | -------: | ------: |
| Logistic Regression |    0.723 |     0.621 |  0.476 |    0.539 |   0.758 |
| Random Forest       |    0.719 |     0.618 |  0.456 |    0.525 |   0.737 |
| Gradient Boosting   |    0.717 |     0.608 |  0.474 |    0.532 |   0.749 |

Los tres modelos presentan resultados relativamente cercanos. Sin embargo, la regresión logística obtuvo el mejor F1-score y también el mejor ROC-AUC entre las alternativas evaluadas.

Esto indica que, para esta primera etapa, un modelo lineal logra un desempeño competitivo frente a modelos más complejos. Esta situación puede ocurrir cuando las relaciones principales entre las variables y la variable objetivo pueden ser capturadas adecuadamente por un modelo más simple, o cuando los modelos más complejos no aportan una mejora significativa con la configuración inicial utilizada.

También se observa que el recall se mantiene en valores moderados. Esto significa que el modelo logra detectar una parte de los clientes que abandonan, pero todavía deja fuera algunos casos positivos. En una etapa posterior, podría evaluarse un ajuste del umbral de clasificación si el objetivo del negocio fuera priorizar la detección de clientes en riesgo por encima de la precisión.

---

## 11. Modelo seleccionado

El modelo seleccionado fue:

```text
Logistic Regression
```

La selección se realizó tomando como criterio principal el F1-score sobre el conjunto de prueba. Además, este modelo presentó el mejor ROC-AUC entre las alternativas comparadas.

El modelo final fue serializado en el archivo:

```text
models/churn_model.joblib
```

Este artefacto contiene el pipeline completo, incluyendo:

* imputación de variables numéricas;
* escalado de variables numéricas;
* imputación de variables categóricas;
* codificación One-Hot;
* modelo de clasificación final.

Guardar el pipeline completo permite realizar inferencias futuras aplicando las mismas transformaciones utilizadas durante el entrenamiento. Esto reduce el riesgo de inconsistencias entre el entrenamiento y el uso posterior del modelo.

---

## 12. Organización del proyecto

El proyecto se organizó con la siguiente estructura:

```text
andeslink-churn-mlops/
├─ data/
│  └─ raw/
│     └─ churn_sintetico.csv
├─ notebooks/
│  └─ 01_eda_churn.ipynb
├─ src/
│  ├─ config.py
│  ├─ data.py
│  ├─ features.py
│  ├─ train.py
│  ├─ evaluate.py
│  ├─ predict.py
│  └─ utils.py
├─ models/
│  └─ churn_model.joblib
├─ reports/
│  ├─ evaluation_metrics.json
│  ├─ evaluation_report.json
│  ├─ informe_primer_parcial.md
│  └─ figures/
├─ tests/
│  ├─ test_data.py
│  └─ test_model.py
├─ docs/
│  └─ arquitectura.md
├─ environment.yml
├─ requirements.txt
├─ dvc.yaml
├─ README.md
├─ .gitignore
└─ pyproject.toml
```

Esta estructura permite separar responsabilidades:

* `data/`: almacena los datos utilizados por el proyecto;
* `notebooks/`: contiene el análisis exploratorio inicial;
* `src/`: concentra la lógica reutilizable de carga, preparación, entrenamiento, evaluación y predicción;
* `models/`: guarda el modelo entrenado y serializado;
* `reports/`: contiene métricas, reportes y documentación de resultados;
* `tests/`: incluye pruebas básicas del proyecto;
* `docs/`: documenta aspectos de arquitectura;
* `README.md`: explica cómo instalar, ejecutar y validar el proyecto.

Esta organización facilita la lectura del proyecto y permite que el flujo pueda ser ejecutado nuevamente sin depender únicamente de celdas manuales de un notebook.

---

## 13. Reproducibilidad y trazabilidad

Uno de los objetivos principales de la entrega es que el entrenamiento pueda reproducirse siguiendo instrucciones claras. Por eso, además del notebook exploratorio, se implementaron scripts reutilizables dentro de la carpeta `src/`.

Los comandos principales de ejecución son:

```bash
python -m src.train
python -m src.evaluate
python -m pytest
```

En Windows, si se utiliza un entorno virtual local sin activar scripts de PowerShell, también puede ejecutarse con:

```powershell
.\.venv\Scripts\python.exe -m src.train
.\.venv\Scripts\python.exe -m src.evaluate
.\.venv\Scripts\python.exe -m pytest
```

El proyecto incluye los siguientes archivos de sopLearning para predecir churn de clientes en AndesLink Servicios Digitales S.A.

El trabajo incluyó la comprensión del problema de negocio, el análisis exploratorio del dataset, la preparación de datos, el entrenamiento de tres modelos supervisados, la evaluación mediante métricas de clasificación, la selección del modelo final y la serialización del pipeline completo.

El modelo seleccionado fue una regresión logística, ya que obtuvo el mejor F1-score y el mejor ROC-AUC entre las alternativas evaluadas. Si bien los resultados son mejorables, el modelo constituye una base funcional y reproducible para continuar con las siguientes etapas del proyecto.

La solución fue organizada como un proyecto modular, con código reutilizable, pruebas básicas, archivos de entorno, documentación e informe técnico. De esta manera, la entrega no queda limitada a un notebook, sino que se aproxima a una práctica inicial de MLOps local.
orte:

* `environment.yml`, para crear un entorno reproducible con conda;
* `requirements.txt`, como alternativa de instalación con pip;
* `dvc.yaml`, para documentar etapas reproducibles del pipeline;
* `README.md`, con instrucciones de instalación y ejecución;
* pruebas mínimas con `pytest`;
* modelo serializado en formato `.joblib`.

El proyecto también deja preparada una estructura compatible con prácticas iniciales de MLOps, separando entrenamiento, evaluación, predicción, documentación y validación.

---

## 14. Pruebas realizadas

Se incluyeron pruebas básicas con `pytest` para validar componentes mínimos del proyecto.

Las pruebas verifican, entre otros puntos:

* que el dataset pueda cargarse correctamente;
* que la variable objetivo exista;
* que el modelo serializado esté disponible;
* que el modelo pueda generar una predicción básica.

La ejecución de pruebas finalizó correctamente con el siguiente resultado:

```text
4 passed
```

Si bien estas pruebas son simples, permiten comprobar que los componentes principales del proyecto se encuentran disponibles y que el flujo básico funciona. En etapas posteriores podrían agregarse pruebas más completas sobre validación de datos, consistencia de esquemas y comportamiento de un servicio de inferencia.

---

## 15. Inferencia inicial

Además del entrenamiento y evaluación, se incluyó un módulo de predicción en:

```text
src/predict.py
```

Este módulo permite cargar el modelo serializado y generar una predicción a partir de nuevos datos de entrada. Aunque en esta primera entrega todavía no se desarrolla una API, esta separación facilita una futura integración del modelo en un servicio de inferencia.

La existencia de este módulo permite verificar que el modelo no depende del notebook ni de un reentrenamiento para ser utilizado. Esto es importante porque el objetivo de esta etapa es obtener un artefacto listo para ser reutilizado en fases posteriores del proyecto.

---

## 16. Limitaciones

El modelo fue entrenado con una primera configuración base de algoritmos. No se realizó una búsqueda exhaustiva de hiperparámetros ni una optimización avanzada del umbral de clasificación.

Otra limitación es que todavía no se cuenta con datos temporales para evaluar cambios en el comportamiento de los clientes, drift de datos o degradación del modelo a lo largo del tiempo. Estos aspectos corresponden a etapas posteriores del proyecto.

También debe considerarse que, aunque la regresión logística obtuvo el mejor resultado en esta comparación inicial, el recall todavía podría mejorarse. En un escenario operativo, sería recomendable discutir con el área de negocio cuál es el costo relativo de un falso negativo frente a un falso positivo.

---

## 17. Conclusión

En esta primera etapa se desarrolló una solución inicial de Machine 
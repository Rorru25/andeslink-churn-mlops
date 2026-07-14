# Informe de monitoreo final - AndesLink Churn

Este informe resume las verificaciones realizadas sobre el despliegue final del proyecto AndesLink Churn.

El objetivo de esta etapa fue agregar una capa de monitoreo sobre la API de predicción, revisar métricas técnicas del servicio y generar un primer análisis de datos/modelo con Evidently.

Las evidencias utilizadas se guardaron en:
reports/evidencias_final/

## Evidencias generadas

Para comprobar el funcionamiento del sistema se guardaron las siguientes capturas:

| Evidencia | Archivo | Qué muestra |
|---|---|---|
| Tests finales | `tests.png` | Pruebas automáticas ejecutadas correctamente |
| Docker Compose | `docker.png` | Servicios principales levantados |
| Predicción en Swagger | `swagger.png` | Endpoint `/predict` funcionando |
| Prometheus conectado | `prometheus.png` | Prometheus leyendo la API |
| Métricas Prometheus | `metrica1.png` | Métricas propias de la API disponibles |
| Métricas Prometheus | `metrica2.png` | Métricas propias de la API disponibles |
| Dashboard Grafana | `grafana.png` | Visualización del monitoreo operativo |
| Reporte Evidently | `evidently.png` | Reporte de calidad/drift generado |

Estas capturas no reemplazan los tests, pero sirven como evidencia visual de que el sistema fue ejecutado y revisado localmente.

## Monitoreo técnico del servicio

La API expone métricas en el endpoint:

```text
/metrics
```

Prometheus consulta ese endpoint y Grafana permite visualizar los datos recolectados.

Las métricas principales revisadas fueron:

- disponibilidad de la API;
- estado de carga del modelo;
- cantidad de requests;
- latencia;
- cantidad de predicciones;
- errores de inferencia;
- distribución de predicciones por clase y nivel de riesgo.

En Prometheus se verificó la consulta:

```promql
up{job="andeslink-api"}
```

El valor esperado es `1`, lo que indica que Prometheus puede comunicarse correctamente con la API.

También se revisaron métricas propias como:

```promql
andeslink_model_loaded
andeslink_api_requests_total
andeslink_predictions_total
andeslink_prediction_errors_total
```

## Interpretación del estado técnico

A partir de las evidencias, el sistema quedó funcionando en un entorno local con los siguientes servicios:

- API FastAPI;
- interfaz Streamlit;
- Prometheus;
- Grafana.

La API respondió correctamente al endpoint `/health` y al endpoint `/predict`.

El dashboard de Grafana permitió revisar el estado general del servicio. En esta etapa, el volumen de requests es bajo porque el proyecto no tiene tráfico real. Por ese motivo, las métricas no muestran todavía un comportamiento productivo, sino una prueba controlada del flujo de monitoreo.

Esto es esperable para el alcance del trabajo, ya que el objetivo era dejar funcionando la observabilidad básica y no simular una operación real de alto volumen.

## Monitoreo de datos y modelo

Además del monitoreo técnico, se generó un reporte con Evidently para comparar datos de referencia contra una ventana actual.

El script utilizado fue:
monitoring/evidently/generate_drift_report.py

El reporte generado quedó guardado en:

reports/monitoring/evidently_drift_report.html

El reporte permite revisar:

- calidad de los datos;
- diferencias entre datos de referencia y datos actuales;
- posibles cambios en distribuciones;
- señales iniciales de data drift.

Como el proyecto no cuenta con usuarios reales generando predicciones de manera continua, el script usa el log de inferencias cuando hay suficientes registros. Si no los hay, genera una ventana actual simulada para poder demostrar el flujo de monitoreo.

Esta decisión no representa un monitoreo productivo real, pero sí permite mostrar cómo se podría controlar la estabilidad de los datos en una implementación posterior.

## Logs de inferencia

Cada predicción realizada por la API genera un registro en:

logs/predictions_log.csv

Este archivo contiene:

- fecha y hora de la predicción;
- nombre y versión del modelo;
- clase predicha;
- probabilidad de churn;
- nivel de riesgo;
- variables de entrada.

El log no se versiona en Git porque se genera durante la ejecución. De todas formas, es importante porque permite construir una ventana de datos actuales para análisis posteriores.

En una versión más avanzada, este log debería guardarse en una base de datos o sistema de almacenamiento más adecuado.

## Posibles acciones correctivas

El monitoreo no sirve solamente para mirar gráficos, sino para decidir qué hacer si aparece un problema.

Algunas acciones correctivas posibles serían:

| Señal observada | Posible interpretación | Acción correctiva |
|---|---|---|
| La API no responde | El servicio está caído o no inició bien | Revisar logs del contenedor y estado del healthcheck |
| Aumentan los errores 4xx | Se están enviando datos inválidos | Revisar validaciones, documentación del payload o interfaz de carga |
| Aumentan los errores 5xx | Error interno de la API o del modelo | Revisar logs, carga del modelo y compatibilidad de datos |
| Sube mucho la latencia | El servicio tarda demasiado en responder | Revisar recursos, tamaño del modelo o cantidad de requests |
| Aparecen muchas predicciones de alto riesgo | Cambio en el perfil de clientes consultados | Analizar datos de entrada y comportamiento comercial |
| Evidently detecta drift | Los datos actuales se alejan del histórico | Revisar variables afectadas y evaluar reentrenamiento |
| Baja la calidad de los datos | Faltantes, valores raros o categorías inesperadas | Corregir validaciones y revisar origen de datos |

##  Limitaciones del monitoreo actual

El monitoreo implementado funciona de manera local y tiene algunas limitaciones:

- no hay tráfico real continuo;
- no hay alertas automáticas configuradas;
- las métricas no se conservan en un almacenamiento persistente;
- las inferencias se guardan en CSV y no en una base de datos;
- el reporte de Evidently puede usar una ventana simulada si no hay suficientes registros reales;
- no hay reentrenamiento automático del modelo.

Estas limitaciones son razonables para el alcance académico del proyecto, pero deberían resolverse si el sistema se llevara a producción.

## Conclusión

El proyecto quedó con una primera capa de monitoreo técnico y de datos.

Prometheus permite recolectar métricas de la API, Grafana permite visualizarlas y Evidently permite revisar cambios entre datos de referencia y datos actuales.

La parte más importante de esta etapa fue pasar de tener solamente una API que predice a tener un servicio que también se puede observar. Esto permite detectar errores, revisar el estado del modelo y empezar a pensar acciones correctivas ante cambios en el comportamiento de los datos o del servicio.
# 🌍 Análisis con Streaming de datos y Machine Learning

Este proyecto, tiene como objetivo procesar y analizar datos de felicidad mundial de **2015 a 2019**. Utiliza técnicas de **ETL (Extracción, Transformación y Carga)**, *machine learning* para predecir puntajes de felicidad, y un flujo de datos en tiempo real con **Apache Kafka**, todo implementado mediante **Docker**.

---

## 📌 Descripción General

El propósito del proyecto es doble:

- Comprender los factores que influyen en la felicidad global, como la economía, el apoyo social, la salud, la libertad, la percepción de corrupción y la generosidad.
- Entrenar un modelo de *machine learning* para predecir puntajes de felicidad utilizando datos históricos limpios y transformados.

Se emplean herramientas modernas como **Python**, **Jupyter Notebook**, **PostgreSQL**, **Kafka** y **Scikit-learn**, integradas en un entorno **Dockerizado** para garantizar portabilidad y consistencia.

---

## ⚙️ Requisitos

- Python 
- Jupyter Notebook
- PostgreSQL
- Apache Kafka
- Docker y Docker Compose
- Dependencias listadas en `requirements.txt`:
  - `pandas`, `scikit-learn`, `xgboost`, `kafka-python`, `SQLAlchemy`, entre otras.

---

## 🚀 Instalación y Configuración

```bash
# 1. Clonar el repositorio
git clone https://github.com/Juanjoslo2/workshop-3.git
cd workshop-3

# 2. Crear y activar un entorno virtual
python -m venv venv
# En Linux/Mac
source venv/bin/activate
# En Windows
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### 📁 Configurar variables de entorno

Crear un archivo `.env` dentro de `env/` con las credenciales de PostgreSQL:

```env
PG_USER=tu_usuario
PG_PASSWORD=tu_contraseña
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=nombre_base_datos
```

### 🐳 Levantar servicios con Docker

```bash
docker-compose up -d
```

---

## 🗂️ Estructura del Proyecto

```plaintext
├── .gitignore
├── docker-compose.yml
├── README.md
├── requirements.txt
├── data/
│   ├── model/
│   │   └── best_model_xgboost_pipeline.pkl
│   ├── raw/
│   │   ├── 2015.csv
│   │   ├── 2016.csv
│   │   ├── 2017.csv
│   │   ├── 2018.csv
│   │   └── 2019.csv
│   └── transform_data/
│       └── transform_happiness_score.csv
├── database/
│   └── db.py
├── env/
│   └── .env
├── notebooks/
│   ├── 01_ETL.ipynb
│   └── 02_Model_training.ipynb
├── streaming/
│   ├── producer.py
│   └── consumer.py
└──
```

---

## 🧾 Descripción de Archivos

- `data/raw/`: Archivos CSV originales con datos de felicidad (2015-2019).
- `data/transform_data/transform_happiness_score.csv`: Datos consolidados y transformados.
- `data/model/best_model_xgboost_pipeline.pkl`: Modelo XGBoost entrenado y almacenado.
- `notebooks/01_ETL.ipynb`: Limpieza y transformación de datos.
- `notebooks/02_Model_training.ipynb`: Entrenamiento y evaluación de modelos.
- `database/db.py`: Operaciones de base de datos con PostgreSQL.
- `streaming/producer.py` / `consumer.py`: Scripts para transmisión de datos con Kafka.
- `docker-compose.yml`: Configuración de Kafka y Zookeeper.

---

## 🛠️ Uso del Proyecto

### 🧪 Extracción y Transformación de Datos

- Ejecutar `notebooks/01_ETL.ipynb` para limpiar y transformar los archivos CSV en `data/raw/`.
- Se genera `transform_happiness_score.csv` en `data/transform_data/`.

### 🤖 Entrenamiento del Modelo

- Ejecutar `notebooks/02_Model_training.ipynb` para entrenar los modelos y guardar el mejor (`XGBoost`) en `data/model/`.

### 🔁 Flujo de Datos con Kafka

1. Asegurarse de que Docker esté corriendo:  
   ```bash
   docker-compose up -d
   ```

2. Crear un topic en Kafka (ej. `docker exec -it kafka_service kafka-topics --create --topic happiness_kafka_topic --bootstrap-server localhost:9092`).

3. Ejecutar el producer:  
   ```bash
   python streaming/producer.py
   ```

4. Ejecutar el consumer:  
   ```bash
   python streaming/consumer.py
   ```

---

## 📊 Detalles Técnicos

### 🧾 Datos Originales

| Año   | Columnas | Observaciones clave |
|-------|----------|---------------------|
| **2015** | 12 columnas | Incluye `Region` y métricas detalladas como `Economy`, `Family`, `Trust`, etc. |
| **2016** | 13 columnas | Similar a 2015 pero con intervalos de confianza adicionales (`Lower/Upper Confidence Interval`). |
| **2017** | 12 columnas | Columnas con nombres diferentes (`Happiness.Score`, `Economy..GDP.per.Capita.`). No tiene `Region`. |
| **2018** | 9 columnas  | Estructura más simplificada. Cambian nombres de columnas. Incluye un valor nulo en `Perceptions of corruption`. |
| **2019** | 9 columnas  | Igual estructura a 2018 pero sin valores nulos. No contiene `Region`. |

### 📄 Detalle por archivo

#### **2015.csv**
- **Número de columnas**: 12  
- **Columnas**:
  - `Country` (object)
  - `Region` (object)
  - `Happiness Rank` (int64)
  - `Happiness Score` (float64)
  - `Standard Error` (float64)
  - `Economy (GDP per Capita)` (float64)
  - `Family` (float64)
  - `Health (Life Expectancy)` (float64)
  - `Freedom` (float64)
  - `Trust (Government Corruption)` (float64)
  - `Generosity` (float64)
  - `Dystopia Residual` (float64)

#### **2016.csv**
- **Número de columnas**: 13  
- **Columnas**:
  - Igual que 2015 +  
  - `Lower Confidence Interval` (float64)  
  - `Upper Confidence Interval` (float64)

#### **2017.csv**
- **Número de columnas**: 12  
- **Columnas**:
  - `Country` (object)
  - `Happiness.Rank` (int64)
  - `Happiness.Score` (float64)
  - `Whisker.high` (float64)
  - `Whisker.low` (float64)
  - `Economy..GDP.per.Capita.` (float64)
  - `Family` (float64)
  - `Health..Life.Expectancy.` (float64)
  - `Freedom` (float64)
  - `Generosity` (float64)
  - `Trust..Government.Corruption.` (float64)
  - `Dystopia.Residual` (float64)

#### **2018.csv**
- **Número de columnas**: 9  
- **Columnas**:
  - `Overall rank` (int64)
  - `Country or region` (object)
  - `Score` (float64)
  - `GDP per capita` (float64)
  - `Social support` (float64)
  - `Healthy life expectancy` (float64)
  - `Freedom to make life choices` (float64)
  - `Generosity` (float64)
  - `Perceptions of corruption` (float64) → contiene un valor nulo

#### **2019.csv**
- **Número de columnas**: 9  
- **Columnas**:
  - Igual que 2018, pero sin valores nulos

### 🧹 Preprocesamiento

- Eliminación de columnas irrelevantes (`Happiness Rank`, `Dystopia Residual`).
- Renombramiento para uniformidad (ej. `GDP per capita` → `economy`).
- Imputación de valores nulos con la mediana.
- Asignación de regiones faltantes desde años anteriores.

> Resultado: `transform_happiness_score.csv`

---

## 📈 Entrenamiento y Evaluación

### Modelos utilizados:

- `LinearRegression`
- `DecisionTreeRegressor`
- `RandomForestRegressor`
- `GradientBoostingRegressor`
- `XGBoost`

### Métricas:

- `R²`, `MAE`, `MSE`, `RMSE`, `Explained Variance`

**Mejor modelo:**  
✅ **XGBoost** — R² = **0.83**, MAE = **0.35**, RMSE = **0.45**

---

## 📡 Integración con Kafka

- **Producer**: Envía filas de `transform_happiness_score.csv` al topic `happiness-transformed`.
- **Consumer**: Procesa mensajes, predice con XGBoost y guarda resultados en PostgreSQL.

---

## 🗃️ Base de Datos

Tabla: `predicted_happiness`

| Columna                   | Tipo de Dato           |
|--------------------------|------------------------|
| id                       | INTEGER PRIMARY KEY AUTOINCREMENT |
| region                   | TEXT                   |
| happiness_score          | FLOAT                  |
| economy                  | FLOAT                  |
| family                   | FLOAT                  |
| health                   | FLOAT                  |
| freedom                  | FLOAT                  |
| government_corruption    | FLOAT                  |
| generosity               | FLOAT                  |
| year                     | INTEGER                |
| predicted_happiness_score | FLOAT                 |

---


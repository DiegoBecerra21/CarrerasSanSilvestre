# San Silvestre Coruña: Historical Data Pipeline

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Scrapy](https://img.shields.io/badge/Framework-Scrapy-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Viz-Matplotlib-11557c?style=flat&logo=matplotlib&logoColor=white)
![Seaborn](https://img.shields.io/badge/Viz-Seaborn-4c72b0?style=flat&logo=seaborn&logoColor=white)

Proyecto de IA & Big Data diseñado para extraer, limpiar y analizar el histórico de resultados de la carrera San Silvestre de A Coruña (2010-2025).

## Descripción del Proyecto
Este repositorio abarca las primeras fases del ciclo de vida del dato (ETL):

| Fase | Tecnología | Descripción |
| :--- | :--- | :--- |
| **1. Ingesta (Scraping)** | `Scrapy` | Extracción robusta de datos web, manejo de paginación y limpieza inicial. |
| **2. Almacenamiento** | `SQLite` | Transformación de datos, normalización de nombres/categorías y carga en base de datos relacional. |
| **3. Análisis de Datos** | `Pandas` | Limpieza avanzada, cálculo de KPIs (ritmos, promedios) y detección de tendencias históricas. |
| **4. Visualización** | `Streamlit` | Dashboard interactivo con filtros dinámicos, gráficos comparativos y buscador de corredores. |

## Estructura del repositorio
* `scrapy_project/`: Código del spider y configuración del crawler.
* `database/`: Scripts de modelado de datos (SQLAlchemy) y pipeline de carga.
* `data/`: Directorio destino para los archivos JSON y la base de datos `.db`.
* `analysis/`: Notebooks de Jupyter para análisis exploratorio (EDA), tendencias y métricas de rendimiento.
* `dashboard/`: Código de la aplicación web interactiva (Streamlit) para visualización de datos.

---

## Guía de inicio rápido

Sigue estos pasos para reproducir el pipeline completo en tu entorno local.

### 1. Instalación de Dependencias
Asegúrate de tener Python instalado y ejecuta:
```bash
pip install -r requirements.txt
```

### 2. Ejecución del pipeline
* Inicia el spider y creará `resultados.json` (el dataset que usaremos)
    ```bash
    cd scrapy_project
    scrapy crawl carrera
    ```
* Script que lee el .json, limpia los datos y crea la base de datos
    ```bash
    cd ../database
    python pipeline.py
    ```

### 3. Ejecución de la app Streamlit
* Ejecutar el comando y usar la url proporcionada por la consola en el navegador:
* Hay una local http://localhost:8501 
* O hay tambien una Network URL: http://IP....:8501
    ```bash
    cd dashboard
    streamlit run app.py
    ```


    

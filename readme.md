# San Silvestre Coruña: Historical Data Pipeline

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Scrapy](https://img.shields.io/badge/Framework-Scrapy-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue)

Proyecto de IA & Big Data diseñado para extraer, limpiar y analizar el histórico de resultados de la carrera San Silvestre de A Coruña (2010-2025).

## Descripción del Proyecto
Este repositorio abarca las primeras fases del ciclo de vida del dato (ETL):

| Fase | Tecnología | Descripción |
| :--- | :--- | :--- |
| **1. Ingesta (Scraping)** | `Scrapy` | Extracción robusta de datos web, manejo de paginación y limpieza inicial. |
| **2. Almacenamiento** | `SQLite` | Transformación de datos, normalización de nombres/categorías y carga en base de datos relacional. |

## Estructura del repositorio
* `scrapy_project/`: Código del spider y configuración del crawler.
* `database/`: Scripts de modelado de datos (SQLAlchemy) y pipeline de carga.
* `data/`: Directorio destino para los archivos JSON y la base de datos `.db`.

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
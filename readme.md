# San Silvestre Coruña - Data Pipeline

Este repositorio contiene el pipeline de extracción (ETL) y almacenamiento de datos de la carrera San Silvestre.

## Primeras fases 
Este código cubre:
1. **Scraping**: Extracción de datos históricos (2010-2025).
2. **Database**: Limpieza y almacenamiento en SQLite.

## Cómo empezar

1. **Instalar dependencias:**
    ```bash
    pip install scrapy
    ```

2. **Ejecutar comandos:**
    ```bash
    scrapy crawl carrera
    ```
    ```bash
    cd database
    python pipeline.py
    ```
# San Silvestre Coruña - Data Pipeline

Este repositorio contiene el pipeline de extracción (ETL) y almacenamiento de datos de la carrera San Silvestre.

## Primeras fases 
Este código cubre:
1. **Scraping**: Extracción de datos históricos (2010-2025).
2. **Database**: Limpieza y almacenamiento en SQLite.

## Cómo empezar

1. **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Comandos a ejecutar:**
    ### Creación de resultados.json (el dataset que usaremos)
    ```bash
    cd scrapy_project
    scrapy crawl carrera
    ```
    ### Creación de carrera_data.db (la base de datos)
    ```bash
    cd database
    python pipeline.py
    ```
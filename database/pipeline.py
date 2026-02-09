import pandas as pd
import json
import os
from sqlalchemy import create_engine
from models import Base, ResultadoCarrera

# Esto creará un archivo llamado 'carrera_data.db'
DB_URI = 'sqlite:///carrera_data.db' 

def get_engine():
    return create_engine(DB_URI, echo=False)

def time_to_minutes(t_str):
    """Convierte '00:35:30' a minutos (float). Maneja nulos."""
    if not t_str or t_str == 'None': return None
    try:
        parts = t_str.split(':')
        if len(parts) == 3: return int(parts[0])*60 + int(parts[1]) + int(parts[2])/60
        elif len(parts) == 2: return int(parts[0]) + int(parts[1])/60
        return None
    except: return None

def run_pipeline():
    print("Iniciando carga a SQLite...")
    
    # Cargamos el .json
    json_path = '../resultados.json'
    if not os.path.exists(json_path):
        print(f"No se pudo encontrar el archivo: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    print(f"Se han leído {len(df)} registros del .json")

    # Ahora transformamos
    # Limpieza:
    df['tiempo_min'] = df['tiempo'].apply(time_to_minutes)
    df.rename(columns={'tiempo': 'tiempo_str'}, inplace=True)
    
    # Quitamos puntos y convertimos a números:
    # 'coerce' pone NaN si no es número (ej: "Desc")
    df['posicion'] = pd.to_numeric(df['posicion'].astype(str).str.replace('.', '', regex=False), errors='coerce')

    # Eliminar duplicados exactos
    df.drop_duplicates(subset=['edicion', 'nombre', 'tiempo_str'], inplace=True)

    # Por último guardamos en SQLite
    engine = get_engine()
    Base.metadata.create_all(engine) # Crea el archivo .db y la tabla si no existen

    try:
        # if_exists='replace' para volver a hacer la tabla en caso de ejecutar el comando de nuevo.
        df.to_sql('resultados', con=engine, if_exists='replace', index=False)
        print(f"Base de datos creada en: {os.path.abspath('carrera_data.db')}")
        print(f"Se han guardado {len(df)} filas.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run_pipeline()
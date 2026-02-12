import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="San Silvestre Coruña Analysis",
    layout="wide"
)

# --- 2. FUNCIONES DE CARGA Y LIMPIEZA DE DATOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "scrapy_project", "resultados.json")

@st.cache_data
def load_data():
    """Carga, limpia y enriquece los datos desde el JSON."""
    if not os.path.exists(DATA_PATH):
        st.error(f"❌ Error: No se encuentra el archivo de datos en: {DATA_PATH}")
        return pd.DataFrame()

    try:
        df = pd.read_json(DATA_PATH)
        
        # A. Convertir tiempo (HH:MM:SS) a segundos
        def time_to_seconds(t):
            try:
                h, m, s = map(int, str(t).split(':'))
                return h * 3600 + m * 60 + s
            except:
                return None
        
        df['tiempo_segundos'] = df['tiempo'].apply(time_to_seconds)
        
        # B. Limpiar distancia y convertir a float (quitar " km")
        # Aseguramos que sea string antes de reemplazar, por si acaso
        df['distancia_num'] = df['distancia'].astype(str).str.replace(' km', '').str.replace(',', '.').astype(float)
        
        # C. Calcular Ritmo (Minutos por Km)
        # Ritmo = (Tiempo en minutos) / Distancia
        df['ritmo_min_km'] = (df['tiempo_segundos'] / 60) / df['distancia_num']
        
        # Eliminar registros corruptos (sin tiempo o distancia)
        df = df.dropna(subset=['tiempo_segundos', 'distancia_num'])
        
        return df
    except Exception as e:
        st.error(f"Error procesando los datos: {e}")
        return pd.DataFrame()

def seconds_to_hms(seconds):
    """Convierte segundos a formato HH:MM:SS para mostrar en pantalla."""
    if pd.isna(seconds): return "--"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

# Cargar los datos
df = load_data()

if df.empty:
    st.stop() # Detener la app si no hay datos

# --- 3. BARRA LATERAL (NAVEGACIÓN) ---
st.sidebar.title("San Silvestre Coruña")
view_mode = st.sidebar.radio("Selecciona una vista:", ["📊 Análisis de Carrera", "🏃 Análisis de Corredor"])

st.sidebar.markdown("---")
st.sidebar.info(f"Datos cargados: {len(df)} registros históricos.")

# --- 4. FEATURE 1: ANÁLISIS DE CARRERA ---
if view_mode == "📊 Análisis de Carrera":
    st.title("Análisis Global de la Carrera")
    
    # --- FILTROS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        # Ordenamos las ediciones de más reciente a más antigua
        ediciones = sorted(df['edicion'].unique(), reverse=True)
        selected_year = st.selectbox("Selecciona Edición:", ediciones)
    
    # Filtrar datos por año primero para actualizar los otros filtros
    df_year = df[df['edicion'] == selected_year]
    
    with col2:
        generos = ["Todos"] + list(df_year['sexo'].unique())
        selected_gender = st.selectbox("Género:", generos)
    
    with col3:
        categorias = ["Todas"] + list(df_year['categoria'].unique())
        selected_category = st.selectbox("Categoría:", categorias)

    # Aplicar filtros secundarios
    df_filtered = df_year.copy()
    if selected_gender != "Todos":
        df_filtered = df_filtered[df_filtered['sexo'] == selected_gender]
    if selected_category != "Todas":
        df_filtered = df_filtered[df_filtered['categoria'] == selected_category]
        
    st.markdown("---")

    # --- KPI METRICS ---
    if not df_filtered.empty:
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("🥇 Mejor Tiempo", seconds_to_hms(df_filtered['tiempo_segundos'].min()))
        kpi2.metric("🐢 Tiempo Máximo", seconds_to_hms(df_filtered['tiempo_segundos'].max()))
        kpi3.metric("⏱️ Tiempo Medio", seconds_to_hms(df_filtered['tiempo_segundos'].mean()))
        kpi4.metric("👥 Corredores", len(df_filtered))
        
        # --- GRÁFICO DE DISTRIBUCIÓN ---
        st.subheader(f"Distribución de Tiempos - Edición {selected_year}")
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Histograma con curva de densidad
        sns.histplot(df_filtered['tiempo_segundos'] / 60, bins=40, kde=True, color="#3498db", ax=ax)
        ax.set_xlabel("Tiempo (Minutos)")
        ax.set_ylabel("Cantidad de Corredores")
        ax.set_title(f"Histograma de Tiempos ({selected_gender} - {selected_category})")
        col_grafica, col_vacia = st.columns([3, 1]) # Proporción 3 a 1 (75% vs 25%)
        with col_grafica:
            st.pyplot(fig)
        
    else:
        st.warning("No hay datos que coincidan con los filtros seleccionados.")

# --- 5. FEATURE 2: ANÁLISIS DE CORREDOR ---
elif view_mode == "🏃 Análisis de Corredor":
    st.title("Ficha Técnica del Corredor")
    
    # Buscador de corredores (ordenados alfabéticamente)
    lista_corredores = sorted(df['nombre'].unique())
    selected_runner = st.selectbox("Buscar corredor (escribe para buscar):", lista_corredores)
    
    if selected_runner:
        # Filtrar datos del corredor
        runner_data = df[df['nombre'] == selected_runner].sort_values('edicion', ascending=False)
        
        # Estadísticas personales
        best_time = runner_data['tiempo_segundos'].min()
        avg_pace = runner_data['ritmo_min_km'].mean()
        
        col1, col2 = st.columns(2)
        col1.metric("Mejor Marca Personal", seconds_to_hms(best_time))
        col2.metric("Ritmo Medio Histórico", f"{avg_pace:.2f} min/km")
        
        st.subheader("Historial de Participaciones")
        # Mostrar tabla limpia
        display_cols = ['edicion', 'tiempo', 'ritmo_min_km', 'posicion', 'categoria', 'distancia']
        st.dataframe(runner_data[display_cols].style.format({'ritmo_min_km': '{:.2f} min/km'}), use_container_width=True)
        
        # --- COMPARATIVA VISUAL ---
        st.subheader("Comparativa de Rendimiento")
        race_to_compare = st.selectbox("Selecciona una carrera para comparar:", runner_data['edicion'].unique())
        
        if race_to_compare:
            # Datos de ESA carrera (todos los corredores)
            race_data = df[df['edicion'] == race_to_compare]
            # Datos del corredor en ESA carrera
            runner_result = runner_data[runner_data['edicion'] == race_to_compare].iloc[0]
            runner_time_min = runner_result['tiempo_segundos'] / 60
            
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            
            # Histograma de fondo (todos)
            sns.histplot(race_data['tiempo_segundos'] / 60, bins=50, color="lightgray", ax=ax2, label="Resto de participantes")
            
            # Línea vertical del corredor
            ax2.axvline(runner_time_min, color="red", linestyle="--", linewidth=2, label=f"{selected_runner}")
            
            ax2.set_xlabel("Tiempo (Minutos)")
            ax2.set_title(f"Posición de {selected_runner} en {race_to_compare}")
            ax2.legend()
            
            col_grafica, col_vacia = st.columns([3, 1])
            with col_grafica:
                st.pyplot(fig2)
            
            st.caption(f"La línea roja indica tu tiempo ({runner_result['tiempo']}) comparado con el resto de los participantes.")
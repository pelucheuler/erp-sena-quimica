import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# --- 1. GENERACIÓN DE BASE DE DATOS FICTICIA ---
# (Esto simula los datos que idealmente vendrían de Neon)
@st.cache_data
def generar_datos_produccion():
    num_registros = 200
    fechas = [datetime.now() - timedelta(minutes=15 * i) for i in range(num_registros)]
    fechas.reverse() # Para tener orden cronológico

    np.random.seed(42)
    datos = {
        'Fecha_Hora': fechas,
        'Linea_Produccion': np.random.choice(['Línea A (Ensamblaje)', 'Línea B (Empaquetado)'], size=num_registros),
        'Unidades_Producidas': np.random.randint(80, 150, size=num_registros),
        'Unidades_Defectuosas': np.random.randint(0, 8, size=num_registros),
        'Tiempo_Parada_Min': np.random.choice([0, 0, 0, 0, 10, 25], size=num_registros), # Mayormente sin paradas
        'Estado_Equipo': np.random.choice(['Operativo', 'Ajuste Menor', 'Falla Mecánica'], size=num_registros, p=[0.85, 0.10, 0.05])
    }
    return pd.DataFrame(datos)

df_produccion = generar_datos_produccion()

# --- 2. DASHBOARD DE SUPERVISIÓN (STREAMLIT) ---
st.title("⚙️ Panel de Supervisión - Gestión de la Producción")
st.markdown("Monitor de indicadores en tiempo real para las líneas automatizadas.")

# Cálculo de KPIs (Indicadores Clave de Rendimiento)
total_unidades = df_produccion['Unidades_Producidas'].sum()
total_defectos = df_produccion['Unidades_Defectuosas'].sum()
tasa_calidad = 100 - ((total_defectos / total_unidades) * 100)
tiempo_perdido = df_produccion['Tiempo_Parada_Min'].sum()

# Mostrar KPIs en columnas
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Producido", f"{total_unidades:,}")
col2.metric("Defectos", f"{total_defectos:,}")
col3.metric("Tasa de Calidad", f"{tasa_calidad:.2f}%")
col4.metric("Tiempo de Parada", f"{tiempo_perdido} min")

st.divider()

# Gráficos de análisis
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Producción por Línea")
    fig_prod = px.bar(df_produccion, x='Linea_Produccion', y='Unidades_Producidas', 
                      color='Linea_Produccion', title="Volumen de Producción")
    st.plotly_chart(fig_prod, use_container_width=True)

with col_graf2:
    st.subheader("Estado Actual de Equipos")
    conteo_estados = df_produccion['Estado_Equipo'].value_counts().reset_index()
    conteo_estados.columns = ['Estado', 'Frecuencia']
    fig_estado = px.pie(conteo_estados, values='Frecuencia', names='Estado', 
                        title="Distribución de Estados de Maquinaria", hole=0.4)
    st.plotly_chart(fig_estado, use_container_width=True)

# Tabla de control para identificar novedades
st.subheader("📋 Registro de Novedades y Fallas Recientes")
# Filtramos para mostrar solo cuando hubo problemas (defectos altos o paradas)
df_alertas = df_produccion[(df_produccion['Tiempo_Parada_Min'] > 0) | (df_produccion['Unidades_Defectuosas'] >= 5)]
st.dataframe(df_alertas[['Fecha_Hora', 'Linea_Produccion', 'Estado_Equipo', 'Tiempo_Parada_Min', 'Unidades_Defectuosas']], use_container_width=True)
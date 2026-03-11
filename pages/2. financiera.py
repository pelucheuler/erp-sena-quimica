import streamlit as st
import pandas as pd
from database import get_connection

st.title("💰 Módulo Financiero y Contable")
st.image("logo.png", width=300)

conn = get_connection()

st.write("Estado de resultados en tiempo real de la Planta de Biodiesel.")

# Consultas a la base de datos
try:
    df_compras = pd.read_sql_query("SELECT SUM(cantidad * costo) as total_gastos FROM compras", conn)
    gastos_totales = df_compras['total_gastos'].iloc[0] if not pd.isna(df_compras['total_gastos'].iloc[0]) else 0
    
    # Asumimos un precio de venta estándar del Biodiesel para el simulador (ej. 15,000 COP por litro)
    PRECIO_VENTA_LITRO = 15000 
    df_prod = pd.read_sql_query("SELECT SUM(cantidad) as total_litros FROM produccion WHERE producto ILIKE '%biodiesel%'", conn)
    litros_producidos = df_prod['total_litros'].iloc[0] if not pd.isna(df_prod['total_litros'].iloc[0]) else 0
    ingresos_totales = litros_producidos * PRECIO_VENTA_LITRO
    
    utilidad_neta = ingresos_totales - gastos_totales

except Exception as e:
    gastos_totales = 0
    ingresos_totales = 0
    utilidad_neta = 0

col1, col2, col3 = st.columns(3)
col1.metric("Ingresos Proyectados (Ventas)", f"${ingresos_totales:,.0f} COP", "Por producción")
col2.metric("Costos Operativos (Compras)", f"${gastos_totales:,.0f} COP", "Materia prima y repuestos", delta_color="inverse")
col3.metric("Utilidad Bruta", f"${utilidad_neta:,.0f} COP", "Rentabilidad")

st.divider()

st.subheader("Libro Mayor: Registro de Gastos")
df_detalles_compras = pd.read_sql_query("SELECT timestamp as Fecha, producto as Concepto, (cantidad * costo) as Valor_Total_COP, proveedor as Proveedor FROM compras ORDER BY timestamp DESC", conn)
st.dataframe(df_detalles_compras, use_container_width=True)

conn.close()
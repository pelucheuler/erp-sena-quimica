import streamlit as st
import pandas as pd
from database import get_connection

st.title("🔧 Módulo de Mantenimiento")
st.image("logo.png", width=300)
conn = get_connection()

st.write("Reporte de fallas en Planta y solicitud de repuestos.")

col1, col2 = st.columns(2)
with col1:
    equipo_fallo = st.text_input("Equipo dañado (Ej. Bomba de Metanol)")
    repuesto = st.text_input("Repuesto necesario")
with col2:
    cantidad = st.number_input("Cantidad de repuestos", min_value=1, step=1)
    gravedad = st.selectbox("Nivel de Urgencia", ["Alta (Planta detenida)", "Media", "Baja"])

if st.button("Generar Orden y Pedir Repuesto"):
    c = conn.cursor()
    c.execute("INSERT INTO compras (producto, cantidad, estado) VALUES (%s, %s, 'Pendiente')", (repuesto, cantidad))
    conn.commit()
    st.success(f"¡Orden generada! Esperando a Compras/Inventario.")

st.divider()
st.subheader("Estado del Stock de Repuestos")
df_stock = pd.read_sql_query("SELECT * FROM stock WHERE tipo='Materia Prima'", conn)
st.dataframe(df_stock, use_container_width=True)

conn.close()
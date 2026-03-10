import streamlit as st
import pandas as pd
from database import get_connection

st.title("🔎 Módulo de Auditoría")
st.image("logo.png", width=300)

conn = get_connection()

st.write("Registro inalterable de todos los movimientos en el sistema ERP.")

# Botón para recargar los datos en tiempo real
if st.button("🔄 Actualizar Registros"):
    st.rerun()

st.divider()

# Cargar la tabla de auditoría ordenando por los más recientes primero
df_auditoria = pd.read_sql_query("SELECT id, accion, usuario, timestamp FROM auditoria ORDER BY timestamp DESC", conn)

if not df_auditoria.empty:
    st.dataframe(df_auditoria, use_container_width=True)
else:
    st.info("Aún no hay registros de actividad en la plataforma.")

conn.close()
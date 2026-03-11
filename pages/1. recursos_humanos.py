import streamlit as st
import pandas as pd
from database import get_connection, registrar_auditoria

st.title("👥 Módulo de Recursos Humanos")
st.image("logo.png", width=300)

usuario = st.session_state.get("usuario", "RRHH")
conn = get_connection()

st.write("Gestión de personal, turnos y novedades de nómina.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Reportar Novedad de Personal")
    trabajador = st.text_input("Nombre del Operario/Jefe de Turno")
    tipo_novedad = st.selectbox("Tipo de Novedad", ["Ausencia (Falla Personal)", "Incapacidad Médica", "Capacitación HSE", "Falta Disciplinaria"])
    observacion = st.text_area("Observaciones")
    
    if st.button("Registrar Novedad"):
        if trabajador:
            registrar_auditoria(f"RRHH reportó {tipo_novedad} para {trabajador}. Nota: {observacion}", usuario)
            st.success("Novedad registrada correctamente en el expediente.")
        else:
            st.error("Ingresa el nombre del trabajador.")

with col2:
    st.subheader("Directorio de Usuarios del ERP")
    df_usuarios = pd.read_sql_query("SELECT id, nombre, rol FROM usuarios", conn)
    st.dataframe(df_usuarios, hide_index=True)

conn.close()
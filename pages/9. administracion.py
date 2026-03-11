import streamlit as st
import pandas as pd
from database import get_connection

st.title("⚙️ Módulo de Administración")
st.image("logo.png", width=300)

usuario = st.session_state.get("usuario", "Admin")
conn = get_connection()

st.write("Panel de control general de la Planta de Biodiesel.")

tab1, tab2, tab3 = st.tabs(["Usuarios", "Inventario Global", "Todas las Operaciones"])

with tab1:
    st.subheader("Usuarios Registrados")
    df_usuarios = pd.read_sql_query("SELECT id, nombre, usuario, rol, grupo_id FROM usuarios", conn)
    st.dataframe(df_usuarios, use_container_width=True)

with tab2:
    st.subheader("Estado Global del Inventario")
    df_stock = pd.read_sql_query("SELECT * FROM stock", conn)
    st.dataframe(df_stock, use_container_width=True)

with tab3:
    st.subheader("Historial de Compras")
    df_compras = pd.read_sql_query("SELECT * FROM compras", conn)
    st.dataframe(df_compras, use_container_width=True)
    
    st.subheader("Historial de Logística")
    df_logistica = pd.read_sql_query("SELECT * FROM logistica", conn)
    st.dataframe(df_logistica, use_container_width=True)

conn.close()
import streamlit as st
import pandas as pd
from database import get_connection, registrar_auditoria

st.title("📦 Módulo de Inventario")
st.image("logo.png", width=300)
usuario = st.session_state["usuario"]
conn = get_connection()

st.subheader("Stock Actual")
df_stock = pd.read_sql_query("SELECT * FROM stock", conn)
st.dataframe(df_stock, use_container_width=True)

st.divider()
st.subheader("Solicitar Insumos a Compras")
col1, col2 = st.columns(2)
with col1:
    producto_req = st.text_input("Insumo / Materia Prima faltante")
with col2:
    cantidad_req = st.number_input("Cantidad requerida", min_value=1, step=1)

if st.button("Enviar Solicitud a Compras"):
    c = conn.cursor()
    c.execute("INSERT INTO compras (producto, cantidad, estado) VALUES (%s, %s, 'Pendiente')", (producto_req, cantidad_req))
    conn.commit()
    registrar_auditoria(f"Solicitó compra de {cantidad_req} unidades de {producto_req}", usuario)
    st.success("¡Solicitud enviada a Compras!")
    st.rerun()

conn.close()
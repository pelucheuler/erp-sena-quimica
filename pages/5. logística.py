import streamlit as st
import pandas as pd
from database import get_connection, registrar_auditoria

st.title("🚚 Módulo de Logística")
st.image("logo.png", width=300)
usuario = st.session_state.get("usuario", "Grupo 4 Logística")
conn = get_connection()

st.write("Control de despachos y recepción de mercancía para la Planta de Biodiesel.")

st.subheader("Registrar Nuevo Movimiento")
col1, col2 = st.columns(2)
with col1:
    producto_mov = st.text_input("Producto / Insumo (Ej. Sello mecánico, Metanol)")
    cantidad_mov = st.number_input("Cantidad", min_value=1, step=1)
with col2:
    destino = st.text_input("Origen/Destino (Ej. Planta Biodiesel, Bodega)")
    metodo_entrega = st.selectbox("Método de Entrega", [
        "El proveedor entrega en planta", 
        "Nosotros recogemos donde el proveedor", 
        "Movimiento interno (Bodega -> Planta)"
    ])

if st.button("Registrar Operación Logística"):
    c = conn.cursor()
    c.execute("INSERT INTO logistica (producto, cantidad, destino, estado, metodo_entrega, grupo_id) VALUES (%s, %s, %s, 'Pendiente', %s, 4)", 
              (producto_mov, cantidad_mov, destino, metodo_entrega))
    conn.commit()
    registrar_auditoria(f"Registró logística de {cantidad_mov}x {producto_mov} - {metodo_entrega}", usuario)
    st.success("Operación registrada correctamente.")
    st.rerun()

st.divider()
st.subheader("Panel de Control Logístico")
df_logistica = pd.read_sql_query("SELECT id, producto, cantidad, destino, metodo_entrega, estado FROM logistica", conn)

if not df_logistica.empty:
    st.dataframe(df_logistica, use_container_width=True)
    
    st.write("**Actualizar Estado de la Operación**")
    col3, col4 = st.columns(2)
    with col3:
        mov_id = st.selectbox("ID de la operación", df_logistica['id'])
    with col4:
        nuevo_estado = st.selectbox("Estado", ["Pendiente", "En tránsito", "Entregado", "Retrasado"])
    
    if st.button("Actualizar Estado"):
        c = conn.cursor()
        c.execute("UPDATE logistica SET estado=%s WHERE id=%s", (nuevo_estado, mov_id))
        conn.commit()
        registrar_auditoria(f"Actualizó logística ID {mov_id} a {nuevo_estado}", usuario)
        st.success("Estado actualizado con éxito.")
        st.rerun()
else:
    st.info("No hay operaciones logísticas registradas.")

conn.close()
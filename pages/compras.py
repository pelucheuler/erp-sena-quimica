import streamlit as st
import pandas as pd
from database import get_connection, registrar_auditoria

st.title("🛒 Módulo de Compras")
st.image("logo.png", width=300)
usuario = st.session_state["usuario"]
conn = get_connection()

st.subheader("Solicitudes Pendientes")
df_pendientes = pd.read_sql_query("SELECT id, producto, cantidad FROM compras WHERE estado='Pendiente'", conn)

if not df_pendientes.empty:
    st.dataframe(df_pendientes, use_container_width=True)
    
    compra_id = st.selectbox("Seleccione el ID de la solicitud", df_pendientes['id'])
    proveedor = st.text_input("Nombre del Proveedor")
    costo = st.number_input("Costo Total ($)", min_value=0.0, step=1000.0)
    
    if st.button("Ejecutar Compra"):
        c = conn.cursor()
        c.execute("UPDATE compras SET proveedor=%s, costo=%s, estado='Completado' WHERE id=%s", (proveedor, costo, compra_id))
        
        producto_comprado = df_pendientes.loc[df_pendientes['id'] == compra_id, 'producto'].values[0]
        cant_comprada = int(df_pendientes.loc[df_pendientes['id'] == compra_id, 'cantidad'].values[0])
        
        c.execute("""INSERT INTO stock (producto, cantidad, tipo) VALUES (%s, %s, 'Materia Prima') 
                     ON CONFLICT(producto) DO UPDATE SET cantidad = stock.cantidad + EXCLUDED.cantidad""", 
                  (producto_comprado, cant_comprada))
        
        conn.commit()
        registrar_auditoria(f"Compró {cant_comprada} de {producto_comprado}", usuario)
        st.success("Compra ejecutada. Material en inventario.")
        st.rerun()
else:
    st.info("No hay solicitudes.")

conn.close()
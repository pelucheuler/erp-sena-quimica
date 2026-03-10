import streamlit as st
import pandas as pd
from database import get_connection, registrar_auditoria

st.title("⚙️ Módulo de Producción")
st.image("logo.png", width=300)
usuario = st.session_state["usuario"]
conn = get_connection()

df_mp = pd.read_sql_query("SELECT producto FROM stock WHERE tipo='Materia Prima' AND cantidad > 0", conn)
lista_mp = df_mp['producto'].tolist() if not df_mp.empty else ["Sin materia prima"]

col1, col2 = st.columns(2)
with col1:
    producto_final = st.text_input("Producto Terminado a fabricar")
    cantidad_final = st.number_input("Cantidad a fabricar", min_value=1)
with col2:
    materia_prima = st.selectbox("Materia prima a consumir", lista_mp)
    cantidad_mp = st.number_input("Cantidad de Materia Prima necesaria", min_value=1)

if st.button("Iniciar Producción"):
    c = conn.cursor()
    c.execute("SELECT cantidad FROM stock WHERE producto=%s", (materia_prima,))
    stock_actual = c.fetchone()
    
    if stock_actual and stock_actual[0] >= cantidad_mp:
        c.execute("UPDATE stock SET cantidad = cantidad - %s WHERE producto=%s", (cantidad_mp, materia_prima))
        c.execute("INSERT INTO produccion (producto, cantidad, materia_prima, cant_mp, estado) VALUES (%s, %s, %s, %s, 'Completada')", 
                  (producto_final, cantidad_final, materia_prima, cantidad_mp))
        c.execute("""INSERT INTO stock (producto, cantidad, tipo) VALUES (%s, %s, 'Producto Terminado') 
                     ON CONFLICT(producto) DO UPDATE SET cantidad = stock.cantidad + EXCLUDED.cantidad""", 
                  (producto_final, cantidad_final))
        conn.commit()
        registrar_auditoria(f"Fabricó {cantidad_final} de {producto_final}", usuario)
        st.success(f"¡Éxito! {producto_final} enviado a bodega.")
    else:
        st.error("❌ ERROR: No hay suficiente materia prima.")

conn.close()
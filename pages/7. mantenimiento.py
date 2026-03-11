import streamlit as st
import pandas as pd
from database import get_connection, registrar_auditoria

st.title("🔧 Módulo de Mantenimiento")
st.image("logo.png", width=300)

usuario = st.session_state.get("usuario", "Grupo 7 Mantenimiento")
conn = get_connection()

st.write("Gestión de equipos y consumo de repuestos para la Planta de Biodiesel.")

tab1, tab2 = st.tabs(["⚙️ Consumo de Repuestos", "📋 Historial"])

with tab1:
    st.subheader("Asignar repuesto a una máquina")
    
    # Consultar qué hay en el inventario para mostrar en el menú
    df_stock = pd.read_sql_query("SELECT producto, cantidad FROM stock WHERE cantidad > 0", conn)
    
    if not df_stock.empty:
        col1, col2 = st.columns(2)
        with col1:
            maquina = st.selectbox("Máquina / Equipo (TAG)", ["PPUR-01 (Purificación)", "DEC-01 (Decantador)", "EQ-EK-003 (Destilación)", "Bomba Metanol", "Reactor Principal"])
            repuesto = st.selectbox("Repuesto a utilizar", df_stock['producto'])
        with col2:
            # Buscar cantidad disponible del repuesto seleccionado
            max_disp = df_stock.loc[df_stock['producto'] == repuesto, 'cantidad'].values[0]
            cantidad_usar = st.number_input(f"Cantidad (Disp: {max_disp})", min_value=1, max_value=int(max_disp), step=1)
            
        if st.button("Consumir Repuesto e Instalar"):
            c = conn.cursor()
            # 1. Descontar del inventario
            c.execute("UPDATE stock SET cantidad = cantidad - %s WHERE producto = %s", (cantidad_usar, repuesto))
            # 2. Registrar en auditoría
            registrar_auditoria(f"Mantenimiento instaló {cantidad_usar}x {repuesto} en el equipo {maquina}", usuario)
            conn.commit()
            st.success(f"¡Repuesto descontado del inventario e instalado en {maquina}!")
            st.rerun()
    else:
        st.warning("No hay repuestos en el inventario. Solicita a Compras que adquiera materiales.")

with tab2:
    st.subheader("Historial de Actividades")
    df_historial = pd.read_sql_query("SELECT * FROM auditoria WHERE accion LIKE 'Mantenimiento%' ORDER BY timestamp DESC", conn)
    st.dataframe(df_historial, use_container_width=True)

conn.close()
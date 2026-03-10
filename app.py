import streamlit as st
from database import init_db, validar_usuario

st.set_page_config(page_title="ERP Educativo SENA", layout="wide")

init_db()

if "usuario" not in st.session_state:
    st.title("Inicio de Sesión - ERP Educativo SENA")
    st.image("logo.png", width=300)

    usuario = st.text_input("Usuario")
    contraseña = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        datos = validar_usuario(usuario, contraseña)
        if datos:
            st.session_state["usuario"] = datos[1]
            st.session_state["rol"] = datos[4]
            st.session_state["grupo_id"] = datos[5]
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

    st.stop()

st.sidebar.title(f"Bienvenido, {st.session_state['usuario']}")

if st.sidebar.button("Cerrar sesión"):
    st.session_state.clear()
    st.rerun()

st.title("ERP Educativo SENA")
st.write("Seleccione un módulo en el menú lateral.")
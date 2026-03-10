import psycopg2
import streamlit as st

# Tu conexión directa a la nube Neon
DB_URL = "postgresql://neondb_owner:npg_bcCx0QzGXH5A@ep-shiny-hall-ad8ikgh5-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

def get_connection():
    return psycopg2.connect(DB_URL)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # Borramos la tabla de logística vieja para crearla con las nuevas columnas
    c.execute("DROP TABLE IF EXISTS logistica")

    c.execute("""CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY, nombre TEXT, usuario TEXT, contraseña TEXT, rol TEXT, grupo_id INTEGER)""")

    c.execute("""CREATE TABLE IF NOT EXISTS stock (
        producto TEXT PRIMARY KEY, cantidad INTEGER, tipo TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS compras (
        id SERIAL PRIMARY KEY, producto TEXT, cantidad INTEGER, 
        costo REAL, proveedor TEXT, estado TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

    c.execute("""CREATE TABLE IF NOT EXISTS produccion (
        id SERIAL PRIMARY KEY, producto TEXT, cantidad INTEGER, 
        materia_prima TEXT, cant_mp INTEGER, estado TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

    # Tabla logística actualizada con metodo_entrega y grupo_id
    c.execute("""CREATE TABLE IF NOT EXISTS logistica (
        id SERIAL PRIMARY KEY, producto TEXT, cantidad INTEGER, 
        destino TEXT, estado TEXT, metodo_entrega TEXT, grupo_id INTEGER, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

    c.execute("""CREATE TABLE IF NOT EXISTS auditoria (
        id SERIAL PRIMARY KEY, accion TEXT, usuario TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

    usuarios = [
        ("Grupo 1 Compras", "grupo1", "grupo1", "compras", 1),
        ("Grupo 2 Inventario", "grupo2", "grupo2", "inventario", 2),
        ("Grupo 3 Producción", "grupo3", "grupo3", "produccion", 3),
        ("Grupo 4 Logística", "grupo4", "grupo4", "logistica", 4),
        ("Grupo 5 Admin", "grupo5", "grupo5", "administrador", 5),
        ("Grupo 6 Auditoría", "grupo6", "grupo6", "auditor", 6),
        ("Grupo 7 Mantenimiento", "grupo7", "grupo7", "mantenimiento", 7),
    ]
    
    for u in usuarios:
        c.execute("SELECT * FROM usuarios WHERE usuario=%s", (u[1],))
        if not c.fetchone():
            c.execute("INSERT INTO usuarios (nombre, usuario, contraseña, rol, grupo_id) VALUES (%s, %s, %s, %s, %s)", u)

    conn.commit()
    conn.close()

def validar_usuario(usuario, contraseña):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE usuario=%s AND contraseña=%s", (usuario, contraseña))
    datos = c.fetchone()
    conn.close()
    return datos

def registrar_auditoria(accion, usuario):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO auditoria (accion, usuario) VALUES (%s, %s)", (accion, usuario))
    conn.commit()
    conn.close()
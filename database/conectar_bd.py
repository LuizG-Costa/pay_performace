import streamlit as st
import psycopg2

def conectar_bd():
    try:
        conn = psycopg2.connect(
            dbname=st.secrets["database"]["DB_NAME"],
            user=st.secrets["database"]["DB_USER"],
            password=st.secrets["database"]["DB_PASSWORD"],
            host=st.secrets["database"]["DB_HOST"],
            port=st.secrets["database"]["DB_PORT"],
            client_encoding="utf8"
        )
        return conn
    except psycopg2.Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

def get_connection():
    return psycopg2.connect(
        dbname=st.secrets["database"]["DB_NAME"],
        user=st.secrets["database"]["DB_USER"],
        password=st.secrets["database"]["DB_PASSWORD"],
        host=st.secrets["database"]["DB_HOST"],
        port=st.secrets["database"]["DB_PORT"],
        client_encoding="utf8"
    )

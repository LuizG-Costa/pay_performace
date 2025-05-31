import streamlit as st
from utils.componentes import renderizar_sidebar

renderizar_sidebar()

st.title("Usuario")

if st.button("Cadastrar Usuario"):
    st.switch_page("pages/Cadastrar_Usuario.py")
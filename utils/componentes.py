import streamlit as st

def renderizar_sidebar():
    with st.sidebar:
        st.write(f"👤 Usuário: {st.session_state.get('usuario')}")

        if st.button("🏠 Página Inicial"):
            st.switch_page("pages/home.py")  # ajuste conforme o nome do seu arquivo de home

        if st.button("Usuario"):
            st.switch_page("pages/Usuario.py")

        if st.button("🚪 Sair"):
            st.session_state["autenticado"] = False
            st.session_state["usuario"] = ""
            st.switch_page("login.py")


# UF DOS ESTADOS DO BRASIL
ufs = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

import streamlit as st
from utils.componentes import renderizar_sidebar


st.set_page_config(layout = "wide")

# Verifica se está logado
if "autenticado" not in st.session_state or not st.session_state["autenticado"]:
    st.warning("Você precisa fazer login para acessar esta página.")
    st.switch_page("login.py")

# Sidebar com botão de logout

# with st.sidebar:
#     st.write(f"👤 Usuário: {st.session_state['usuario']}")

#     if st.button("Cadastro Usuario"):
#         st.switch_page("pages/Cadastrar_Usuario.py")

#     if st.button("🚪 Sair"):
#         st.session_state["autenticado"] = False
#         st.session_state["usuario"] = ""
#         st.switch_page("login.py")

renderizar_sidebar()


st.title(f"Bem-Vindo {st.session_state['usuario']}")



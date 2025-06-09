import streamlit as st
from utils.transacoes import grafico_total_eth_por_funcionario
from utils.componentes import renderizar_sidebar
from utils.componentes import verificar_credenciais
from database.conectar_bd import get_connection





st.set_page_config(layout = "wide")

# Verifica se está logado
if "autenticado" not in st.session_state or not st.session_state["autenticado"]:
    st.warning("Você precisa estar logado para acessar esta página.")
    st.switch_page("pages/Login.py")


renderizar_sidebar()


if "usuario" in st.session_state:
    st.title(f"👋 Bem-vindo, {st.session_state['usuario']['nome_funcionario']}!")

st.markdown("---")
st.subheader("📊 ETH Transferido por Funcionário")
grafico_total_eth_por_funcionario()




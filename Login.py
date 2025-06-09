import streamlit as st
from utils.componentes import verificar_credenciais

#--------------------------------- NOTA DE VERSÃO ----------------------------------------------
#"Nesta versão, a avaliação de performance é feita manualmente pelo administrador da plataforma, 
# que atribui uma pontuação ao funcionário com base em critérios internos da empresa. A pontuação 
# é registrada na blockchain e utilizada para cálculo automático do bônus em ETH."
##-----------------------------------------------------------------------------------------------


#col1, col2 = st.columns(2)
#with col1:
    #st.title("Bem-Vindo à")
#with col2:
st.image("/Users/luizc/OneDrive/Documentos/PYTHON/pay_performace/image/pay_logo.png")


# @st.cache_data
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

# Redireciona se já estiver autenticado
if st.session_state["autenticado"]:
    st.switch_page("pages/Home.py")

# Formulário de login
with st.form("form_login"):
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    botao_login = st.form_submit_button("Entrar")

    if botao_login:
        funcionario = verificar_credenciais(email, senha)
        if funcionario:
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = funcionario  # armazena os dados do funcionário
            st.success("Login realizado com sucesso!")
            st.switch_page("pages/Home.py")
        else:
            st.error("E-mail ou senha incorretos.")



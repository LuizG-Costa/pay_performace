import streamlit as st


#col1, col2 = st.columns(2)
#with col1:
    #st.title("Bem-Vindo à")
#with col2:
st.image("/Users/luizc/OneDrive/Documentos/PYTHON/pay_performace/image/pay_logo.png")

# Simulação de banco de dados de usuários
USUARIOS = {
    "admin": "1234",
    "usuario": "senha123"
}
@st.cache_data
# Função para verificar credenciais
def verificar_credenciais(usuario, senha):
    return USUARIOS.get(usuario) == senha

# Inicialização do estado da sessão
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

# Se o usuário já estiver autenticado, redireciona para a página inicial
if st.session_state["autenticado"]:
    st.switch_page("pages/Home.py")


with st.form("form_login"):
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    botao_login = st.form_submit_button("Entrar")

    if botao_login:
        if verificar_credenciais(usuario, senha):
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = usuario
            st.success("Login realizado com sucesso!")
            st.switch_page("pages/Home.py")
        else:
            st.error("Usuário ou senha incorretos.")



if "autenticado" in st.session_state and st.session_state["autenticado"]:
    st.switch_page("pages/Home.py")



import streamlit as st
import re
from utils.componentes import renderizar_sidebar, ufs   
from datetime import date


if "autenticado" not in st.session_state or not st.session_state["autenticado"]:
    st.warning("Você precisa fazer login para acessar esta página.")
    st.switch_page("login.py")

# CHAMAR A FUNÇÃO SIDEBAR JÁ CRIADA DE utils/componentes.py
renderizar_sidebar()
# Conteúdo principal
st.title("Cadastro de Usuário")


# def formatar_cpf(cpf):
#     cpf = re.sub(r'\D', '', cpf)  # Remove tudo que não é dígito
#     if len(cpf) == 11:
#         return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
#     return cpf

with st.form("cad_func"):
    col1, col2, col3 = st.columns(3)
    with col1:
        matricula = st.text_input("Matricula")
    with col2:
        nome_func = st.text_input("Nome do Funcionario", placeholder="Nome e Sobrenome")
    with col3:
        senha = st.text_input("Senha", type="password", placeholder="Recomendado no minimo 8 caracteres")
    
    col4, col5, col6 = st.columns(3)
    with col4:
        cpf = st.text_input("CPF", placeholder="000.000.000-00")
    with col5:
        data_nasc = st.date_input("Data de Nascimento",  value=date(2000, 1, 1), format=("DD/MM/YYYY"), min_value=date(1900, 1, 1), max_value=date(2100, 12, 31),)
    with col6:
        data_admissao = st.date_input("Data de Admissão", value=None, format=("DD/MM/YYYY"), min_value=date(1900, 1, 1), max_value=date(2100, 12, 31),)
    
    col7, col8, col9 = st.columns(3)
    with col7:
        genero = st.radio("Genero de nascimento:",["Masculino", "Feminino"])
    with col8:
        telefone = st.text_input("Nº telefone/celular", placeholder="(00) 9 0000-0000")
    with col9:
        uf = st.selectbox("Selecione o Estado (UF)", ufs)
    
    col10, col11, col12, col13 = st.columns(4)
    with col10:
        cep = st.text_input("CEP", placeholder="00.000-000")
    with col11:
            endereço = st.text_input("Endereço", placeholder="Rua, Av.")
    with col12:
            bairro = st.text_input("Bairro", placeholder="Campinas, Brasilia")
    with col13:
        numero_residencia = st.text_input("Nº")
    
    compl = st.text_input("Complemento", placeholder="Cond, casa, sobrado")
        
    #checkbox_val = st.checkbox("Form checkbox")

    cadastrar = st.form_submit_button("Cadastrar")



# Fora do bloco "with st.form"
if cadastrar:
    erro = False

    if not nome_func.strip():
        st.error("⚠️ O campo *Nome* é obrigatório.")
        erro = True

    if not senha.strip():
        st.error("⚠️ O campo ***Senha*** é obrigatório.")
        erro = True

    if telefone and not telefone.isdigit():
        st.error("⚠️ Telefone/celular deve conter apenas números.")
        erro = True

    if matricula and not matricula.isdigit():
        st.error("⚠️ A matrícula deve conter apenas números.")
        erro = True

    if cpf and not cpf.isdigit():
        st.error("⚠️ CPF está faltando digito ou contém letra.")
        erro = True

    if not cpf.strip():
        st.error("⚠️ O campo ***CPF*** é obrigatório.")
        erro = True

    # cpf_limpo = re.sub(r'\D', '', cpf) # CONDIÇÃO DA FUNCAO ** def formatar_cpf **
    # if len(cpf_limpo) != 11:
    #     st.error("⚠️ O CPF deve conter 11 dígitos.")
    # else:
    #     cpf_formatado = formatar_cpf(cpf)

    if data_admissao is None:
        st.error("⚠️ Data de Admissão está em branco!")
        erro = True

    if data_nasc and data_admissao and data_nasc > data_admissao:
        st.error("⚠️ A data de nascimento não pode ser maior que a data de admissão.")
        erro = True

    if not erro:
        st.success(f"Funcionário {nome_func} cadastrado com sucesso!")

if st.button("Voltar"):
    st.switch_page("pages/Usuario.py")
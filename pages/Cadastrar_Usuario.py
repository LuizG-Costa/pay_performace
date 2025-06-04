import streamlit as st
import re
from datetime import date
from utils.componentes import renderizar_sidebar, ufs, est_civil
from utils.usarios_cadastrados import inserir_dados
from database.conectar_bd import conectar_bd

if "autenticado" not in st.session_state or not st.session_state["autenticado"]:
    st.warning("Você precisa fazer login para acessar esta página.")
    st.switch_page("login.py")

renderizar_sidebar()

st.title("✏️Cadastro de Usuário")

with st.form("cad_func"):
    # Campos do formulário...
    col1, col2, col3 = st.columns(3)
    with col1:
        matricula = st.text_input("Matricula*")
    with col2:
        nome_funcionario = st.text_input("Nome do Funcionario*", placeholder="Nome e Sobrenome")
    with col3:
        genero = st.radio("Genero de nascimento:*", ["Masculino", "Feminino"])

    col4, col5, col6 = st.columns(3)
    with col4:
        cpf = st.text_input("CPF*", max_chars=11, placeholder="000.000.000-00")
    with col5:
        data_nascimento = st.date_input(
            "Data de Nascimento*",
            value=date(2000, 1, 1),
            format=("DD/MM/YYYY"),
            min_value=date(1900, 1, 1),
            max_value=date(2100, 12, 31),
        )
    with col6:
        data_admissao = st.date_input(
            "Data de Admissão*",
            value=None,
            format=("DD/MM/YYYY"),
            min_value=date(1900, 1, 1),
            max_value=date(2100, 12, 31),
        )

    col7, col8, col9 = st.columns(3)
    with col7:
        estado_civil = st.selectbox("Estado Civil*", est_civil)
    with col8:
        telefone = st.text_input(
            "Nº telefone/celular", placeholder="(00) 9 0000-0000", max_chars=11
        )

    st.subheader("🏠 Endereço")
    col10, col11, col12, col13 = st.columns(4)
    with col10:
        cep = st.text_input("CEP*", max_chars=8, placeholder="00.000-000")
    with col11:
        uf = st.selectbox("Selecione o Estado (UF)*", ufs)
    with col12:
        bairro = st.text_input("Bairro*", placeholder="Campinas, Brasilia")
    with col13:
        numero_residencia = st.text_input("Nº")
    col14, col15 = st.columns(2)
    with col14:
        endereco = st.text_input("Endereço*", placeholder="Rua, Av.")
    with col15:
        complemento = st.text_input("Complemento", placeholder="Cond, casa, sobrado")

    st.subheader("👨‍💻Acesso")
    col16, col17 = st.columns(2)
    with col16:
        email = st.text_input(
            "Email*", placeholder="@gmail.com, @hotmail.com, @yahoo.com, etc"
        )
    with col17:
        senha = st.text_input(
            "Senha*", type="password", placeholder="Recomendado no minimo 8 caracteres"
        )

    if st.form_submit_button("Cadastrar"):
        # Coletar os dados do formulário
        dados_cadastro = {
            "matricula": matricula,
            "nome_funcionario": nome_funcionario,
            "genero": genero,
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "data_admissao": data_admissao,
            "estado_civil": estado_civil,
            "telefone": telefone,
            "cep": cep,
            "uf": uf,
            "bairro": bairro,
            "numero_residencia": numero_residencia,
            "endereco": endereco,
            "complemento": complemento,
            "email": email,
            "senha": senha,
        }

        # Conectar ao banco de dados
        conn = conectar_bd()
        if conn:
            # Inserir os dados no banco de dados
            inserir_dados(conn, dados_cadastro)
            # Fechar a conexão com o banco de dados
            conn.close()

if st.button("Voltar"):
    st.switch_page("pages/Usuario.py")

    # def formatar_cpf(cpf):
#     cpf = re.sub(r'\D', '', cpf)  # Remove tudo que não é dígito
#     if len(cpf) == 11:
#         return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
#     return cpf


# Fora do bloco "with st.form"

    # cpf_limpo = re.sub(r'\D', '', cpf) # CONDIÇÃO DA FUNCAO ** def formatar_cpf **
    # if len(cpf_limpo) != 11:
    #     st.error("⚠️ O CPF deve conter 11 dígitos.")
    # else:
    #     cpf_formatado = formatar_cpf(cpf)

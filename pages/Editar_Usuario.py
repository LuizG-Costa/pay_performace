import streamlit as st
from datetime import date, datetime
from utils.componentes import renderizar_sidebar, ufs, est_civil
from utils.usarios_cadastrados import inserir_dados, buscar_funcionario, atualizar_funcionario
from database.conectar_bd import conectar_bd
import time

st.set_page_config(layout="wide")
st.title("📝 Editar Usuário")

# Verifica autenticação
if "autenticado" not in st.session_state or not st.session_state["autenticado"]:
    st.warning("Você precisa fazer login para acessar esta página.")
    st.switch_page("login.py")

renderizar_sidebar()

conn = conectar_bd()
dados_existentes = None
modo_edicao = False

# Verifica se está em modo edição
if "matricula_editar" in st.session_state:
    matricula_editar = st.session_state["matricula_editar"]
    dados_existentes = buscar_funcionario(conn, matricula_editar)
    modo_edicao = True

# FORMULÁRIO DE CADASTRO / EDIÇÃO
with st.form("cad_func"):
    col1, col2, col3 = st.columns(3)
    with col1:
        matricula = st.text_input("Matricula*", value=dados_existentes["matricula"] if dados_existentes else "", disabled=modo_edicao)
    with col2:
        nome_funcionario = st.text_input("Nome do Funcionario*", placeholder="Nome e Sobrenome", value=dados_existentes["nome_funcionario"] if dados_existentes else "")
    with col3:
        genero = st.radio("Genero de nascimento:*", ["Masculino", "Feminino"], index=0 if (dados_existentes and dados_existentes["genero"] == "Masculino") else 1)

    col4, col5, col6 = st.columns(3)
    with col4:
        cpf = st.text_input("CPF*", max_chars=11, placeholder="000.000.000-00", value=dados_existentes["cpf"] if dados_existentes else "")
    with col5:
        data_nascimento = st.date_input(
            "Data de Nascimento*",
            value=dados_existentes["data_nascimento"] if dados_existentes else date(2000, 1, 1),
            format="DD/MM/YYYY",
            min_value=date(1900, 1, 1),
            max_value=date(2100, 12, 31),
        )
    with col6:
        data_admissao = st.date_input(
            "Data de Admissão*",
            value=dados_existentes["data_admissao"] if dados_existentes else date.today(),
            format="DD/MM/YYYY",
            min_value=date(1900, 1, 1),
            max_value=date(2100, 12, 31),
        )

    col7, col8, col9 = st.columns(3)
    with col7:
        estado_civil = st.selectbox("Estado Civil*", est_civil,
                                    index=est_civil.index(dados_existentes["estado_civil"]) if dados_existentes else 0)
    with col8:
        telefone = st.text_input("Nº telefone/celular", placeholder="(00) 9 0000-0000", max_chars=11, value=dados_existentes["telefone"] if dados_existentes else "")

    st.subheader("🏠 Endereço")
    col10, col11, col12, col13 = st.columns(4)
    with col10:
        cep = st.text_input("CEP*", max_chars=8, placeholder="00.000-000", value=dados_existentes["cep"] if dados_existentes else "")
    with col11:
        uf = st.selectbox("Selecione o Estado (UF)*", ufs, index=ufs.index(dados_existentes["uf"]) if dados_existentes else 0)
    with col12:
        bairro = st.text_input("Bairro*", placeholder="Campinas, Brasilia", value=dados_existentes["bairro"] if dados_existentes else "")
    with col13:
        numero_residencia = st.text_input("Nº", value=dados_existentes["numero_residencia"] if dados_existentes else "")

    col14, col15 = st.columns(2)
    with col14:
        endereco = st.text_input("Endereço*", placeholder="Rua, Av.", value=dados_existentes["endereco"] if dados_existentes else "")
    with col15:
        # Correção do KeyError: Use .get() com um valor padrão
        complemento = st.text_input("Complemento", placeholder="Cond, casa, sobrado", value=dados_existentes.get("complemento", "") if dados_existentes else "")

    st.subheader("👨‍💻 Acesso")
    col16, col17 = st.columns(2)
    with col16:
        email = st.text_input("Email*", placeholder="@gmail.com", value=dados_existentes["email"] if dados_existentes else "")
    with col17:
        senha = st.text_input("Senha*", type="password", placeholder="Mínimo 8 caracteres", value=dados_existentes["senha"] if dados_existentes else "")

    # Botão de envio
    if st.form_submit_button("Atualizar Cadastro" if modo_edicao else "Cadastrar"):
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

        if conn:
            if modo_edicao:
                atualizar_funcionario(conn, dados_cadastro)
                st.success("Cadastro atualizado com sucesso!")
                del st.session_state["matricula_editar"]
                time.sleep(2)  # Aguardar 2 segundos antes de redirecionar
                st.switch_page("pages/Usuario.py")
            # else:
            #     inserir_dados(conn, dados_cadastro)
            #     st.success("Funcionário cadastrado com sucesso!")
            conn.close()

# Botão para voltar
if st.button("Voltar"):
    st.switch_page("pages/Usuario.py")


# TEM ALGUM ERRO NESSE TROço QUE QUANDO TENTO EDITAR DUAS VEZES SEGUIDAS, ELE VAI PARA A TELA DE CADASTRO, PROVAVELMENTE VOU COLOCAR UM TIME.OUT PARA VOLTAR PARA TELA DE USUÁRIOS E CONTORNAR O BUG AAAA
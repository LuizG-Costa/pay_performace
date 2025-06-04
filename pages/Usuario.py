import streamlit as st
import pandas as pd
from utils.componentes import renderizar_sidebar, exportar_funcionarios_para_csv
from utils.consultas import listar_funcionarios
from utils.info_bancario import inserir_ou_atualizar_banco_funcionario, buscar_info_banco

#✅ Função para redirecionar à página de edição
# #def ir_para_edicao(matricula):
#    # st.session_state["matricula_editar"] = matricula
#    # st.switch_page("pages/Editar_Usuario.py")

st.set_page_config(layout="wide")
renderizar_sidebar()

st.title("Usuário")


col1, col2 = st.columns([1, 8])  # Coluna para o título e coluna para o botão
with col1:
    if st.button("✏️Cadastrar Usuário"):
        st.session_state["pagina_cadastro_usuario"] = True
        st.switch_page("pages/Cadastrar_Usuario.py")
    
with col2:
    if st.download_button(
    label="📥 Exportar Funcionários",
    data=exportar_funcionarios_para_csv(),
    file_name="funcionarios.csv",
    mime="text/csv"
    ):
        st.success("Funcionários exportados com sucesso!")

st.write("---")

st.title("👥 Funcionários Cadastrados")

funcionarios = listar_funcionarios()

if funcionarios:
    colunas = ["Matrícula", "Nome", "CPF", "E-mail", "Data de Admissão"]
    df = pd.DataFrame(funcionarios, columns=colunas)

    for i, row in df.iterrows():
        col1, col2 = st.columns([13, 1])  # Nome + botão Editar

        with col1:
            st.markdown(f"### {row['Nome']} - Mat.: {row['Matrícula']}")

        with col2:
            if st.button("📝Editar", key=f"editar_{i}"):
                st.session_state["matricula_editar"] = row["Matrícula"]
                st.switch_page("pages/Editar_Usuario.py")

        st.write(f"CPF: {row['CPF']} | E-mail: {row['E-mail']}")

        with st.expander("➕ Inserir/Editar Banco"):
            dados_existentes = buscar_info_banco(row["Matrícula"])
            tipo_existente = dados_existentes[2] if dados_existentes else "Banco Tradicional"

            tipo_banco = st.radio(
                f"Escolha o tipo de banco para {row['Nome']}",
                ["Banco Tradicional", "Blockchain"],
                index=0 if tipo_existente == "Banco Tradicional" else 1,
                key=f"banco_{i}"
            )

            nome_banco = dados_existentes[3] if dados_existentes else ""
            agencia = dados_existentes[4] if dados_existentes else ""
            conta = dados_existentes[5] if dados_existentes else ""
            tipo_conta = dados_existentes[6] if dados_existentes else "Corrente"
            carteira_blockchain = dados_existentes[7] if dados_existentes else ""

            if tipo_banco == "Banco Tradicional":
                nome_banco = st.text_input("Nome do Banco", value=nome_banco, key=f"nome_banco_{i}")
                agencia = st.text_input("Agência", value=agencia, key=f"agencia_{i}")
                conta = st.text_input("Conta", value=conta, key=f"conta_{i}")
                tipo_conta = st.selectbox("Tipo de Conta", ["Corrente", "Poupança"], index=0 if tipo_conta == "Corrente" else 1, key=f"tipo_conta_{i}")
                carteira_blockchain = None

            elif tipo_banco == "Blockchain":
                carteira_blockchain = st.text_input("URL da Carteira Blockchain", value=carteira_blockchain, key=f"blockchain_{i}")
                nome_banco = agencia = conta = tipo_conta = None

            if st.button("Salvar", key=f"salvar_banco_{i}"):
                inserir_ou_atualizar_banco_funcionario(
                    matricula=row["Matrícula"],
                    tipo_banco=tipo_banco,
                    nome_banco=nome_banco,
                    agencia=agencia,
                    conta=conta,
                    tipo_conta=tipo_conta,
                    carteira_blockchain=carteira_blockchain
                )
                st.success(f"Banco '{tipo_banco}' salvo/atualizado com sucesso para {row['Nome']}!")
        st.write(" --- ")
else:
    st.info("Nenhum funcionário cadastrado ainda.")



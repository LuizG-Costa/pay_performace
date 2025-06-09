import streamlit as st
from datetime import date
import pandas as pd
from datetime import datetime, timedelta
from web3 import Web3
from utils.consultas import listar_funcionarios
from utils.componentes import renderizar_sidebar
from utils.info_bancario import buscar_info_banco
from utils.blockchain import transferir_eth
from utils.transacoes import registrar_transacao, buscar_transacoes_periodo, exportar_csv_por_funcionario, exportar_csv_funcionarios_geral, buscar_total_eth_enviado


if "autenticado" not in st.session_state or not st.session_state["autenticado"]:
    st.warning("Você precisa estar logado para acessar esta página.")
    st.switch_page("pages/Login.py")


#st.set_page_config(layout="wide")
renderizar_sidebar()

st.page_title="🪙 Transação Blockchain"
st.title("🪙 Transações Blockchain")

# Selecionar funcionário
funcionarios = listar_funcionarios()
matriculas = {f"{f[1]} - Mat.: {f[0]}": f[0] for f in funcionarios}  # Nome (matricula)

nome_selecionado = st.selectbox("Selecione um funcionário ou digite para pesquisar", list(matriculas.keys()))
matricula = matriculas[nome_selecionado]

# Buscar carteira e mostrar bônus
dados = buscar_info_banco(matricula)
carteira = dados[7] if dados else None

col1, col2 = st.columns(2)

with col1:
    st.text_input("Carteira Blockchain", value=carteira if carteira else "Não cadastrada", disabled=True)

with col2:
    if carteira:
        try:
            carteira_checksum = Web3.to_checksum_address(carteira)
            total_eth = buscar_total_eth_enviado(matricula)
            st.metric("💰 ETH já transferido", f"{total_eth:.3f} ETH")
        except Exception as e:
            st.warning(f"Erro ao consultar bônus: {e}")
    else:
        st.warning("Carteira não cadastrada")

# Botão de transferência
st.markdown("---")
st.subheader("🏦 Realizar Transferência de ETH")

valor_eth = st.number_input("Valor a transferir (ETH)", min_value=0.0, step=0.01, format="%.5f")

if st.button("💳 Transferir ETH"):
    resultado = transferir_eth(carteira, valor_eth)
    if "Erro" in resultado:
        st.error(resultado)
    else:
        registrar_transacao(matricula, carteira, valor_eth, resultado)
        st.success(f"Transação realizada com sucesso! Hash: {resultado}")

# Filtro de período
st.markdown("---")
st.subheader("🔍 Histórico de Transações")

filtro = st.selectbox("Filtrar por", ["Hoje", "Esta semana", "Este mês", "Este ano"])
data_inicio = datetime.now()

if filtro == "Hoje":
    data_inicio = datetime.now().replace(hour=0, minute=0, second=0)
elif filtro == "Esta semana":
    data_inicio -= timedelta(days=datetime.now().weekday())
elif filtro == "Este mês":
    data_inicio = data_inicio.replace(day=1)
elif filtro == "Este ano":
    data_inicio = data_inicio.replace(month=1, day=1)

transacoes = buscar_transacoes_periodo(matricula, data_inicio)

if transacoes:
    df = pd.DataFrame(transacoes, columns=["Data", "Carteira", "Valor ETH", "Hash"])
    df["Data"] = df["Data"].astype(str)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Nenhuma transação encontrada para o período.")

# Exportar CSV
st.markdown("---")
st.subheader("📃 Exportar Relatório")
col_data1, col_data2 = st.columns(2)

with col_data1:
    data_de = st.date_input("De:", value=datetime.now() - timedelta(days=7),
            format=("DD/MM/YYYY"),
            min_value=date(1900, 1, 1),
            max_value=date(2100, 12, 31))

with col_data2:
    data_ate = st.date_input("Até:", 
            value=datetime.now(),
            format=("DD/MM/YYYY"),
            min_value=date(1900, 1, 1),
            max_value=date(2100, 12, 31))

data_de = datetime.combine(data_de, datetime.min.time())
data_ate = datetime.combine(data_ate, datetime.max.time())
csv1 = exportar_csv_por_funcionario(matricula, data_de, data_ate)
csv2 = exportar_csv_funcionarios_geral(data_de, data_ate)

col_csv1, col_csv2 = st.columns([1, 5])

if csv1.strip():
    with col_csv1:
        st.download_button(
            label="📥 Baixar CSV do Funcionário",
            data=csv1,
            file_name=f"transacoes - {matricula}.csv",
            mime="text/csv"
    )
if csv2.strip():
    with col_csv2:
            st.download_button(
                label="📥 Baixar CSV de todos Funcionário",
                data=csv2,
                file_name=f"transacoes_todos_funcionario.csv",
                mime="text/csv"
            )
else:
    st.warning("⚠️ Nenhuma transação encontrada no intervalo selecionado.")


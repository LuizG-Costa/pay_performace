import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
from io import StringIO
from datetime import date, datetime, timedelta
from database.conectar_bd import get_connection


# PÀGINA DEDICADO AO "TRANSICAO_BLOCKCHAIN"

# Registrar uma transação no banco de dados
def registrar_transacao(matricula, endereco_wallet, valor_eth, tx_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transacoes_blockchain (matricula, endereco_wallet, valor_eth, tx_hash)
        VALUES (%s, %s, %s, %s)
    """, (matricula, endereco_wallet, valor_eth, tx_hash))
    conn.commit()
    cursor.close()
    conn.close()

# Buscar transações de um funcionário em um período
def buscar_transacoes_periodo(matricula, data_inicio):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT data_transacao, endereco_wallet, valor_eth, tx_hash
        FROM transacoes_blockchain
        WHERE matricula = %s AND data_transacao >= %s
        ORDER BY data_transacao DESC
    """, (matricula, data_inicio))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados


def buscar_total_eth_enviado(matricula):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(valor_eth), 0)
        FROM transacoes_blockchain
        WHERE matricula = %s
    """, (matricula,))
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return float(total)


# Exportar CSV com transações de TODOS os funcionários filtradas por data
def exportar_csv_funcionarios_geral(data_de, data_ate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.nome_funcionario, t.matricula, t.endereco_wallet, t.valor_eth, t.tx_hash, t.data_transacao
        FROM transacoes_blockchain t
        JOIN funcionarios f ON f.matricula = t.matricula
        WHERE t.data_transacao BETWEEN %s AND %s
        ORDER BY t.data_transacao DESC
    """, (data_de, data_ate))

    dados = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(dados, columns=[
        "Nome", "Matricula", "Carteira", "Valor (ETH)", "Hash", "Data"
    ])

    if df.empty:
        return "Nome;Matricula;Carteira;Valor (ETH);Hash;Data\n"

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, sep=';', date_format='%d/%m/%Y %H:%M:%S')
    return csv_buffer.getvalue()


# Exportar CSV com transações de um FUNCIONÁRIO ESPECÍFICO filtradas por data
def exportar_csv_por_funcionario(matricula, data_de, data_ate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.nome_funcionario, t.matricula, t.endereco_wallet, t.valor_eth, t.tx_hash, t.data_transacao
        FROM transacoes_blockchain t
        JOIN funcionarios f ON f.matricula = t.matricula
        WHERE t.matricula = %s AND t.data_transacao BETWEEN %s AND %s
        ORDER BY t.data_transacao DESC
    """, (matricula, data_de, data_ate))

    dados = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(dados, columns=[
        "Nome", "Matricula", "Carteira", "Valor (ETH)", "Hash", "Data"
    ])

    if df.empty:
        return "Nome;Matricula;Carteira;Valor (ETH);Hash;Data\n"

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, sep=';', date_format='%d/%m/%Y %H:%M:%S')

    return csv_buffer.getvalue()


# Gerar gráfico de total de ETH enviados por funcionário
def grafico_total_eth_por_funcionario():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.nome_funcionario, SUM(t.valor_eth) as total_eth
        FROM transacoes_blockchain t
        JOIN funcionarios f ON f.matricula = t.matricula
        GROUP BY f.nome_funcionario
        ORDER BY total_eth DESC
    """)
    dados = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(dados, columns=["Funcionário", "Total ETH"])
    if not df.empty:
        fig = px.bar(df, x="Funcionário", y="Total ETH", text="Total ETH",
            title="Total de ETH transferido por Funcionário",
            labels={"Total ETH": "ETH Enviado"})
        fig.update_traces(texttemplate='%{text:.4f}', textposition='outside')
        fig.update_layout(xaxis_tickangle=-45, height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhuma transação registrada ainda para gerar o gráfico.")

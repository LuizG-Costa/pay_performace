import streamlit as st
import pandas as pd
import io
from database.conectar_bd import conectar_bd

def renderizar_sidebar():
    with st.sidebar:
        st.write(f"👤 Usuário: {st.session_state['usuario']['nome_funcionario']}")

        if st.button("🏠 Página Inicial"):
            st.switch_page("pages/home.py")  # ajuste conforme o nome do seu arquivo de home

        if st.button("🧑‍💼   Usuario"):
            st.switch_page("pages/Usuario.py")

        if st.button("🪙 Transações Blockchain"):
            st.switch_page("pages/Transicao_Blockchain.py")
        
        if st.button("💵 Transações Tradicional"):
            st.switch_page("pages/Pagamento_Tradicional.py")

        if "usuario" in st.session_state and st.session_state["usuario"]["email"] == "admin@oculto.com":
            if st.button("📊 Contrato Blockchain"):
                st.switch_page("pages/contrato_blockchain.py")
        #else:
            #t.error("Acesso restrito! Esta página é apenas para testes internos.")

        if st.button("🚪 Sair"):
            st.session_state["autenticado"] = False
            st.session_state["usuario"] = ""
            st.switch_page("Login.py")


# UF DOS ESTADOS DO BRASIL
ufs = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

# ESTADOS CIVIS DO CADASTRO DE FUNCIONÁRIOS/USUARIOS
est_civil = [
    "Solteiro(a)",
    "Casado(a)",
    "Separado(a) judicialmente",
    "Divorciado(a)",
    "Viúvo(a)",
    "União estável"
]


def exportar_funcionarios_para_csv():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM funcionarios")
    colunas = [desc[0] for desc in cursor.description]
    dados = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(dados, columns=colunas)

    # Remove a coluna 'senha', se existir
    if 'senha' in df.columns:
        df.drop(columns=['senha'], inplace=True),
    
    if "id" in df.columns:
        df.drop( columns=["id"], inplace=True)

    # Gera CSV em memória
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, sep=';')  # usa ; para compatibilidade com Excel em PT-BR
    return buffer.getvalue()


# Função para verificar as credenciais do usuário e fazer o login na plataforma
def verificar_credenciais(email, senha):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM funcionarios 
        WHERE email = %s AND senha = %s
    """, (email, senha))
    row = cursor.fetchone()
    colunas = [desc[0] for desc in cursor.description]
    conn.close()
    return dict(zip(colunas, row)) if row else None

import streamlit as st
import psycopg2
from datetime import date
from database.conectar_bd import get_connection

#INSERIR OS DADOS NO BANCO DE DADOS
def inserir_dados(conn, dados):
    """Função para inserir os dados do formulário no banco de dados."""
    cursor = conn.cursor()
    query = """
    INSERT INTO funcionarios (
        matricula, nome_funcionario, genero, cpf, data_nascimento, data_admissao,
        estado_civil, telefone, cep, uf, bairro, numero_residencia, endereco,
        complemento, email, senha, data_cadastro
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        cursor.execute(query, (
            dados["matricula"], dados["nome_funcionario"], dados["genero"], dados["cpf"],
            dados["data_nascimento"], dados["data_admissao"], dados["estado_civil"],
            dados["telefone"], dados["cep"], dados["uf"], dados["bairro"],
            dados["numero_residencia"], dados["endereco"], dados["complemento"],
            dados["email"], dados["senha"], date.today()
        ))
        conn.commit()
        st.success("Usuário cadastrado com sucesso!")
    except psycopg2.Error as e:
        conn.rollback()
        st.error(f"Erro ao inserir dados no banco de dados: {e}")
    finally:
        cursor.close()




def buscar_funcionario(conn, matricula):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM funcionarios WHERE matricula = %s", (matricula,))
    colunas = [desc[0] for desc in cursor.description]
    dados = cursor.fetchone()
    return dict(zip(colunas, dados)) if dados else None


# Função para atualizar os dados do funcionário no banco de dados
def atualizar_funcionario(conn, dados):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE funcionarios SET
            nome_funcionario = %s,
            genero = %s,
            cpf = %s,
            data_nascimento = %s,
            data_admissao = %s,
            estado_civil = %s,
            telefone = %s,
            cep = %s,
            uf = %s,
            bairro = %s,
            numero_residencia = %s,
            endereco = %s,
            complemento = %s,
            email = %s,
            senha = %s
        WHERE matricula = %s
    """, (
        dados["nome_funcionario"], dados["genero"], dados["cpf"],
        dados["data_nascimento"], dados["data_admissao"], dados["estado_civil"],
        dados["telefone"], dados["cep"], dados["uf"], dados["bairro"],
        dados["numero_residencia"], dados["endereco"], dados["complemento"],
        dados["email"], dados["senha"], dados["matricula"]
    ))
    conn.commit()


# def buscar_funcionarios_com_tipo_banco(tipo_banco): # Removido 'conn' e 'matricula' daqui
    # conn = get_connection() # Obter a conexão aqui
    # cursor = conn.cursor()
    # cursor.execute("""
        # SELECT
            # f.matricula,
            # f.nome_funcionario,
            # ib.nome_banco,
            # ib.agencia,
            # ib.conta,
            # ib.tipo_conta,
            # ib.carteira_blockchain
        # FROM
            # funcionarios f
        # JOIN
            # informacoes_bancarias ib ON f.matricula = ib.matricula
        # WHERE
            # ib.tipo_banco = %s
    # """, (tipo_banco,))
    # funcionarios = cursor.fetchall()
    # cursor.close()
    # conn.close() # Fechar a conexão
    # return funcionarios

def buscar_funcionario(matricula):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM funcionarios WHERE matricula = %s", (matricula,))
    dados = cursor.fetchone()
    cursor.close()
    conn.close()
    return dados

# Buscar todos os funcionários cadastrados
def buscar_todos_funcionarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT matricula, nome_funcionario, email FROM funcionarios ORDER BY nome_funcionario")
    funcionarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return funcionarios

# Atualizar dados do funcionário
def atualizar_funcionario(dados):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE funcionarios SET
            nome_funcionario = %s,
            genero = %s,
            cpf = %s,
            data_nascimento = %s,
            data_admissao = %s,
            estado_civil = %s,
            telefone = %s,
            cep = %s,
            uf = %s,
            bairro = %s,
            numero_residencia = %s,
            endereco = %s,
            complemento = %s,
            email = %s
        WHERE matricula = %s
    """, (
        dados['nome_funcionario'], dados['genero'], dados['cpf'],
        dados['data_nascimento'], dados['data_admissao'], dados['estado_civil'],
        dados['telefone'], dados['cep'], dados['uf'], dados['bairro'],
        dados['numero_residencia'], dados['endereco'], dados['complemento'],
        dados['email'], dados['matricula']
    ))
    conn.commit()
    cursor.close()
    conn.close()

# Buscar funcionários com banco tradicional
def buscar_funcionarios_com_tipo_banco(tipo_banco):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.matricula, f.nome_funcionario, b.nome_banco, b.agencia, b.conta, b.tipo_conta
        FROM funcionarios f
        JOIN info_bancario b ON f.matricula = b.matricula
        WHERE b.tipo_banco = %s
        ORDER BY f.nome_funcionario
    """, (tipo_banco,))
    funcionarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return funcionarios
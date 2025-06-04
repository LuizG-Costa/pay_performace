import streamlit as st
import psycopg2
from datetime import date

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
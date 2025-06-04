from database.conectar_bd import get_connection

def inserir_ou_atualizar_banco_funcionario(matricula, tipo_banco, nome_banco, agencia, conta, tipo_conta, carteira_blockchain):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM info_bancario WHERE matricula = %s", (matricula,))
    existe = cursor.fetchone()

    if existe:
        cursor.execute("""
            UPDATE info_bancario
            SET tipo_banco = %s,
                nome_banco = %s,
                agencia = %s,
                conta = %s,
                tipo_conta = %s,
                carteira_blockchain = %s,
                data_cadastro = CURRENT_TIMESTAMP
            WHERE matricula = %s
        """, (tipo_banco, nome_banco, agencia, conta, tipo_conta, carteira_blockchain, matricula))
    else:
        cursor.execute("""
            INSERT INTO info_bancario (
                matricula, tipo_banco,
                nome_banco, agencia, conta, tipo_conta,
                carteira_blockchain
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (matricula, tipo_banco, nome_banco, agencia, conta, tipo_conta, carteira_blockchain))

    conn.commit()
    conn.close()

def buscar_info_banco(matricula):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM info_bancario WHERE matricula = %s", (matricula,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado
from database.conectar_bd import get_connection

def listar_funcionarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT matricula, nome_funcionario, cpf, email, data_admissao
        FROM funcionarios
        WHERE visivel_no_sistema = TRUE
    """)
    resultado = cursor.fetchall()
    conn.close()
    return resultado


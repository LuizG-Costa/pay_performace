import psycopg2
import pandas as pd
import io
from io import StringIO
from datetime import datetime
from database.conectar_bd import get_connection

# Registrar um pagamento tradicional
def registrar_pagamento_tradicional(matricula, nome_banco, agencia, conta, tipo_conta, valor_pago, descricao):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pagamentos_tradicionais (
            matricula, nome_banco, agencia, conta, tipo_conta, valor_pago, descricao
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (matricula, nome_banco, agencia, conta, tipo_conta, valor_pago, descricao))
    conn.commit()
    cursor.close()
    conn.close()

# Buscar pagamentos por funcionário
def buscar_pagamentos_por_funcionario(matricula):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT data_pagamento, valor_pago, descricao, nome_banco, agencia, conta, tipo_conta
        FROM pagamentos_tradicionais
        WHERE matricula = %s
        ORDER BY data_pagamento DESC
    """, (matricula,))
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados

# Exportar pagamentos para CSV por período
def exportar_csv_pagamentos_tradicionais(data_de, data_ate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.nome_funcionario, p.matricula, p.valor_pago, p.descricao, p.nome_banco, p.agencia, p.conta, p.tipo_conta, p.data_pagamento
        FROM pagamentos_tradicionais p
        JOIN funcionarios f ON f.matricula = p.matricula
        WHERE p.data_pagamento BETWEEN %s AND %s
        ORDER BY p.data_pagamento DESC
    """, (data_de, data_ate))
    dados = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(dados, columns=[
        "Nome", "Matrícula", "Valor Pago", "Descrição", "Banco", "Agência", "Conta", "Tipo", "Data"
    ])

    if df.empty:
        return "Nome;Matrícula;Valor Pago;Descrição;Banco;Agência;Conta;Tipo;Data\n"

    csv_bytes = io.BytesIO()
    csv_bytes.write(df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig'))
    csv_bytes.seek(0)
    return csv_bytes.getvalue()

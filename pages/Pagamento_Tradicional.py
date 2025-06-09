import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.pagamento_tradicional import (
    registrar_pagamento_tradicional,
    buscar_pagamentos_por_funcionario,
    exportar_csv_pagamentos_tradicionais
)
from datetime import datetime, timedelta
from utils.usarios_cadastrados import buscar_funcionarios_com_tipo_banco # Importação atualizada
from utils.componentes import renderizar_sidebar



if "autenticado" not in st.session_state or not st.session_state["autenticado"]:
    st.warning("Você precisa estar logado para acessar esta página.")
    st.switch_page("pages/Login.py")

st.page_title= "💵 Pagamento Tradicional"
st.title("💵 Pagamento - Banco Tradicional")

renderizar_sidebar()

# Selecionar funcionário com banco tradicional
# AQUI ESTÁ A CHAMADA CORRETA:
# Selecionar funcionário com banco tradicional
funcionarios = buscar_funcionarios_com_tipo_banco("Banco Tradicional")

if not funcionarios:
    st.warning("Nenhum funcionário com conta tradicional cadastrado.")
    st.stop()

nomes = [f"{f[1]} ({f[0]})" for f in funcionarios]
selecionado = st.selectbox("Selecione o funcionário:", nomes)

matricula = selecionado.split("(")[-1].strip(")")
func = next(f for f in funcionarios if f[0] == matricula)

st.markdown("---")


st.subheader("📋 Dados bancários")
st.write(f"**Banco:** {func[2]}  ")
st.write(f"**Agência:** {func[3]} | **Conta:** {func[4]} | **Tipo:** {func[5]}")

# Formulário de simulação de pagamento
st.subheader("📝 Registrar Pagamento")
valor = st.number_input("Valor a ser pago (R$):", min_value=0.01, step=0.01, format="%.2f")
descricao = st.text_input("Descrição do pagamento", placeholder="Ex: Bônus por desempenho")

if st.button("💳 Registrar Pagamento"):
    registrar_pagamento_tradicional(
        matricula=func[0],
        nome_banco=func[2],
        agencia=func[3],
        conta=func[4],
        tipo_conta=func[5],
        valor_pago=valor,
        descricao=descricao
    )
    st.success("Pagamento simulado registrado com sucesso!")

st.markdown("---")

# Mostrar histórico
st.subheader("📄 Pagamentos Registrados")

pagamentos = buscar_pagamentos_por_funcionario(func[0])
pagamentos_filtrados = [(p[0], p[1], p[2]) for p in pagamentos]  # Data, Valor, Descrição
if pagamentos:
    df_pagamentos = pd.DataFrame(pagamentos_filtrados, columns=["Data", "Valor Pago (R$)", "Descrição"])
    df_pagamentos["Data"] = pd.to_datetime(df_pagamentos["Data"]).dt.strftime("%d/%m/%Y %H:%M")
    st.dataframe(df_pagamentos, use_container_width=True)
else:
    st.info("Nenhum pagamento registrado para este funcionário.")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    data_ini = st.date_input("De:", value=datetime.now() - timedelta(days=30), format="DD/MM/YYYY")
with col2:
    data_fim = st.date_input("Até:", value=datetime.now(), format="DD/MM/YYYY")

csv = exportar_csv_pagamentos_tradicionais(
    datetime.combine(data_ini, datetime.min.time()),
    datetime.combine(data_fim, datetime.max.time())
)

st.download_button(
    label="📥 Baixar CSV",
    data=csv,
    file_name="pagamentos_tradicionais.csv",
    mime="text/csv"
)
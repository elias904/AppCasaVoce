import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Processador de Vendas", layout="wide")

# Dicionário dos meses
meses = {
    "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4, "maio": 5, "junho": 6,
    "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
}

# Função para converter a data
def converter_data_venda(data_str):
    try:
        partes = data_str.split()
        dia = partes[0]
        mes = f"{meses[partes[2].lower()]}"
        ano = partes[4]
        hora_minuto = partes[5]
        return f"{dia}/{mes}/{ano} {hora_minuto}"
    except:
        return pd.NaT

# Função para agrupar a hora
def agrupar_hora_venda(data_str):
    try:
        partes = data_str.split()
        hora_minuto = partes[1]
        hora, minuto = map(int, hora_minuto.split(":"))
        if 0 <= minuto < 15:
            minuto = 0
        elif 15 <= minuto < 45:
            minuto = 30
        else:
            minuto = 0
            hora = (hora + 1) % 24
        return f"{hora:02d}:{minuto:02d}"
    except:
        return pd.NaT

# Função para obter o SKU pai
def sku_pai(data_str):
    try:
        return data_str[:-1]
    except:
        return pd.NaT

st.title("📊 Processador de Vendas para Power BI")

uploaded_file = st.file_uploader("Faça o upload do arquivo Excel (.xlsx)", type="xlsx")

if uploaded_file:
    # Lê a planilha
    df = pd.read_excel(uploaded_file, sheet_name="Vendas BR", skiprows=5)

    # Processa os dados
    df["N.º de venda"] = df["N.º de venda"].astype(str)
    df["Data da venda"] = df["Data da venda"].apply(converter_data_venda)
    df["Hora agrupada"] = df["Data da venda"].apply(agrupar_hora_venda)
    df["SKU pai"] = df["SKU"].apply(sku_pai)

    st.success("Arquivo processado com sucesso!")

    # Exibe uma prévia
    st.subheader("Prévia dos dados processados")
    st.dataframe(df.head())

    # Gerar Excel com aba "Todos os Dados"
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Todos os Dados", index=False)
    buffer.seek(0)

    # Botão para download do Excel
    st.download_button(
        label="📥 Baixar Excel Processado",
        data=buffer,
        file_name="vendas_processadas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

import streamlit as st
import pandas as pd

st.title("SISTEMA DE EMERGÊNCIA - TMS FRANCAL")

# Link de Publicação direto da Aba 'Clientes' que você gerou
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-k3doFN8BGK5YL9su9avmaFLgV97SbE3erJdh0YDJxACO3nNrYX6XTO0a7rhRtUN9xcdeIsLWurAr/pub?gid=1756592231&single=true&output=csv"

try:
    st.write("Tentando conectar à planilha...")
    df = pd.read_csv(URL)
    st.success("Conexão feita com sucesso!")
    st.write("Colunas encontradas:", df.columns.tolist())
    st.dataframe(df.head())
except Exception as e:
    st.error(f"Erro crítico: {e}")
    st.info("Verifique se o link da publicação na web está correto e se a aba 'Clientes' foi publicada.")

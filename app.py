import streamlit as st
import pandas as pd

st.title("DIAGNÓSTICO DA PLANILHA")

uploaded_file = st.file_uploader("Suba o arquivo base_Geral.xlsx", type=["xlsx"])

if uploaded_file is not None:
    try:
        xl = pd.ExcelFile(uploaded_file)
        st.write("### Abas encontradas na planilha que você subiu:")
        st.write(xl.sheet_names)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

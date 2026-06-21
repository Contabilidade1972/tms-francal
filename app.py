import streamlit as st
import pandas as pd

st.title("TMS FRANCAL - DIAGNÓSTICO DE COLUNAS")

uploaded_file = st.file_uploader("Selecione o arquivo base_Geral.xlsx", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, sheet_name=0, engine='openpyxl')
        st.success("Planilha carregada!")
        
        # MOSTRA AS COLUNAS PARA VOCÊ
        st.write("### As colunas que o sistema enxerga são:")
        st.write(df.columns.tolist())
        
        # MOSTRA OS DADOS DA PRIMEIRA LINHA PARA CONFERÊNCIA
        st.write("### Exemplo dos dados (primeira linha):")
        st.write(df.iloc[0])
        
    except Exception as e:
        st.error(f"Erro: {e}")

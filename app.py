import streamlit as st
import pandas as pd

st.title("TMS FRANCAL - DIAGNÓSTICO DE ABAS")

# URL da aba "Clientes" que você publicou
URL_CLIENTES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-k3doFN8BGK5YL9su9avmaFLgV97SbE3erJdh0YDJxACO3nNrYX6XTO0a7rhRtUN9xcdeIsLWurAr/pub?gid=1756592231&single=true&output=csv"

try:
    df = pd.read_csv(URL_CLIENTES)
    
    st.success("Planilha 'Clientes' carregada com sucesso!")
    
    # Isso vai mostrar a lista de colunas na sua tela
    st.write("### Nomes das colunas encontrados:")
    st.write(df.columns.tolist())
    
    st.write("### Primeiras linhas da planilha (para conferência):")
    st.write(df.head())

except Exception as e:
    st.error(f"Erro ao conectar: {e}")

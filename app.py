import streamlit as st
import pandas as pd
import re

st.title("TMS FRANCAL - ACESSO EM TEMPO REAL")

# URL da sua planilha publicada
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-k3doFN8BGK5YL9su9avmaFLgV97SbE3erJdh0YDJxACO3nNrYX6XTO0a7rhRtUN9xcdeIsLWurAr/pub?output=csv"

try:
    # Lê os dados direto do Google Sheets
    df = pd.read_csv(SHEET_URL)
    
    # Limpa os nomes das colunas (remove \n e espaços)
    df.columns = df.columns.str.replace('\n', '').str.strip()
    
    st.success("Conectado ao Google Sheets com sucesso!")
    
    cnpj = st.text_input("Digite o CNPJ/CPF do cliente:")
    
    if st.button("BUSCAR"):
        # Função para limpar números
        def limpar_numero(valor):
            return re.sub(r'\D', '', str(valor))
        
        # Limpa a coluna CPF/CNPJ da planilha
        coluna_busca = "CPF/CNPJ"
        df['limpo'] = df[coluna_busca].apply(limpar_numero)
        
        cnpj_limpo = limpar_numero(cnpj)
        
        # Filtra os dados
        resultado = df[df['limpo'] == cnpj_limpo]
        
        if not resultado.empty:
            st.write("### Dados encontrados:")
            st.write(resultado.iloc[0])
        else:
            st.error("CNPJ/CPF não encontrado na base.")
            
except Exception as e:
    st.error(f"Erro ao conectar na planilha: {e}")

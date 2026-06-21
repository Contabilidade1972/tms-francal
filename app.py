import streamlit as st
import pandas as pd
import re

st.title("TMS FRANCAL - BUSCA DE CLIENTES")

# Link específico da aba "Clientes"
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-k3doFN8BGK5YL9su9avmaFLgV97SbE3erJdh0YDJxACO3nNrYX6XTO0a7rhRtUN9xcdeIsLWurAr/pub?gid=1821072074&single=true&output=csv"

try:
    # Lê a aba Clientes
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.replace('\n', '').str.strip()
    
    st.success("Base de Clientes carregada!")
    
    termo = st.text_input("Digite o CNPJ/CPF do cliente:")
    
    if st.button("BUSCAR"):
        def limpar(val): return re.sub(r'\D', '', str(val))
        
        # Garante que a coluna de busca exista
        if "CPF/CNPJ" in df.columns:
            df['limpo'] = df['CPF/CNPJ'].apply(limpar)
            resultado = df[df['limpo'] == limpar(termo)]
            
            if not resultado.empty:
                st.write("### Dados encontrados:")
                st.write(resultado.iloc[0])
            else:
                st.error("CNPJ/CPF não encontrado na base de Clientes.")
        else:
            st.error("Coluna 'CPF/CNPJ' não encontrada na aba. Verifique o cabeçalho.")
            
except Exception as e:
    st.error(f"Erro ao conectar: {e}")

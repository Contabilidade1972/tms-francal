import streamlit as st
import pandas as pd
import re

st.title("TMS FRANCAL - BUSCA")

uploaded_file = st.file_uploader("Selecione o arquivo base_Geral.xlsx", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Lê a primeira aba
        df = pd.read_excel(uploaded_file, sheet_name=0, engine='openpyxl')
        st.success("Planilha carregada!")
        
        cnpj = st.text_input("Digite o CNPJ/CPF do cliente:")
        
        if st.button("BUSCAR"):
            # Função para extrair apenas números de uma string
            def limpar_numero(valor):
                return re.sub(r'\D', '', str(valor))
            
            # Limpa a coluna da planilha (assumindo a primeira coluna)
            coluna_busca = df.columns[0]
            df['limpo'] = df[coluna_busca].apply(limpar_numero)
            
            # Limpa o que você digitou
            cnpj_limpo = limpar_numero(cnpj)
            
            # Filtra
            resultado = df[df['limpo'] == cnpj_limpo]
            
            if not resultado.empty:
                st.write("### Dados encontrados:")
                st.write(resultado.iloc[0])
            else:
                st.error("CNPJ/CPF não encontrado na base.")
                st.info(f"O sistema buscou pelo número puro: {cnpj_limpo}")
                
    except Exception as e:
        st.error(f"Erro ao processar: {e}")

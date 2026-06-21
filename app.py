import streamlit as st
import pandas as pd
import re

st.title("TMS FRANCAL - BUSCA DE CLIENTES")

uploaded_file = st.file_uploader("Selecione o arquivo base_Geral.xlsx", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Lê o arquivo
        df = pd.read_excel(uploaded_file, sheet_name=0, engine='openpyxl')
        
        # Limpa os nomes das colunas: remove quebras de linha (\n) e espaços extras
        df.columns = df.columns.str.replace('\n', '').str.strip()
        
        st.success("Planilha carregada e colunas organizadas!")
        
        # Campo de busca
        cnpj = st.text_input("Digite o CNPJ/CPF do cliente:")
        
        if st.button("BUSCAR"):
            # Função de limpeza de números
            def limpar_numero(valor):
                return re.sub(r'\D', '', str(valor))
            
            # Limpa a coluna CPF/CNPJ
            coluna_busca = "CPF/CNPJ"
            df['limpo'] = df[coluna_busca].apply(limpar_numero)
            
            cnpj_limpo = limpar_numero(cnpj)
            
            # Filtra
            resultado = df[df['limpo'] == cnpj_limpo]
            
            if not resultado.empty:
                st.write("### Dados encontrados:")
                st.write(resultado.iloc[0])
            else:
                st.error("CNPJ/CPF não encontrado na base.")
                
    except Exception as e:
        st.error(f"Erro ao processar: {e}")

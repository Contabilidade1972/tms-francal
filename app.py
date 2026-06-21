import streamlit as st
import pandas as pd
import os

st.title("TMS FRANCAL - GESTÃO DE DADOS")

# Define o caminho do arquivo
FILE_NAME = "base_Geral.xlsx"

if os.path.exists(FILE_NAME):
    try:
        # Carrega a aba Clientes
        df = pd.read_excel(FILE_NAME, sheet_name="Clientes")
        st.success("Base de dados carregada com sucesso!")
        
        cnpj = st.text_input("Digite o CNPJ/CPF:")
        if st.button("BUSCAR"):
            # Converte a coluna para string para garantir a busca
            df['CPF/CNPJ'] = df['CPF/CNPJ'].astype(str).str.strip()
            resultado = df[df['CPF/CNPJ'] == cnpj.strip()]
            
            if not resultado.empty:
                st.write("### Dados encontrados:")
                st.write(resultado.iloc[0])
            else:
                st.error("CNPJ/CPF não encontrado na base.")
    except Exception as e:
        st.error(f"Erro ao ler a planilha: {e}")
else:
    st.error(f"O arquivo {FILE_NAME} não foi encontrado na pasta do repositório.")
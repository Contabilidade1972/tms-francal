import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="TMS FRANCAL", layout="wide")

st.title("TMS FRANCAL - BUSCA DE DADOS")

# Nome do arquivo e da aba confirmados
FILE_NAME = "base_Geral.xlsx"
SHEET_NAME = "BASE DE CLIENTES"

try:
    # Carregamento da planilha
    df = pd.read_excel(FILE_NAME, sheet_name=SHEET_NAME, engine='openpyxl')
    st.success("Planilha carregada com sucesso!")
    
    # Campo de busca
    cnpj = st.text_input("Digite o CNPJ/CPF do cliente:")
    
    if st.button("BUSCAR"):
        # Limpeza e conversão para busca precisa
        df['CPF/CNPJ'] = df['CPF/CNPJ'].astype(str).str.strip()
        
        # Filtro
        resultado = df[df['CPF/CNPJ'] == cnpj.strip()]
        
        if not resultado.empty:
            st.write("### Dados encontrados:")
            st.write(resultado.iloc[0])
        else:
            st.error("CNPJ/CPF não encontrado na base.")
            
except Exception as e:
    st.error(f"Erro ao carregar o sistema: {e}")
    st.info("Verifique se o arquivo 'base_Geral.xlsx' está na pasta e se a aba 'BASE DE CLIENTES' existe.")

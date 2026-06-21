import streamlit as st
import pandas as pd

st.title("TMS FRANCAL - BUSCA")

# Componente para subir o arquivo
uploaded_file = st.file_uploader("Selecione o arquivo base_Geral.xlsx", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Lê a primeira aba disponível, não importa o nome
        df = pd.read_excel(uploaded_file, sheet_name=0, engine='openpyxl')
        st.success("Planilha carregada com sucesso!")
        
        # Exibe as colunas encontradas para você confirmar se são as corretas
        st.write("Colunas encontradas:", df.columns.tolist())
        
        cnpj = st.text_input("Digite o CNPJ/CPF do cliente:")
        
        if st.button("BUSCAR"):
            # Converte para string e remove espaços para busca
            coluna_busca = df.columns[0] # Assume que a primeira coluna é a do CPF/CNPJ
            df[coluna_busca] = df[coluna_busca].astype(str).str.strip()
            
            resultado = df[df[coluna_busca] == cnpj.strip()]
            
            if not resultado.empty:
                st.write("### Dados encontrados:")
                st.write(resultado.iloc[0])
            else:
                st.error("CNPJ/CPF não encontrado na base.")
                
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        st.info("Verifique se o arquivo está no formato correto.")
else:
    st.info("Por favor, faça o upload do arquivo base_Geral.xlsx abaixo.")

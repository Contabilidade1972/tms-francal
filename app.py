import streamlit as st
import pandas as pd

st.title("TMS FRANCAL - BUSCA")

# FORMA SEGURA: O próprio usuário faz o upload do arquivo na hora
uploaded_file = st.file_uploader("Selecione o arquivo base_Geral.xlsx", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Lê o arquivo que você subiu agora
        df = pd.read_excel(uploaded_file, sheet_name="BASE DE CLIENTES", engine='openpyxl')
        st.success("Planilha carregada!")
        
        cnpj = st.text_input("Digite o CNPJ:")
        if st.button("BUSCAR"):
            df['CPF/CNPJ'] = df['CPF/CNPJ'].astype(str).str.strip()
            resultado = df[df['CPF/CNPJ'] == cnpj.strip()]
            
            if not resultado.empty:
                st.write(resultado.iloc[0])
            else:
                st.error("CNPJ não encontrado.")
    except Exception as e:
        st.error(f"Erro na leitura: {e}")
else:
    st.info("Por favor, selecione o arquivo base_Geral.xlsx acima.")

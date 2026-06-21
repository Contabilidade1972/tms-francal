import streamlit as st
import pandas as pd
import re

st.title("TMS FRANCAL - GESTÃO DE CLIENTES")

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-k3doFN8BGK5YL9su9avmaFLgV97SbE3erJdh0YDJxACO3nNrYX6XTO0a7rhRtUN9xcdeIsLWurAr/pub?output=csv"

try:
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.replace('\n', '').str.strip()
    
    tab1, tab2 = st.tabs(["Buscar Cliente/Nota", "Cadastrar Novo"])

    with tab1:
        tipo_busca = st.radio("Buscar por:", ["CNPJ/CPF", "Nota Fiscal"])
        termo = st.text_input("Digite o número para busca:")
        
        if st.button("BUSCAR"):
            def limpar(val): return re.sub(r'\D', '', str(val))
            
            # Se for CNPJ, busca na coluna CPF/CNPJ. Se for Nota, busca na coluna 'Nota Fiscal' (ajuste o nome se necessário)
            coluna = "CPF/CNPJ" if tipo_busca == "CNPJ/CPF" else "Nota Fiscal"
            
            df['limpo'] = df[coluna].apply(limpar)
            resultado = df[df['limpo'] == limpar(termo)]
            
            if not resultado.empty:
                st.write("### Dados encontrados:")
                st.write(resultado.iloc[0])
            else:
                st.error("Não encontrado na base.")
                st.session_state['cadastrar_cnpj'] = termo # Passa o termo para a aba de cadastro

    with tab2:
        st.header("Cadastro de Novo Cliente")
        with st.form("form_cadastro"):
            nome = st.text_input("Nome/Razão Social")
            cnpj_novo = st.text_input("CNPJ/CPF", value=st.session_state.get('cadastrar_cnpj', ''))
            submit = st.form_submit_button("Cadastrar")
            
            if submit:
                st.info("Para salvar automaticamente no Google Sheets, precisaremos configurar a escrita. Por enquanto, os dados seriam enviados para um e-mail ou log.")
                st.write(f"Dados prontos para salvar: {nome}, {cnpj_novo}")

except Exception as e:
    st.error(f"Erro: {e}")

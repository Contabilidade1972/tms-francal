import streamlit as st
import pandas as pd
import re

st.title("TMS FRANCAL - GESTÃO DE OPERAÇÕES")

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-k3doFN8BGK5YL9su9avmaFLgV97SbE3erJdh0YDJxACO3nNrYX6XTO0a7rhRtUN9xcdeIsLWurAr/pub?output=csv"

# Função de limpeza
def limpar(val): return re.sub(r'\D', '', str(val))

try:
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.replace('\n', '').str.strip()
    
    tab1, tab2, tab3 = st.tabs(["Buscar Cliente", "Gerar Minuta de Despacho", "Cadastrar Novo"])

    with tab1:
        termo = st.text_input("Buscar cliente por CNPJ/CPF:")
        if st.button("BUSCAR CLIENTE"):
            df['limpo'] = df['CPF/CNPJ'].apply(limpar)
            resultado = df[df['limpo'] == limpar(termo)]
            if not resultado.empty:
                st.write(resultado.iloc[0])
            else:
                st.error("Cliente não encontrado.")

    with tab2:
        st.header("Gerar Minuta de Despacho")
        nf = st.text_input("Número da Nota Fiscal (ou cole o conteúdo do XML):")
        cnpj_cliente = st.text_input("CNPJ do Cliente para Despacho:")
        
        if st.button("GERAR MINUTA"):
            # Aqui faremos a busca do cliente e combinaremos com o número da NF
            df['limpo'] = df['CPF/CNPJ'].apply(limpar)
            cliente = df[df['limpo'] == limpar(cnpj_cliente)]
            
            if not cliente.empty:
                st.success(f"Dados prontos para Minuta NF nº {nf}")
                st.write(f"Cliente: {cliente.iloc[0]['Nome']}")
                # A partir daqui, você pode gerar um PDF ou salvar no Sheets
            else:
                st.error("CNPJ do cliente não encontrado para gerar a minuta.")

    with tab3:
        st.write("Funcionalidade de cadastro em desenvolvimento.")

except Exception as e:
    st.error(f"Erro no sistema: {e}")

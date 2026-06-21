import streamlit as st
import pandas as pd
import re

st.title("TMS FRANCAL - GESTÃO DE OPERAÇÕES")

# URL direta da planilha (usaremos para ler a estrutura)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg/edit#gid=0"

# Função de limpeza
def limpar(val): return re.sub(r'\D', '', str(val))

try:
    # Para ler abas específicas, usaremos o link de exportação do Google (CSV da aba Clientes)
    # Substitua este link pelo link de publicação CSV ESPECÍFICO da aba "Clientes"
    URL_CLIENTES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-k3doFN8BGK5YL9su9avmaFLgV97SbE3erJdh0YDJxACO3nNrYX6XTO0a7rhRtUN9xcdeIsLWurAr/pub?gid=1756592231&single=true&output=csv"
    
    df = pd.read_csv(URL_CLIENTES)
    df.columns = df.columns.str.replace('\n', '').str.strip()
    
    tab1, tab2, tab3 = st.tabs(["Buscar Cliente", "Gerar Minuta", "Cadastrar"])

    with tab1:
        termo = st.text_input("Digite o CNPJ/CPF para busca:")
        if st.button("BUSCAR"):
            df['limpo'] = df['CPF/CNPJ'].apply(limpar)
            resultado = df[df['limpo'] == limpar(termo)]
            
            if not resultado.empty:
                st.write("### Dados do Cliente:")
                st.write(resultado.iloc[0])
            else:
                st.error("Cliente não encontrado na aba Clientes.")

except Exception as e:
    st.error(f"Erro ao conectar na aba Clientes: {e}")

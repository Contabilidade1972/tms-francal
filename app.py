import streamlit as st
import pandas as pd

st.title("TMS FRANCAL - ACESSO EM TEMPO REAL")

# URL da sua planilha publicada na web
# No Google Sheets: Arquivo > Compartilhar > Publicar na Web > CSV
SHEET_URL = "COLOQUE_AQUI_O_LINK_DO_CSV_DA_SUA_PLANILHA"

try:
    # O Streamlit lê o CSV direto do Google Sheets
    df = pd.read_csv(SHEET_URL)
    
    # Limpeza dos nomes das colunas
    df.columns = df.columns.str.replace('\n', '').str.strip()
    
    st.success("Conectado ao Google Sheets com sucesso!")
    
    cnpj = st.text_input("Digite o CNPJ/CPF:")
    
    if st.button("BUSCAR"):
        # Lógica de limpeza e busca
        df['limpo'] = df['CPF/CNPJ'].astype(str).str.replace(r'\D', '', regex=True)
        cnpj_limpo = cnpj.strip().replace('.', '').replace('-', '').replace('/', '')
        
        resultado = df[df['limpo'] == cnpj_limpo]
        
        if not resultado.empty:
            st.write(resultado.iloc[0])
        else:
            st.error("Cliente não encontrado.")
            
except Exception as e:
    st.error(f"Erro ao conectar na planilha: {e}")

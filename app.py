import streamlit as st
import pandas as pd
from pathlib import Path

st.title("TMS FRANCAL - BUSCA")

# Localiza o arquivo na mesma pasta onde o app.py está, sem depender de caminhos
caminho_base = Path(__file__).parent / "base_Geral.xlsx"

if not caminho_base.exists():
    st.error(f"Erro: Arquivo não encontrado em {caminho_base.absolute()}")
    st.write("Arquivos encontrados nesta pasta:", [f.name for f in Path(__file__).parent.iterdir()])
else:
    try:
        df = pd.read_excel(caminho_base, sheet_name="BASE DE CLIENTES", engine='openpyxl')
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

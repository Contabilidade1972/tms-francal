import streamlit as st
import pandas as pd
import re

st.title("TMS FRANCAL - GESTÃO DE OPERAÇÕES")

# Seu link validado para a aba "Clientes"
URL_CLIENTES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-k3doFN8BGK5YL9su9avmaFLgV97SbE3erJdh0YDJxACO3nNrYX6XTO0a7rhRtUN9xcdeIsLWurAr/pub?gid=1821072074&single=true&output=csv"

try:
    # Carrega os dados
    df = pd.read_csv(URL_CLIENTES)
    
    # Limpeza técnica pesada: remove espaços e quebras de linha dos nomes das colunas
    df.columns = [col.strip().replace('\n', '') for col in df.columns]
    
    # Garante que a coluna de busca exista
    coluna_cpf_cnpj = "CPF/CNPJ"
    if coluna_cpf_cnpj not in df.columns:
        st.error(f"Erro: A coluna '{coluna_cpf_cnpj}' não foi encontrada. Colunas atuais: {df.columns.tolist()}")
    else:
        # Interface
        tab1, tab2, tab3 = st.tabs(["Buscar Cliente", "Gerar Minuta", "Cadastrar Novo"])
        
        with tab1:
            termo = st.text_input("Digite o CNPJ/CPF para busca:")
            if st.button("BUSCAR CLIENTE"):
                # Função de limpeza
                def limpar(val): return re.sub(r'\D', '', str(val))
                
                df['limpo'] = df[coluna_cpf_cnpj].apply(limpar)
                resultado = df[df['limpo'] == limpar(termo)]
                
                if not resultado.empty:
                    st.write("### Dados encontrados:")
                    st.write(resultado.iloc[0])
                else:
                    st.error("Cliente não encontrado.")

except Exception as e:
    st.error(f"Erro na conexão: {e}")

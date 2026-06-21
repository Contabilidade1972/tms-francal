import streamlit as st
import pandas as pd
import re

st.title("TMS FRANCAL - GESTÃO DE OPERAÇÕES")

# Links da planilha (Aba Clientes)
URL_CLIENTES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-k3doFN8BGK5YL9su9avmaFLgV97SbE3erJdh0YDJxACO3nNrYX6XTO0a7rhRtUN9xcdeIsLWurAr/pub?gid=1821072074&single=true&output=csv"

try:
    df = pd.read_csv(URL_CLIENTES)
    df.columns = [col.strip().replace('\n', '') for col in df.columns]

    tab1, tab2, tab3 = st.tabs(["Buscar Cliente", "Gerar Minuta", "Cadastrar Novo"])

    # Aba 1: Busca (Já validada)
    with tab1:
        termo = st.text_input("Digite o CNPJ/CPF para busca:")
        if st.button("BUSCAR CLIENTE"):
            def limpar(val): return re.sub(r'\D', '', str(val))
            df['limpo'] = df['CPF/CNPJ'].apply(limpar)
            resultado = df[df['limpo'] == limpar(termo)]
            if not resultado.empty:
                st.write(resultado.iloc[0])
            else:
                st.error("Cliente não encontrado.")

    # Aba 2: O novo formulário de Minuta
    with tab2:
        st.header("Preencher Minuta de Despacho")
        cnpj_minuta = st.text_input("CNPJ do Cliente:")
        
        if st.button("PUXAR DADOS"):
            def limpar(val): return re.sub(r'\D', '', str(val))
            df['limpo'] = df['CPF/CNPJ'].apply(limpar)
            cliente = df[df['limpo'] == limpar(cnpj_minuta)]
            
            if not cliente.empty:
                st.session_state['cliente_minuta'] = cliente.iloc[0]
                st.success("Dados do cliente carregados!")
            else:
                st.error("CNPJ não encontrado.")

        if 'cliente_minuta' in st.session_state:
            c = st.session_state['cliente_minuta']
            st.write(f"**Cliente:** {c['Nome']}")
            st.write(f"**Endereço:** {c['Logradouro']}, {c['Número']} - {c['Município']}")
            
            # Campos da NF
            nf = st.text_input("Número da Nota Fiscal")
            peso = st.number_input("Peso (kg)")
            volume = st.number_input("Volume")
            
            if st.button("GERAR MINUTA"):
                st.info(f"Dados prontos para exportação: NF {nf}, Cliente {c['Nome']}, Peso {peso}kg.")
                # Aqui adicionaremos em breve a lógica de salvar no registro e criar PDF

except Exception as e:
    st.error(f"Erro no sistema: {e}")

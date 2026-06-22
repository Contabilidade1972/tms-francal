import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
import json

st.title("TMS FRANCAL - GESTÃO DE OPERAÇÕES")

# Função para conectar ao Google Sheets via Secrets
def conectar_sheets():
    # Carrega as secrets configuradas no Streamlit Cloud
    credentials = dict(st.secrets["gspread"])
    
    # Cria um arquivo temporário de credenciais a partir das secrets
    with open("service-account.json", "w") as f:
        json.dump(credentials, f)
        
    gc = gspread.service_account(filename="service-account.json")
    # Abre a planilha pelo nome ou ID (certifique-se que o e-mail do bot foi compartilhado)
    sh = gc.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg") 
    return sh.worksheet("REGISTRO_OPERACIONAL")

tab1, tab2, tab3 = st.tabs(["Ordem de Coleta", "Minuta de Despacho", "Fatura"])

with tab1:
    st.header("1. Ordem de Coleta (Solicitação)")
    
    col1, col2 = st.columns(2)
    with col1:
        cnpj_remetente = st.text_input("CNPJ Remetente")
        cnpj_destinatario = st.text_input("CNPJ Destinatário")
    with col2:
        nf = st.text_input("Número da Nota Fiscal")
        data_coleta = st.date_input("Data da Coleta")
        
    col3, col4, col5 = st.columns(3)
    with col3:
        peso_bruto = st.number_input("Peso Bruto (kg)")
    with col4:
        volume = st.number_input("Volume")
    with col5:
        valor_mercadoria = st.number_input("Valor da Mercadoria (R$)")
        
    observacoes = st.text_area("Observações")
    
    if st.button("SALVAR ORDEM DE COLETA"):
        try:
            ws = conectar_sheets()
            nova_linha = [
                str(datetime.now().timestamp()), # ID_OPERACAO
                datetime.now().strftime("%d/%m/%Y %H:%M"), # DATA_GERACAO
                str(data_coleta),
                cnpj_remetente,
                cnpj_destinatario,
                nf,
                str(peso_bruto),
                str(volume),
                str(valor_mercadoria),
                observacoes,
                "PENDENTE" # STATUS
            ]
            ws.append_row(nova_linha)
            st.success("Ordem de Coleta gravada com sucesso no Google Sheets!")
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")

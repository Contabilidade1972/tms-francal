import streamlit as st
import gspread
import json
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="TMS FRANCAL", layout="centered")

st.title("TMS FRANCAL - GESTÃO DE OPERAÇÕES")

# Função de Conexão com Google Sheets
def conectar_sheets():
    # Lê a configuração de dentro do grupo [gspread] no Secrets
    secrets_data = json.loads(st.secrets["gspread"]["json_content"])
    gc = gspread.service_account_from_dict(secrets_data)
    # Abre a planilha pelo ID
    sh = gc.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg") 
    return sh.worksheet("REGISTRO_OPERACIONAL")

# Formulário
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
        peso_bruto = st.number_input("Peso Bruto (kg)", min_value=0.0)
    with col4:
        volume = st.number_input("Volume", min_value=0)
    with col5:
        valor_mercadoria = st.number_input("Valor da Mercadoria (R$)", min_value=0.0)
        
    observacoes = st.text_area("Observações")
    
    if st.button("SALVAR ORDEM DE COLETA"):
        try:
            ws = conectar_sheets()
            nova_linha = [
                str(datetime.now().timestamp()), 
                datetime.now().strftime("%d/%m/%Y %H:%M"),
                str(data_coleta),
                cnpj_remetente,
                cnpj_destinatario,
                nf,
                str(peso_bruto),
                str(volume),
                str(valor_mercadoria),
                observacoes,
                "PENDENTE"
            ]
            ws.append_row(nova_linha)
            st.success("Ordem de Coleta gravada com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")

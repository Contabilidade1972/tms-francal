import streamlit as st
import gspread
import json

st.title("TMS FRANCAL - ACESSO")

def conectar():
    # Carrega a string JSON do Secrets
    json_str = st.secrets["GCP_JSON"]
    # Converte para dicionário Python
    creds_dict = json.loads(json_str)
    
    # Conecta ao Google Sheets
    gc = gspread.service_account_from_dict(creds_dict)
    return gc.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg").worksheet("REGISTRO_OPERACIONAL")

if st.button("INICIAR CONEXÃO"):
    try:
        ws = conectar()
        st.success("Conectado com sucesso!")
    except Exception as e:
        st.error(f"Erro de conexão: {e}")

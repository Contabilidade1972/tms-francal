import streamlit as st
import gspread
from datetime import datetime

st.set_page_config(page_title="TMS FRANCAL")

def conectar_sheets():
    # Carrega cada valor individualmente do Secrets
    creds = {
        "type": st.secrets["TYPE"],
        "project_id": st.secrets["PROJECT_ID"],
        "private_key_id": st.secrets["PRIVATE_KEY_ID"],
        "private_key": st.secrets["PRIVATE_KEY"],
        "client_email": st.secrets["CLIENT_EMAIL"],
        "token_uri": st.secrets["TOKEN_URI"]
    }
    gc = gspread.service_account_from_dict(creds)
    sh = gc.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg") 
    return sh.worksheet("REGISTRO_OPERACIONAL")

st.title("TMS FRANCAL")

if st.button("TESTAR CONEXÃO"):
    try:
        ws = conectar_sheets()
        st.success("Conexão OK!")
    except Exception as e:
        st.error(f"Erro: {e}")

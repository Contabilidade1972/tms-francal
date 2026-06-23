import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials

# Força a leitura do segredo como um JSON puro, ignorando interpretação PEM
def get_sheet():
    # Carrega a string JSON do secrets
    json_str = st.secrets["gcp_json"]
    # Converte string para dicionário
    info = json.loads(json_str)
    
    # Cria as credenciais a partir do dicionário (não do arquivo PEM)
    creds = Credentials.from_service_account_info(info)
    scoped_creds = creds.with_scopes([
        'https://spreadsheets.google.com/feeds', 
        'https://www.googleapis.com/auth/drive'
    ])
    
    client = gspread.authorize(scoped_creds)
    return client.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg").worksheet("REGISTRO_OPERACIONAL")

# O resto do seu código...

import streamlit as st
import gspread
import json
from datetime import datetime

st.set_page_config(page_title="TMS FRANCAL")
st.title("TMS FRANCAL - GESTÃO DE OPERAÇÕES")

def conectar_sheets():
    # Usando o formato de variáveis individuais que salvamos no Secrets
    try:
        creds = {
            "type": st.secrets["TYPE"],
            "project_id": st.secrets["PROJECT_ID"],
            "private_key_id": st.secrets["PRIVATE_KEY_ID"],
            "private_key": st.secrets["PRIVATE_KEY"].replace('\\n', '\n'),
            "client_email": st.secrets["CLIENT_EMAIL"],
            "token_uri": st.secrets["TOKEN_URI"]
        }
        gc = gspread.service_account_from_dict(creds)
        sh = gc.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg") 
        return sh.worksheet("REGISTRO_OPERACIONAL")
    except Exception as e:
        return f"Erro de Conexão: {e}"

# Formulário (sem tentar conectar no carregamento)
cnpj_remetente = st.text_input("CNPJ Remetente")
cnpj_destinatario = st.text_input("CNPJ Destinatário")
nf = st.text_input("Número da Nota Fiscal")

if st.button("SALVAR DADOS"):
    ws = conectar_sheets()
    if isinstance(ws, str):
        st.error(ws) # Se deu erro na conexão, mostra aqui
    else:
        st.success("Conectado! (Dados seriam salvos aqui)")

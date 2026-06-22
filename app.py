import streamlit as st
import gspread
import json
from datetime import datetime

# Conecta usando a variável que colocamos no Secrets
def conectar_sheets():
    # Isso carrega a chave diretamente da memória, sem precisar de arquivo
    creds_dict = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
    gc = gspread.service_account_from_dict(creds_dict)
    sh = gc.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg") 
    return sh.worksheet("REGISTRO_OPERACIONAL")

st.title("TMS FRANCAL - GESTÃO DE OPERAÇÕES")

# Seu formulário de coleta...
cnpj_remetente = st.text_input("CNPJ Remetente")
# ... resto do código ...

if st.button("SALVAR ORDEM DE COLETA"):
    try:
        ws = conectar_sheets()
        # ... salvar ...
        st.success("Dados gravados!")
    except Exception as e:
        st.error(f"Erro: {e}")

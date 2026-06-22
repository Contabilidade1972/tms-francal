import streamlit as st
import gspread
import json

def conectar():
    # Carrega o JSON
    json_str = st.secrets["GCP_JSON"]
    creds_dict = json.loads(json_str)
    
    # FORÇA a quebra de linha correta na chave privada
    creds_dict["private_key"] = creds_dict["private_key"].replace('\\n', '\n')
    
    gc = gspread.service_account_from_dict(creds_dict)
    return gc.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg").worksheet("REGISTRO_OPERACIONAL")

st.title("TMS FRANCAL - ACESSO")
if st.button("CONECTAR"):
    try:
        ws = conectar()
        st.success("Conectado!")
    except Exception as e:
        st.error(f"Erro: {e}")

import streamlit as st
import requests

st.set_page_config(page_title="TMS FRANCAL", layout="centered")
st.title("TMS FRANCAL - ORDEM DE COLETA")

# Usamos 'session_state' para limpar os campos após salvar
if 'form_key' not in st.session_state:
    st.session_state.form_key = 0

def limpar_campos():
    st.session_state.form_key += 1

with st.form(key=f"coleta_form_{st.session_state.form_key}", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        cnpj_rem = st.text_input("CNPJ Remetente")
        cnpj_dest = st.text_input("CNPJ Destinatário")
        peso = st.number_input("Peso Bruto (kg)", min_value=0.0)
    with col2:
        nf = st.text_input("Número da NF")
        volume = st.number_input("Volumes", min_value=0)
        valor = st.number_input("Valor da Mercadoria (R$)", min_value=0.0)
    
    obs = st.text_area("Observações")
    
    submit_button = st.form_submit_button("SALVAR ORDEM DE COLETA")

if submit_button:
    url = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec"
    payload = {
        "cnpj_remetente": cnpj_rem, "cnpj_destinatario": cnpj_dest,
        "nf": nf, "peso": peso, "volume": volume,
        "valor": valor, "observacoes": obs
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            st.success("Ordem de Coleta enviada com sucesso!")
        else:
            st.error(f"Erro no envio: {response.status_code}")
    except Exception as e:
        st.error(f"Erro de conexão: {e}")

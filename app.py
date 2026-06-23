import streamlit as st
import requests

URL = "SUA_URL_AQUI" # Certifique-se que esta URL é a da Nova Implantação

st.set_page_config(layout="wide")
st.title("Cadastro de Motoristas")

if 'd' not in st.session_state: st.session_state.d = [""] * 23

cpf_busca = st.text_input("Buscar por CPF")
if st.button("Buscar Motorista"):
    try:
        r = requests.get(f"{URL}?cpf={cpf_busca}", timeout=15)
        if r.status_code == 200:
            st.session_state.d = r.json()
            st.rerun()
        else:
            st.error(f"Erro do Servidor: {r.status_code}")
    except Exception as e:
        st.error(f"Erro de conexão: {e}")

d = st.session_state.d

with st.form("motorista_form"):
    # (Mantenha aqui os campos conforme o código anterior)
    # ...
    
    if st.form_submit_button("SALVAR / ATUALIZAR"):
        payload = {
            "nome": nome, "telefone": tel, "cpf": cpf, # ... siga o mapa do rowData do Apps Script
        }
        # ... requests.post ...

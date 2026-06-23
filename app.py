import streamlit as st
import requests

URL = "SUA_NOVA_URL_AQUI" # Cole a nova URL de implantação aqui

st.set_page_config(layout="wide")
st.sidebar.title("TMS FRANCAL")
st.sidebar.selectbox("Módulo", ["Cadastro: Motoristas"])

st.title("Cadastro de Motoristas")
if 'd' not in st.session_state: st.session_state.d = [""] * 23

cpf_busca = st.text_input("CPF")
if st.button("Buscar"):
    try:
        st.session_state.d = requests.get(f"{URL}?cpf={cpf_busca}", timeout=10).json()
        st.rerun()
    except: st.error("Erro na comunicação com a base.")

d = st.session_state.d

with st.form("form_motorista"):
    c1, c2, c3 = st.columns(3)
    nome = c1.text_input("Nome", value=d[0] if isinstance(d, list) else "")
    tel = c2.text_input("Telefone", value=d[1] if isinstance(d, list) else "")
    nasc = c3.text_input("Nascimento", value=d[17] if isinstance(d, list) else "")
    
    # ... adicione aqui todos os outros campos seguindo o índice d[2] a d[22] ...
    
    if st.form_submit_button("SALVAR"):
        payload = {"nome": nome, "tel": tel, "cpf": d[10] if isinstance(d, list) else cpf_busca, /* inclua todos os campos aqui */}
        requests.post(URL, json=payload)
        st.success("Salvo!")

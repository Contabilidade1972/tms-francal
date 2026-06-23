import streamlit as st
import requests

# URL deve ser sua URL de implantação mais recente
URL = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec"

st.set_page_config(layout="wide")
if 'd' not in st.session_state: st.session_state.d = [""] * 23

st.title("Cadastro de Motoristas")
cpf_in = st.text_input("CPF (Somente números)")
if st.button("Buscar"):
    try:
        resp = requests.get(f"{URL}?cpf={cpf_in}", timeout=10).json()
        st.session_state.d = resp if isinstance(resp, list) else [""] * 23
        st.rerun()
    except Exception as e: st.error(f"Erro: {e}")

d = st.session_state.d
with st.form("motorista_form"):
    c1, c2, c3 = st.columns(3)
    nome = c1.text_input("Nome", value=d[0])
    tel = c2.text_input("Telefone", value=d[1])
    nasc = c3.text_input("Data Nascimento", value=d[17])
    
    # ... Continue adicionando os inputs seguindo o índice d[0] até d[22] ...
    
    if st.form_submit_button("Salvar / Atualizar"):
        payload = {"nome": nome, "telefone": tel, "cpf": d[10] or cpf_in, ...}
        requests.post(URL, json=payload)
        st.success("Salvo!")

import streamlit as st
import requests
import re

st.set_page_config(layout="wide")

def fmt(v, t):
    v = re.sub(r'\D', '', str(v))
    if t == 'cpf': return f"{v[:3]}.{v[3:6]}.{v[6:9]}-{v[9:]}" if len(v)==11 else v
    if t == 'cep': return f"{v[:5]}-{v[5:]}" if len(v)==8 else v
    return v

if 'd' not in st.session_state: st.session_state.d = [""] * 23

st.title("Cadastro de Motoristas")
col_b, col_btn = st.columns([4, 1])
cpf_in = col_b.text_input("Buscar CPF")
if col_btn.button("Buscar"):
    url = f"https://script.google.com/macros/s/SUA_URL_AQUI/exec?cpf={re.sub(r'\D', '', cpf_in)}"
    st.session_state.d = requests.get(url).json() if "status" not in requests.get(url).json() else [""] * 23
    st.rerun()

d = st.session_state.d
with st.form("motorista_form"):
    c1, c2 = st.columns(2)
    nome = c1.text_input("Nome", value=d[0])
    tel = c2.text_input("Telefone", value=d[1])
    # ... adicione os campos restantes mapeando os índices de d[0] a d[22] ...
    
    if st.form_submit_button("Salvar / Atualizar"):
        payload = {"nome": nome, "telefone": tel, "cpf": d[10], ...} # Adicione todos os campos
        requests.post("https://script.google.com/macros/s/SUA_URL_AQUI/exec", json=payload)
        st.success("Dados salvos!")

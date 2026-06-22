import streamlit as st
import requests
import re

st.set_page_config(layout="wide")

def aplicar_mascara(val, tipo):
    v = re.sub(r'\D', '', str(val))
    if tipo == 'cpf': return f"{v[:3]}.{v[3:6]}.{v[6:9]}-{v[9:]}" if len(v) == 11 else v
    if tipo == 'cep': return f"{v[:5]}-{v[5:]}" if len(v) == 8 else v
    if tipo == 'tel': return f"({v[:2]}){v[2:6]}-{v[6:]}" if len(v) == 10 else v
    return v

if 'data' not in st.session_state: st.session_state.data = {}

st.title("Cadastro de Motoristas")
cpf_in = st.text_input("CPF (Somente números)")
if st.button("Buscar"):
    url = f"https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec?cpf={cpf_in}"
    try:
        st.session_state.data = requests.get(url, timeout=10).json()
    except: st.error("Erro na comunicação.")

d = st.session_state.data

with st.form("form_motorista"):
    st.subheader("Dados Pessoais")
    c1, c2, c3 = st.columns(3)
    nome = c1.text_input("Nome", value=d.get('Nome', ''))
    tel = c2.text_input("Telefone", value=aplicar_mascara(d.get('Telefone', ''), 'tel'))
    nasc = c3.date_input("Data de Nascimento", value=None)
    
    st.subheader("Endereço")
    c1, c2 = st.columns(2)
    cep = c1.text_input("CEP", value=aplicar_mascara(d.get('CEP', ''), 'cep'))
    uf = c2.selectbox("UF", ["MG", "SP", "RJ"], index=0)
    mun = c1.text_input("Município")
    
    st.subheader("Habilitação e Banco")
    c1, c2 = st.columns(2)
    cnh = c1.text_input("CNH", value=d.get('CNH', ''))
    banco = c2.text_input("Banco", value=d.get('Banco', ''))
    obs = st.text_area("Observações", value=d.get('Observações', ''))

    if st.form_submit_button("Salvar"):
        st.success("Dados enviados para processamento!")

import streamlit as st
import requests
import re

# --- CONFIGURAÇÃO E FUNÇÕES ---
st.set_page_config(page_title="TMS FRANCAL", layout="wide")
def formatar_cpf(v): return re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\d{2}', re.sub(r'\D', '', v))
def formatar_cep(v): return re.sub(r'(\d{5})(\d{3})', r'\1-\2', re.sub(r'\D', '', v))

menu = st.sidebar.selectbox("Módulo", ["Operação: Coletas", "Cadastro: Motoristas"])

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    if 'data' not in st.session_state: st.session_state.data = None

    c1, c2 = st.columns([3, 1])
    with c1: cpf_in = st.text_input("CPF (Somente números)")
    with c2: 
        if st.button("Buscar"):
            resp = requests.get(f"https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec?cpf={cpf_in}").json()
            st.session_state.data = resp if "status" not in resp else None

    d = st.session_state.data or ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    
    with st.form("motorista_form"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome", value=d[0])
            tel = st.text_input("Telefone", value=d[1])
            cep = st.text_input("CEP", value=d[2])
            # Busca Automática CEP
            if len(re.sub(r'\D', '', cep)) == 8:
                end = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()
                log, bair = end.get('logradouro', ''), end.get('bairro', '')
            else: log, bair = d[3], d[6]
            logradouro = st.text_input("Logradouro", value=log)
            numero = st.text_input("Número", value=d[4])
        with col2:
            uf = st.selectbox("UF", ["MG", "SP", "RJ", "ES", "DF"], index=0) # Lista completa necessária aqui
            mun = st.selectbox("Município", ["Belo Horizonte", "Ibirité"]) # Exemplo: Integrar com API IBGE
            bairro = st.text_input("Bairro", value=bair)
            cpf = st.text_input("CPF", value=d[10])
            rntrc = st.text_input("RNTRC", value=d[13])

        b1, b2, b3 = st.columns(3)
        if b1.form_submit_button("Salvar Novo"): # Lógica de Append
             pass 
        if b2.form_submit_button("Atualizar"): # Lógica de Update
             pass
        if b3.form_button("Limpar"): st.session_state.data = None; st.rerun()

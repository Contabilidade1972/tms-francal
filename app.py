import streamlit as st
import requests
import re

# --- CONFIGURAÇÃO E FUNÇÕES ---
st.set_page_config(page_title="TMS FRANCAL", layout="wide")

def formatar_cpf(v): return re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\d{2}', re.sub(r'\D', '', v))

st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.selectbox("Módulo", ["Operação: Coletas", "Cadastro: Motoristas"])

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    
    # Gerenciamento de estado
    if 'data' not in st.session_state: st.session_state.data = None

    # Botão de Limpar (FORA do formulário)
    if st.button("Limpar / Novo Cadastro"):
        st.session_state.data = None
        st.rerun()

    c1, c2 = st.columns([3, 1])
    with c1: cpf_in = st.text_input("CPF (Somente números)")
    with c2: 
        if st.button("Buscar"):
            url = f"https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec?cpf={cpf_in}"
            try:
                resp = requests.get(url).json()
                st.session_state.data = resp if "status" not in resp else None
                st.rerun()
            except: st.error("Erro na comunicação.")

    d = st.session_state.data or ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    
    with st.form("motorista_form"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome", value=d[0])
            tel = st.text_input("Telefone", value=d[1])
            cep = st.text_input("CEP", value=d[2])
            logradouro = st.text_input("Logradouro", value=d[3])
            numero = st.text_input("Número", value=d[4])
        with col2:
            uf = st.selectbox("UF", ["MG", "SP", "RJ", "ES", "DF"], index=0)
            bairro = st.text_input("Bairro", value=d[6])
            municipio = st.text_input("Município", value=d[7])
            cpf = st.text_input("CPF", value=d[10])
            rntrc = st.text_input("RNTRC", value=d[13])

        b1, b2 = st.columns(2)
        submit_save = b1.form_submit_button("Salvar Novo")
        submit_upd = b2.form_submit_button("Atualizar")

        if submit_save or submit_upd:
            payload = {"tipo": "MOTORISTA", "nome": nome, "telefone": tel, "cep": cep, 
                       "logradouro": logradouro, "numero": numero, "bairro": bairro, 
                       "municipio": municipio, "uf": uf, "cpf": cpf, "rntrc": rntrc}
            requests.post("https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec", json=payload)
            st.success("Dados processados com sucesso!")

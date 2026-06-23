import streamlit as st
import requests

# CONFIGURAÇÃO CENTRALIZADA
URL_SCRIPT = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec"

st.set_page_config(layout="wide", page_title="TMS FRANCAL")
st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.selectbox("Módulo", ["Cadastro: Motoristas", "Relatórios"])

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    
    # Campo de busca com botão explícito
    cpf_in = st.text_input("CPF (Somente números)")
    if st.button("Buscar Motorista"):
        try:
            resp = requests.get(f"{URL_SCRIPT}?cpf={cpf_in}", timeout=10).json()
            st.session_state.data = resp if "status" not in resp else None
            st.rerun()
        except: st.error("Erro na comunicação.")

    d = st.session_state.data or {}

    with st.form("motorista_form"):
        # Seção organizada em colunas
        c1, c2, c3 = st.columns(3)
        nome = c1.text_input("Nome", value=d.get('Nome', ''))
        tel = c2.text_input("Telefone", value=d.get('Telefone', ''))
        nasc = c3.text_input("Data de Nascimento", value=d.get('DataNasc', ''))
        
        # ... (insira os outros campos seguindo o padrão d.get('NomeDoCampo', '')) ...

        if st.form_submit_button("Salvar / Atualizar"):
            payload = {
                "nome": nome, "telefone": tel, "cpf": cpf_in, 
                # ... inclua todos os campos aqui ...
            }
            try:
                response = requests.post(URL_SCRIPT, json=payload)
                if response.status_code == 200:
                    st.success("Dados salvos!")
                else:
                    st.error(f"Erro ao salvar: {response.status_code}")
            except Exception as e:
                st.error(f"Erro: {str(e)}")

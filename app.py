import streamlit as st
import requests

st.set_page_config(page_title="TMS FRANCAL", layout="wide")
menu = st.sidebar.selectbox("Módulo", ["Cadastro: Motoristas"])

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    if 'data' not in st.session_state: st.session_state.data = None

    c1, c2 = st.columns([3, 1])
    cpf_in = c1.text_input("CPF (Somente números)")
    if c2.button("Buscar"):
        # USE A URL DO SEU NOVO DEPLOY
        url = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec?cpf=" + cpf_in
        try:
            resp = requests.get(url, timeout=10).json()
            st.session_state.data = resp if "status" not in resp else None
            st.rerun()
        except: st.error("Erro na comunicação com o banco.")

    d = st.session_state.data or [""] * 22
    
    with st.form("motorista_form"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome", value=d[0])
            tel = st.text_input("Telefone", value=d[1])
            cep = st.text_input("CEP", value=d[2])
            log = st.text_input("Logradouro", value=d[3])
            num = st.text_input("Número", value=d[4])
            comp = st.text_input("Complemento", value=d[5])
            bairro = st.text_input("Bairro", value=d[6])
            mun = st.text_input("Município", value=d[7])
        with col2:
            uf = st.text_input("UF", value=d[8])
            rg = st.text_input("RG", value=d[9])
            cpf = st.text_input("CPF", value=d[10])
            cnh = st.text_input("CNH", value=d[11])
            banco = st.text_input("Banco", value=d[14])
            agencia = st.text_input("Agência", value=d[15])
            conta = st.text_input("Conta", value=d[16])
            rntrc = st.text_input("RNTRC", value=d[13])

        if st.form_submit_button("Salvar / Atualizar"):
            payload = {
                "tipo": "MOTORISTA", "nome": nome, "telefone": tel, "cep": cep, "logradouro": log, 
                "numero": num, "complemento": comp, "bairro": bairro, "municipio": mun, 
                "uf": uf, "rg": rg, "cpf": cpf, "cnh": cnh, "rntrc": rntrc, 
                "banco": banco, "agencia": agencia, "conta": conta
            }
            requests.post("https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec", json=payload)
            st.success("Dados salvos!")

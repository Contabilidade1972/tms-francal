import streamlit as st
import requests

st.set_page_config(page_title="TMS FRANCAL", layout="wide")
st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.selectbox("Módulo", ["Operação: Coletas", "Cadastro: Motoristas"])

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    
    # Inicializa o estado dos campos para permitir edição
    if 'logradouro' not in st.session_state: st.session_state.logradouro = ""
    if 'bairro' not in st.session_state: st.session_state.bairro = ""
    if 'municipio' not in st.session_state: st.session_state.municipio = ""
    if 'uf' not in st.session_state: st.session_state.uf = ""

    with st.form(key="motorista_form"):
        col1, col2 = st.columns(2)
        with col1:
            cpf = st.text_input("CPF (Digite para buscar)")
            nome = st.text_input("Nome (Motorista)")
            telefone = st.text_input("Telefone Comercial")
            cep = st.text_input("CEP")
            # Usa os valores do session_state para permitir edição manual
            logradouro = st.text_input("Logradouro", value=st.session_state.logradouro)
            numero = st.text_input("Número")
            complemento = st.text_input("Complemento")
            bairro = st.text_input("Bairro", value=st.session_state.bairro)
        with col2:
            municipio = st.text_input("Município", value=st.session_state.municipio)
            uf = st.text_input("UF", value=st.session_state.uf)
            rg = st.text_input("RG")
            cnh = st.text_input("CNH")
            uf_cnh = st.text_input("UF/CNH")
            rntrc = st.text_input("RNTRC")

        # Lógica de Busca de CEP
        if len(cep) == 8:
            res = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            if res.status_code == 200:
                dados = res.json()
                if "erro" not in dados:
                    st.session_state.logradouro = dados['logradouro']
                    st.session_state.bairro = dados['bairro']
                    st.session_state.municipio = dados['localidade']
                    st.session_state.uf = dados['uf']
                    st.rerun() # Atualiza a tela para preencher os campos

        submit_motorista = st.form_submit_button("SALVAR / ATUALIZAR MOTORISTA")
        
        if submit_motorista:
            url = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec"
            payload = {
                "tipo": "MOTORISTA", "nome": nome, "telefone": telefone, "cep": cep, 
                "logradouro": logradouro, "numero": numero, "complemento": complemento, 
                "bairro": bairro, "municipio": municipio, "uf": uf, "rg": rg, 
                "cpf": cpf, "cnh": cnh, "uf_cnh": uf_cnh, "rntrc": rntrc
            }
            requests.post(url, json=payload)
            st.success("Dados salvos com sucesso!")

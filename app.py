import streamlit as st
import requests

st.set_page_config(page_title="TMS FRANCAL", layout="wide")

st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.selectbox("Módulo", ["Operação: Coletas", "Cadastro: Motoristas"])

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    with st.form(key="motorista_form"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome (Motorista)")
            telefone = st.text_input("Telefone Comercial")
            cep = st.text_input("CEP")
            logradouro = st.text_input("Logradouro")
            numero = st.text_input("Número")
            complemento = st.text_input("Complemento")
            bairro = st.text_input("Bairro")
        with col2:
            municipio = st.text_input("Município")
            uf = st.text_input("UF")
            rg = st.text_input("RG")
            cpf = st.text_input("CPF")
            cnh = st.text_input("CNH")
            uf_cnh = st.text_input("UF/CNH")
            rntrc = st.text_input("RNTRC")

        submit_motorista = st.form_submit_button("SALVAR MOTORISTA")
        
        if submit_motorista:
            url = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec"
            payload = {
                "tipo": "MOTORISTA", "nome": nome, "telefone": telefone, "cep": cep, 
                "logradouro": logradouro, "numero": numero, "complemento": complemento, 
                "bairro": bairro, "municipio": municipio, "uf": uf, "rg": rg, 
                "cpf": cpf, "cnh": cnh, "uf_cnh": uf_cnh, "rntrc": rntrc
            }
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    st.success("Motorista cadastrado!")
                else:
                    st.error("Erro no envio.")
            except Exception as e:
                st.error(str(e))
# (Módulo Coletas segue igual)

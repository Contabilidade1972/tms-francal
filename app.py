import streamlit as st
import requests

# Configuração inicial
st.set_page_config(page_title="TMS FRANCAL", layout="wide")

# Definição do menu na barra lateral
st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.selectbox("Módulo", ["Operação: Coletas", "Cadastro: Motoristas"])

# --- MÓDULO MOTORISTAS ---
if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    with st.form(key="motorista_form", clear_on_submit=True):
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
                    st.success("Motorista cadastrado com sucesso!")
                else:
                    st.error(f"Erro no envio: {response.status_code}")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")

# --- MÓDULO COLETAS ---
elif menu == "Operação: Coletas":
    st.title("TMS FRANCAL - ORDEM DE COLETA")
    with st.form(key="coleta_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            cnpj_rem = st.text_input("CNPJ Remetente")
            cnpj_dest = st.text_input("CNPJ Destinatário")
            peso = st.number_input("Peso Bruto (kg)", min_value=0.0, format="%.2f")
        with col2:
            nf = st.text_input("Número da NF")
            volume = st.number_input("Volumes", min_value=0)
            valor = st.number_input("Valor da Mercadoria (R$)", min_value=0.0, format="%.2f")
        obs = st.text_area("Observações")
        submit_coleta = st.form_submit_button("SALVAR ORDEM DE COLETA")

    if submit_coleta:
        url = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec"
        payload = {
            "cnpj_remetente": cnpj_rem, "cnpj_destinatario": cnpj_dest,
            "nf": nf, "peso": peso, "volume": volume,
            "valor": valor, "observacoes": obs
        }
        requests.post(url, json=payload)
        st.success("Ordem de Coleta enviada!")

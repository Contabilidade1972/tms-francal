import streamlit as st
import requests

st.set_page_config(page_title="TMS FRANCAL", layout="wide")

menu = st.sidebar.selectbox("Módulo", ["Operação: Coletas", "Cadastro: Motoristas"])

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    
    # Campos que usaremos para busca
    cpf = st.text_input("CPF (Digite para buscar)")
    nome = st.text_input("Nome (Motorista)")
    cep = st.text_input("CEP")
    
    # Gatilho ViaCEP
    if len(cep) == 8:
        res = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        if res.status_code == 200:
            dados = res.json()
            st.info(f"Endereço encontrado: {dados.get('logradouro')}, {dados.get('bairro')}")

    # Botão de Salvar
    if st.button("SALVAR / ATUALIZAR MOTORISTA"):
        # Payload com todos os campos...
        # (mesma estrutura que já criamos)
        st.success("Dados processados com sucesso!")

import streamlit as st

st.set_page_config(page_title="TMS FRANCAL", layout="wide")

menu = st.sidebar.selectbox("Módulo do Sistema", 
                            ["Operação: Coletas", "Cadastro: Clientes", "Cadastro: Motoristas", "Cadastro: Veículos"])

if menu == "Operação: Coletas":
    # Aqui entra o formulário que já temos funcionando
    st.title("Ordem de Coleta")
elif menu == "Cadastro: Clientes":
    st.title("Cadastro de Clientes")
    # Futuro formulário de clientes
elif menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    # Futuro formulário de motoristas
elif menu == "Cadastro: Veículos":
    st.title("Cadastro de Veículos")
    # Futuro formulário de veículos

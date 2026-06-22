import streamlit as st
import requests

# Validador de CPF simples
def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11: return False
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]): return False
    return True

st.set_page_config(page_title="TMS FRANCAL", layout="wide")
st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.selectbox("Módulo", ["Operação: Coletas", "Cadastro: Motoristas"])

# --- MÓDULO MOTORISTAS ---
if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    with st.form(key="motorista_form", clear_on_submit=True):
        nome = st.text_input("Nome do Motorista")
        cpf = st.text_input("CPF (apenas números)")
        cnh = st.text_input("CNH")
        telefone = st.text_input("Telefone")
        rntrc = st.text_input("RNTRC")
        
        submit_motorista = st.form_submit_button("SALVAR MOTORISTA")
        
        if submit_motorista:
            if not validar_cpf(cpf):
                st.error("CPF Inválido! Verifique o número.")
            else:
                # URL de envio (usaremos o mesmo link do Apps Script)
                url = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec"
                payload = {"tipo": "MOTORISTA", "nome": nome, "cpf": cpf, "cnh": cnh, "telefone": telefone, "rntrc": rntrc}
                requests.post(url, json=payload)
                st.success("Motorista cadastrado com sucesso!")

# --- MÓDULO COLETAS (O que já funcionava) ---
elif menu == "Operação: Coletas":
    # (Cole aqui o código anterior do formulário de coleta)
    st.write("Módulo de Coletas ativo...")

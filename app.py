import streamlit as st
import requests
import re

st.set_page_config(layout="wide")
st.title("Cadastro de Motoristas - TMS FRANCAL")

# Inicializa session_state
if 'data' not in st.session_state: st.session_state.data = [""] * 23

# Função de busca
cpf_in = st.text_input("Buscar por CPF (apenas números)")
if st.button("Buscar Motorista"):
    url = f"https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec?cpf={cpf_in}"
    try:
        resp = requests.get(url, timeout=10).json()
        st.session_state.data = resp if "status" not in resp else [""] * 23
        st.rerun()
    except: st.error("Erro na comunicação.")

d = st.session_state.data

with st.form("motorista_form"):
    st.subheader("Dados Pessoais")
    c1, c2, c3 = st.columns(3)
    nome = c1.text_input("Nome", value=d[0])
    tel = c2.text_input("Telefone Comercial", value=d[1])
    nasc = c3.text_input("Data de Nascimento", value=d[17])
    
    st.subheader("Endereço")
    c1, c2, c3 = st.columns(3)
    cep = c1.text_input("CEP", value=d[2])
    log = c2.text_input("Logradouro", value=d[3])
    num = c3.text_input("Número", value=d[4])
    comp = c1.text_input("Complemento", value=d[5])
    bairro = c2.text_input("Bairro", value=d[6])
    mun = c3.text_input("Município", value=d[7])
    uf = c1.selectbox("UF", ["MG", "SP", "RJ", "ES", "DF"], index=0)
    rg = c2.text_input("RG", value=d[9])
    
    st.subheader("Habilitação e Banco")
    c1, c2, c3 = st.columns(3)
    cpf = c1.text_input("CPF", value=d[10] or cpf_in)
    cnh = c2.text_input("CNH", value=d[11])
    uf_cnh = c3.text_input("UF/CNH", value=d[12])
    cat = c1.text_input("Categoria", value=d[19])
    emissao = c2.text_input("Emissão CNH", value=d[18])
    venc = c3.text_input("Vencimento CNH", value=d[19])
    fil = c1.text_input("Filiação", value=d[20])
    banco = c2.text_input("Banco", value=d[14])
    ag = c3.text_input("Agência", value=d[15])
    conta = c1.text_input("Conta", value=d[16])
    rntrc = c2.text_input("RNTRC", value=d[13])
    obs = st.text_area("Observações", value=d[21])

    if st.form_submit_button("Salvar / Atualizar"):
        payload = {
            "nome": nome, "telefone": tel, "cep": cep, "logradouro": log, "numero": num,
            "complemento": comp, "bairro": bairro, "municipio": mun, "uf": uf, "rg": rg,
            "cpf": cpf, "cnh": cnh, "uf_cnh": uf_cnh, "rntrc": rntrc, "banco": banco,
            "agencia": ag, "conta": conta, "nasc": nasc, "emissao": emissao,
            "vencimento": venc, "categoria": cat, "filiacao": fil, "obs": obs
        }
        requests.post("https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec", json=payload)
        st.success("Dados salvos com sucesso!")

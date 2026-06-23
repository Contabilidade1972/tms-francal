import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("Cadastro de Motoristas - TMS FRANCAL")

# URL da sua Implantação (substitua pela correta da Versão 16)
URL = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec"

if 'd' not in st.session_state: st.session_state.d = [""] * 23

# Busca
cpf_in = st.text_input("CPF (Somente números)")
if st.button("Buscar"):
    try:
        resp = requests.get(f"{URL}?cpf={cpf_in}", timeout=10).json()
        st.session_state.d = resp if isinstance(resp, list) else [""] * 23
        st.rerun()
    except Exception as e: st.error(f"Erro: {e}")

d = st.session_state.d

with st.form("motorista_form"):
    st.subheader("Dados Pessoais")
    c1, c2, c3 = st.columns(3)
    nome = c1.text_input("Nome", value=d[0])
    tel = c2.text_input("Telefone", value=d[1])
    nasc = c3.text_input("Data Nascimento", value=d[17])
    
    st.subheader("Endereço")
    c4, c5, c6 = st.columns(3)
    cep = c4.text_input("CEP", value=d[2])
    log = c5.text_input("Logradouro", value=d[3])
    num = c6.text_input("Número", value=d[4])
    
    c7, c8, c9 = st.columns(3)
    comp = c7.text_input("Complemento", value=d[5])
    bairro = c8.text_input("Bairro", value=d[6])
    mun = c9.text_input("Município", value=d[7])
    
    c10, c11, c12 = st.columns(3)
    uf = c10.text_input("UF", value=d[8])
    rg = c11.text_input("RG", value=d[9])
    cpf = c12.text_input("CPF", value=d[10] if d[10] else cpf_in)

    st.subheader("Habilitação e Banco")
    c13, c14, c15 = st.columns(3)
    cnh = c13.text_input("CNH", value=d[11])
    ufcnh = c14.text_input("UF/CNH", value=d[12])
    rntrc = c15.text_input("RNTRC", value=d[13])
    
    c16, c17, c18 = st.columns(3)
    emissao = c16.text_input("Emissão CNH", value=d[18])
    venc = c17.text_input("Vencimento CNH", value=d[19])
    cat = c18.text_input("Categoria", value=d[20])
    
    c19, c20, c21 = st.columns(3)
    banco = c19.text_input("Banco", value=d[14])
    ag = c20.text_input("Agência", value=d[15])
    conta = c21.text_input("Conta", value=d[16])
    
    filiacao = st.text_input("Filiação", value=d[21])
    obs = st.text_area("Observações", value=d[22])

    if st.form_submit_button("Salvar / Atualizar"):
        payload = {
            "nome": nome, "telefone": tel, "cep": cep, "logradouro": log, "numero": num,
            "complemento": comp, "bairro": bairro, "municipio": mun, "uf": uf, "rg": rg,
            "cpf": cpf, "cnh": cnh, "uf_cnh": ufcnh, "rntrc": rntrc, "banco": banco,
            "agencia": ag, "conta": conta, "nasc": nasc, "emissao": emissao,
            "vencimento": venc, "categoria": cat, "filiacao": filiacao, "obs": obs
        }
        try:
            requests.post(URL, json=payload)
            st.success("Dados salvos com sucesso!")
        except Exception as e: st.error(f"Erro ao salvar: {e}")

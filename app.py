import streamlit as st
import requests
import re

# Funções de formatação
def formatar_cpf(val):
    val = re.sub(r'\D', '', str(val))
    return f"{val[:3]}.{val[3:6]}.{val[6:9]}-{val[9:]}" if len(val) == 11 else val

def formatar_cep(val):
    val = re.sub(r'\D', '', str(val))
    return f"{val[:5]}-{val[5:]}" if len(val) == 8 else val

st.set_page_config(page_title="TMS FRANCAL", layout="wide")
st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.selectbox("Módulo", ["Operação: Coletas", "Cadastro: Motoristas"])
ufs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    
    # Inicializa estados para garantir que o formulário não trave
    if 'dados_motorista' not in st.session_state: st.session_state.dados_motorista = None
    
    col_busca1, col_busca2 = st.columns([3, 1])
    with col_busca1:
        cpf_input = st.text_input("CPF (Somente números)")
    with col_busca2:
        btn_busca = st.button("Buscar Motorista")

    if btn_busca and cpf_input:
        url_busca = f"https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec?cpf={cpf_input}"
        try:
            resp = requests.get(url_busca).json()
            if "status" not in resp:
                st.session_state.dados_motorista = resp
                st.rerun()
            else:
                st.warning("Motorista não encontrado.")
        except: st.error("Erro na comunicação com a base.")

    dados = st.session_state.dados_motorista
    
    with st.form(key="motorista_form"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome", value=dados[0] if dados else "")
            telefone = st.text_input("Telefone", value=dados[1] if dados else "")
            cep = st.text_input("CEP", value=formatar_cep(dados[2]) if dados else "")
            logradouro = st.text_input("Logradouro", value=dados[3] if dados else "")
            numero = st.text_input("Número", value=dados[4] if dados else "")
            complemento = st.text_input("Complemento", value=dados[5] if dados else "")
            bairro = st.text_input("Bairro", value=dados[6] if dados else "")
        with col2:
            municipio = st.text_input("Município", value=dados[7] if dados else "")
            uf = st.selectbox("UF", ufs, index=ufs.index(dados[8]) if dados and dados[8] in ufs else 12)
            rg = st.text_input("RG", value=dados[9] if dados else "")
            cpf = st.text_input("CPF", value=formatar_cpf(dados[10]) if dados else cpf_input)
            cnh = st.text_input("CNH", value=dados[11] if dados else "")
            uf_cnh = st.text_input("UF/CNH", value=dados[12] if dados else "")
            rntrc = st.text_input("RNTRC", value=dados[13] if dados else "")

        if st.form_submit_button("SALVAR / ATUALIZAR"):
            payload = {"tipo": "MOTORISTA", "nome": nome, "telefone": telefone, "cep": re.sub(r'\D', '', cep), 
                       "logradouro": logradouro, "numero": numero, "complemento": complemento, 
                       "bairro": bairro, "municipio": municipio, "uf": uf, "rg": rg, 
                       "cpf": re.sub(r'\D', '', cpf), "cnh": cnh, "uf_cnh": uf_cnh, "rntrc": rntrc}
            requests.post("https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec", json=payload)
            st.success("Dados salvos com sucesso!")
            st.session_state.dados_motorista = None # Limpa após salvar

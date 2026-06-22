import streamlit as st
import requests
import re

# Função para formatar padrões brasileiros
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
    
    # Inicialização básica
    nome_val, tel_val, cep_val, log_val, num_val, comp_val, bair_val, mun_val, uf_val, rg_val, cpf_val, cnh_val, ufcnh_val, rntrc_val = [""] * 14

    cpf_busca = st.text_input("CPF (Digite apenas números e dê Enter para buscar)")
    
    if cpf_busca:
        url_busca = f"https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec?cpf={cpf_busca}"
        try:
            resp = requests.get(url_busca).json()
            if "status" not in resp:
                st.info("Dados carregados.")
                nome_val, tel_val, cep_val, log_val, num_val, comp_val, bair_val, mun_val, uf_val, rg_val, cpf_val, cnh_val, ufcnh_val, rntrc_val = resp
        except: pass

    with st.form(key="motorista_form"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome", value=nome_val)
            telefone = st.text_input("Telefone", value=tel_val) # Sugestão: aplicar máscara aqui caso precise
            cep = st.text_input("CEP", value=formatar_cep(cep_val))
            logradouro = st.text_input("Logradouro", value=log_val)
            numero = st.text_input("Número", value=num_val)
            complemento = st.text_input("Complemento", value=comp_val)
            bairro = st.text_input("Bairro", value=bair_val)
        with col2:
            municipio = st.text_input("Município", value=mun_val)
            # Seletor de UF
            uf_index = ufs.index(uf_val) if uf_val in ufs else 12 # Default MG
            uf = st.selectbox("UF", ufs, index=uf_index)
            rg = st.text_input("RG", value=rg_val)
            cpf = st.text_input("CPF", value=formatar_cpf(cpf_val))
            cnh = st.text_input("CNH", value=cnh_val)
            uf_cnh = st.text_input("UF/CNH", value=ufcnh_val)
            rntrc = st.text_input("RNTRC", value=rntrc_val)

        submit = st.form_submit_button("SALVAR / ATUALIZAR")
        
        if submit:
            url = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec"
            payload = {
                "tipo": "MOTORISTA", "nome": nome, "telefone": telefone, "cep": cep, 
                "logradouro": logradouro, "numero": numero, "complemento": complemento, 
                "bairro": bairro, "municipio": municipio, "uf": uf, "rg": rg, 
                "cpf": re.sub(r'\D', '', cpf), "cnh": cnh, "uf_cnh": uf_cnh, "rntrc": rntrc
            }
            requests.post(url, json=payload)
            st.success("Dados salvos com sucesso!")

import streamlit as st
import requests

st.set_page_config(page_title="TMS FRANCAL", layout="wide")
ufs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

def formatar_cpf(cpf): return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if len(cpf) == 11 else cpf

menu = st.sidebar.selectbox("Módulo", ["Operação: Coletas", "Cadastro: Motoristas"])

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    cpf_busca = st.text_input("CPF (Digite apenas números e dê Enter para buscar)")
    
    # Lógica de Busca
    if cpf_busca:
        url_busca = f"https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec?cpf={cpf_busca}"
        resp = requests.get(url_busca).json()
        if "status" not in resp:
            st.info("Motorista encontrado! Dados carregados.")
            nome_val, tel_val, cep_val, log_val, num_val, comp_val, bair_val, mun_val, uf_val, rg_val, cpf_val, cnh_val, ufcnh_val, rntrc_val = resp[0], resp[1], resp[2], resp[3], resp[4], resp[5], resp[6], resp[7], resp[8], resp[9], resp[10], resp[11], resp[12], resp[13]
        else:
            st.warning("Motorista novo. Preencha os campos abaixo.")
            nome_val, tel_val, cep_val, log_val, num_val, comp_val, bair_val, mun_val, uf_val, rg_val, cpf_val, cnh_val, ufcnh_val, rntrc_val = "", "", "", "", "", "", "", "", "", "", cpf_busca, "", "", ""

    with st.form("motorista_form"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome", value=nome_val)
            telefone = st.text_input("Telefone", value=tel_val)
            cep = st.text_input("CEP", value=cep_val)
            logradouro = st.text_input("Logradouro", value=log_val)
            numero = st.text_input("Número", value=num_val)
        with col2:
            bairro = st.text_input("Bairro", value=bair_val)
            municipio = st.text_input("Município", value=mun_val)
            uf = st.selectbox("UF", ufs, index=ufs.index(uf_val) if uf_val in ufs else 12)
            cpf = st.text_input("CPF", value=cpf_val)
            cnh = st.text_input("CNH", value=cnh_val)
            rntrc = st.text_input("RNTRC", value=rntrc_val)

        if st.form_submit_button("SALVAR / ATUALIZAR"):
            payload = {"tipo": "MOTORISTA", "nome": nome, "telefone": telefone, "cep": cep, "logradouro": logradouro, "numero": numero, "bairro": bairro, "municipio": municipio, "uf": uf, "cpf": cpf, "cnh": cnh, "rntrc": rntrc}
            requests.post("https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec", json=payload)
            st.success("Dados salvos!")

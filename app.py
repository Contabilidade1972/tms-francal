import streamlit as st
import requests

st.set_page_config(page_title="TMS FRANCAL", layout="wide")

st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.selectbox("Módulo", ["Operação: Coletas", "Cadastro: Motoristas"])

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    
    # Inicialização das variáveis para evitar NameError
    nome_val, tel_val, cep_val, log_val, num_val = "", "", "", "", ""
    comp_val, bair_val, mun_val, uf_val, rg_val = "", "", "", "", ""
    cpf_val, cnh_val, ufcnh_val, rntrc_val = "", "", "", ""

    cpf_busca = st.text_input("CPF (Digite apenas números e dê Enter para buscar)")
    
    if cpf_busca:
        url_busca = f"https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec?cpf={cpf_busca}"
        try:
            resp = requests.get(url_busca).json()
            if "status" not in resp:
                st.info("Motorista encontrado! Dados carregados.")
                nome_val, tel_val, cep_val, log_val, num_val = resp[0], resp[1], resp[2], resp[3], resp[4]
                comp_val, bair_val, mun_val, uf_val, rg_val = resp[5], resp[6], resp[7], resp[8], resp[9]
                cpf_val, cnh_val, ufcnh_val, rntrc_val = resp[10], resp[11], resp[12], resp[13]
        except:
            st.warning("Motorista novo ou erro na busca.")

    with st.form(key="motorista_form"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome", value=nome_val)
            telefone = st.text_input("Telefone", value=tel_val)
            cep = st.text_input("CEP", value=cep_val)
            logradouro = st.text_input("Logradouro", value=log_val)
            numero = st.text_input("Número", value=num_val)
            complemento = st.text_input("Complemento", value=comp_val)
            bairro = st.text_input("Bairro", value=bair_val)
        with col2:
            municipio = st.text_input("Município", value=mun_val)
            uf = st.text_input("UF", value=uf_val)
            rg = st.text_input("RG", value=rg_val)
            cpf = st.text_input("CPF", value=cpf_val)
            cnh = st.text_input("CNH", value=cnh_val)
            uf_cnh = st.text_input("UF/CNH", value=ufcnh_val)
            rntrc = st.text_input("RNTRC", value=rntrc_val)

        submit_motorista = st.form_submit_button("SALVAR / ATUALIZAR")
        
        if submit_motorista:
            url = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec"
            payload = {
                "tipo": "MOTORISTA", "nome": nome, "telefone": telefone, "cep": cep, 
                "logradouro": logradouro, "numero": numero, "complemento": complemento, 
                "bairro": bairro, "municipio": municipio, "uf": uf, "rg": rg, 
                "cpf": cpf, "cnh": cnh, "uf_cnh": uf_cnh, "rntrc": rntrc
            }
            requests.post(url, json=payload)
            st.success("Dados salvos!")

elif menu == "Operação: Coletas":
    st.write("Módulo de Coletas (mantido anteriormente)")

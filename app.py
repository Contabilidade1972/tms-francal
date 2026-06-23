import streamlit as st
import requests

# URL centralizada
URL = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec"

st.set_page_config(layout="wide", page_title="TMS FRANCAL")
st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.selectbox("Módulo", ["Cadastro: Motoristas", "Relatórios"])

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    
    # Gerenciamento de estado inicial
    if 'd' not in st.session_state: st.session_state.d = [""] * 23

    # Busca (Fora do form para ser independente)
    cpf_busca = st.text_input("Buscar por CPF (apenas números)")
    if st.button("Buscar Motorista"):
        try:
            resp = requests.get(f"{URL}?cpf={cpf_busca}", timeout=10).json()
            st.session_state.d = resp if isinstance(resp, list) else [""] * 23
            st.rerun()
        except: st.error("Erro na comunicação.")

    d = st.session_state.d

    with st.form("motorista_form"):
        st.subheader("Dados Pessoais")
        c1, c2, c3 = st.columns(3)
        # Campos simples, sem callbacks proibidos dentro do form
        nome = c1.text_input("Nome", value=d[0])
        tel = c2.text_input("Telefone Comercial", value=d[1])
        nasc = c3.text_input("Data de Nascimento", value=d[17])
        
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
        uf = c10.selectbox("UF", ["MG", "SP", "RJ", "ES", "DF"], index=0)
        rg = c11.text_input("RG", value=d[9])
        cpf = c12.text_input("CPF", value=d[10] if d[10] else cpf_busca)

        st.subheader("Habilitação e Banco")
        h1, h2, h3 = st.columns(3)
        cnh = h1.text_input("CNH", value=d[11])
        uf_cnh = h2.text_input("UF/CNH", value=d[12])
        cat = h3.text_input("Categoria", value=d[20])
        
        h4, h5, h6 = st.columns(3)
        emissao = h4.text_input("Data de Emissão", value=d[18])
        venc = h5.text_input("Vencimento CNH", value=d[19])
        fil = h6.text_input("Filiação", value=d[21])
        
        h7, h8, h9 = st.columns(3)
        banco = h7.text_input("Banco", value=d[14])
        ag = h8.text_input("Agência", value=d[15])
        conta = h9.text_input("Conta", value=d[16])
        
        rntrc = st.text_input("RNTRC", value=d[13])
        obs = st.text_area("Observações", value=d[22])

        # BOTÃO SUBMIT OBRIGATÓRIO
        submit = st.form_submit_button("SALVAR / ATUALIZAR DADOS")

        if submit:
            payload = {
                "nome": nome.upper(), "telefone": tel, "cep": cep, "logradouro": log.upper(),
                "numero": num, "complemento": comp.upper(), "bairro": bairro.upper(),
                "municipio": mun.upper(), "uf": uf, "rg": rg, "cpf": cpf, "cnh": cnh,
                "uf_cnh": uf_cnh, "rntrc": rntrc, "banco": banco.upper(), "agencia": ag,
                "conta": conta, "nasc": nasc, "emissao": emissao, "vencimento": venc,
                "categoria": cat.upper(), "filiacao": fil.upper(), "obs": obs.upper()
            }
            try:
                requests.post(URL, json=payload)
                st.success("Dados salvos com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

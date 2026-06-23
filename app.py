import streamlit as st
import requests

URL = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec"
LISTA_BANCOS = ["001 - BANCO DO BRASIL", "104 - CAIXA ECONÔMICA", "341 - ITAÚ", "033 - SANTANDER", "237 - BRADESCO"]
UF_LISTA = ["MG", "SP", "RJ", "ES", "DF"]

st.set_page_config(layout="wide")

# MENU LATERAL
st.sidebar.title("TMS FRANCAL")
modulo = st.sidebar.radio("Módulos", ["Cadastro: Motoristas", "Relatórios"])

if modulo == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    if 'd' not in st.session_state: st.session_state.d = [""] * 23
    
    cpf_busca = st.text_input("Buscar por CPF")
    if st.button("Buscar"):
        r = requests.get(f"{URL}?cpf={cpf_busca}")
        st.session_state.d = r.json() if r.status_code == 200 else [""] * 23
        st.rerun()

    d = st.session_state.d
    with st.form("motorista_form"):
        # Campos Pessoais
        c1, c2, c3 = st.columns(3)
        nome = c1.text_input("Nome", value=d[0]).upper()
        tel = c2.text_input("Telefone", value=d[1])
        nasc = c3.text_input("Data Nascimento", value=d[17])
        
        # CEP AUTOMÁTICO
        c4, c5, c6 = st.columns(3)
        cep = c4.text_input("CEP", value=d[2])
        if len(cep.replace("-","")) == 8:
            try:
                res = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()
                log, bair, mun = res['logradouro'], res['bairro'], res['localidade']
            except: log, bair, mun = d[3], d[6], d[7]
        else: log, bair, mun = d[3], d[6], d[7]
        
        log = c5.text_input("Logradouro", value=log).upper()
        num = c6.text_input("Número", value=d[4])
        
        c7, c8, c9 = st.columns(3)
        comp = c7.text_input("Complemento", value=d[5]).upper()
        bair = c8.text_input("Bairro", value=bair).upper()
        mun = c9.text_input("Município", value=mun).upper()
        
        # SELECTBOX PARA BANCOS E UF
        c10, c11, c12 = st.columns(3)
        uf = c10.selectbox("UF", UF_LISTA, index=UF_LISTA.index(d[8]) if d[8] in UF_LISTA else 0)
        banco = c11.selectbox("Banco", LISTA_BANCOS, index=LISTA_BANCOS.index(d[14]) if d[14] in LISTA_BANCOS else 0)
        cpf = c12.text_input("CPF", value=d[10] if d[10] else cpf_busca)
        
        # BOTÕES SEPARADOS
        c_btn1, c_btn2 = st.columns(2)
        salvar = c_btn1.form_submit_button("SALVAR NOVO")
        atualizar = c_btn2.form_submit_button("ATUALIZAR DADOS")
        
        if salvar or atualizar:
            # Lógica de envio (seu payload aqui...)
            st.success("Dados salvos!")

elif modulo == "Relatórios":
    st.title("Módulo de Relatórios")
    st.write("Em breve: Integração com Power BI.")

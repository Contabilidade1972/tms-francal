import streamlit as st
import requests

st.set_page_config(page_title="TMS FRANCAL", layout="wide")
menu = st.sidebar.selectbox("Módulo", ["Cadastro: Motoristas"])

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    if 'data' not in st.session_state: st.session_state.data = None

    col_b, col_btn = st.columns([4, 1])
    cpf_in = col_b.text_input("CPF (Somente números)")
    if col_btn.button("Buscar"):
        url = f"https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec?cpf={cpf_in}"
        try:
            resp = requests.get(url, timeout=10).json()
            st.session_state.data = resp if "status" not in resp else None
            st.rerun()
        except: st.error("Erro na comunicação.")

    d = st.session_state.data or [""] * 22
    
    with st.form("motorista_form"):
        st.subheader("Dados Pessoais e Bancários")
        c1, c2, c3 = st.columns(3)
        nome = c1.text_input("Nome", value=d[0])
        tel = c2.text_input("Telefone", value=d[1])
        banco = c3.text_input("Banco", value=d[14])
        agencia = c1.text_input("Agência", value=d[15])
        conta = c2.text_input("Conta", value=d[16])
        
        st.subheader("Habilitação")
        h1, h2, h3 = st.columns(3)
        cnh = h1.text_input("CNH", value=d[11])
        cat = h2.text_input("Categoria", value=d[19])
        venc = h3.date_input("Vencimento CNH", value=None) # Necessita tratamento de data
        emissao = h1.date_input("Emissão", value=None)
        fil = h2.text_input("Filiação", value=d[20])
        obs = h3.text_area("Observações", value=d[21])

        if st.form_submit_button("Salvar / Atualizar"):
            payload = {
                "tipo": "MOTORISTA", "nome": nome, "telefone": tel, "cpf": d[10] or cpf_in,
                "banco": banco, "agencia": agencia, "conta": conta, "cnh": cnh,
                "categoria": cat, "filiacao": fil, "obs": obs
            }
            try:
                requests.post("https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec", json=payload)
                st.success("Dados salvos!")
            except: st.error("Falha ao salvar.")

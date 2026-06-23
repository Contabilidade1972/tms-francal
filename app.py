import streamlit as st
import requests

# URL oficial da sua Versão 30
URL = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec"

LISTA_BANCOS = ["001 - BANCO DO BRASIL", "104 - CAIXA ECONÔMICA", "341 - ITAÚ", "033 - SANTANDER", "237 - BRADESCO"]
UF_LISTA = ["MG", "SP", "RJ", "ES", "DF"]

st.set_page_config(layout="wide", page_title="TMS FRANCAL")

# MENU LATERAL
st.sidebar.title("TMS FRANCAL")
modulo = st.sidebar.radio("Módulos", ["Cadastro: Motoristas", "Relatórios"])

if modulo == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    
    if 'd' not in st.session_state: st.session_state.d = [""] * 23
    
    # BUSCA
    cpf_busca = st.text_input("Buscar por CPF (apenas números)")
    if st.button("Buscar Motorista"):
        try:
            r = requests.get(f"{URL}?cpf={cpf_busca}", timeout=10)
            st.session_state.d = r.json() if r.status_code == 200 else [""] * 23
            st.rerun()
        except Exception as e: st.error(f"Erro na busca: {e}")

    d = st.session_state.d

    # FORMULÁRIO
    with st.form("motorista_form"):
        st.subheader("Dados Pessoais")
        c1, c2, c3 = st.columns(3)
        nome = c1.text_input("Nome", value=d[0]).upper()
        tel = c2.text_input("Telefone Comercial", value=d[1])
        nasc = c3.text_input("Data de Nascimento", value=d[17])
        
        st.subheader("Endereço")
        c4, c5, c6 = st.columns(3)
        cep = c4.text_input("CEP", value=d[2])
        
        # LÓGICA CEP AUTOMÁTICO
        log, bair, mun = d[3], d[6], d[7]
        if len(cep.replace("-","")) == 8:
            try:
                res = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5).json()
                log, bair, mun = res.get('logradouro', d[3]), res.get('bairro', d[6]), res.get('localidade', d[7])
            except: pass
            
        log = c5.text_input("Logradouro", value=log).upper()
        num = c6.text_input("Número", value=d[4])
        
        c7, c8, c9 = st.columns(3)
        comp = c7.text_input("Complemento", value=d[5]).upper()
        bairro = c8.text_input("Bairro", value=bair).upper()
        mun = c9.text_input("Município", value=mun).upper()
        
        c10, c11, c12 = st.columns(3)
        uf = c10.selectbox("UF", UF_LISTA, index=UF_LISTA.index(d[8]) if d[8] in UF_LISTA else 0)
        rg = c11.text_input("RG", value=d[9])
        cpf = c12.text_input("CPF", value=d[10] if d[10] else cpf_busca)

        st.subheader("Habilitação e Banco")
        h1, h2, h3 = st.columns(3)
        cnh = h1.text_input("CNH", value=d[11])
        ufcnh = h2.text_input("UF/CNH", value=d[12])
        rntrc = h3.text_input("RNTRC", value=d[13])
        
        h4, h5, h6 = st.columns(3)
        emissao = h4.text_input("Data de Emissão", value=d[18])
        venc = h5.text_input("Vencimento CNH", value=d[19])
        cat = h6.text_input("Categoria", value=d[20]).upper()
        
        h7, h8, h9 = st.columns(3)
        banco = h7.selectbox("Banco", LISTA_BANCOS, index=LISTA_BANCOS.index(d[14]) if d[14] in LISTA_BANCOS else 0)
        ag = h8.text_input("Agência", value=d[15])
        conta = h9.text_input("Conta", value=d[16])
        
        filiacao = st.text_input("Filiação", value=d[21]).upper()
        obs = st.text_area("Observações", value=d[22]).upper()

        # BOTÕES SEPARADOS
        btn1, btn2 = st.columns(2)
        salvar_novo = btn1.form_submit_button("SALVAR NOVO")
        atualizar = btn2.form_submit_button("ATUALIZAR DADOS")

        if salvar_novo or atualizar:
            payload = {
                "nome": nome, "tel": tel, "cep": cep, "log": log, "num": num,
                "comp": comp, "bair": bairro, "mun": mun, "uf": uf, "rg": rg,
                "cpf": cpf, "cnh": cnh, "ufcnh": ufcnh, "rntrc": rntrc, "banco": banco,
                "ag": ag, "conta": conta, "nasc": nasc, "emis": emissao,
                "venc": venc, "cat": cat, "fil": filiacao, "obs": obs
            }
            try:
                requests.post(URL, json=payload)
                st.success("Operação realizada com sucesso!")
            except Exception as e: st.error(f"Erro ao salvar: {e}")

elif modulo == "Relatórios":
    st.title("Módulo de Relatórios")
    st.info("Aguardando configuração de consultas PBI/Logs.")

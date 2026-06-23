import streamlit as st
import requests
import re

# Configuração da Página
st.set_page_config(layout="wide", page_title="TMS FRANCAL")

# Inicialização segura do estado
if 'data' not in st.session_state:
    st.session_state.data = {}

# Função para aplicar máscaras
def aplicar_mascara(val, tipo):
    v = re.sub(r'\D', '', str(val))
    if tipo == 'cpf': return f"{v[:3]}.{v[3:6]}.{v[6:9]}-{v[9:]}" if len(v) == 11 else v
    if tipo == 'cep': return f"{v[:5]}-{v[5:]}" if len(v) == 8 else v
    if tipo == 'tel': return f"({v[:2]}) {v[2:6]}-{v[6:]}" if len(v) == 10 else v
    return v

st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.selectbox("Módulo", ["Cadastro: Motoristas", "Relatórios"])

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    
    # Busca com tratamento de erros
    d = st.session_state.data
    c1, c2 = st.columns([3, 1])
    cpf_busca = c1.text_input("CPF (Somente números)", key="cpf_busca_input")
    if c2.button("Buscar Motorista"):
        url = f"https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec?cpf={cpf_busca}"
        try:
            resp = requests.get(url, timeout=10).json()
            st.session_state.data = resp if "status" not in resp else {}
            st.rerun()
        except: st.error("Erro na comunicação com a base.")

    with st.form("motorista_form"):
        st.subheader("Dados Pessoais")
        c1, c2, c3 = st.columns(3)
        nome = c1.text_input("Nome", value=d.get('Nome', ''))
        tel = c2.text_input("Telefone Comercial", value=d.get('Telefone Comercial', ''))
        nasc = c3.text_input("Data de Nascimento", value=d.get('DataNasc', ''))
        
        st.subheader("Endereço")
        c1, c2, c3 = st.columns(3)
        cep = c1.text_input("CEP", value=d.get('CEP', ''))
        log = c2.text_input("Logradouro", value=d.get('Logradouro', ''))
        num = c3.text_input("Número", value=d.get('Número', ''))
        
        c4, c5, c6 = st.columns(3)
        comp = c4.text_input("Complemento", value=d.get('Complemento', ''))
        bairro = c5.text_input("Bairro", value=d.get('Bairro', ''))
        mun = c6.text_input("Município", value=d.get('Município', ''))
        
        c7, c8, c9 = st.columns(3)
        uf = c7.selectbox("UF", ["MG", "SP", "RJ", "ES", "DF"], index=0)
        rg = c8.text_input("RG", value=d.get('RG', ''))
        cpf = c9.text_input("CPF", value=d.get('CPF', ''))

        st.subheader("Habilitação e Banco")
        h1, h2, h3 = st.columns(3)
        cnh = h1.text_input("CNH", value=d.get('CNH', ''))
        uf_cnh = h2.text_input("UF/CNH", value=d.get('UF/CNH', ''))
        cat = h3.text_input("Categoria", value=d.get('Categoria', ''))
        
        h4, h5, h6 = st.columns(3)
        emissao = h4.text_input("Data de Emissão", value=d.get('EmissãoCNH', ''))
        venc = h5.text_input("Vencimento CNH", value=d.get('VencimentoCNH', ''))
        filiacao = h6.text_input("Filiação", value=d.get('Filiação', ''))
        
        h7, h8, h9 = st.columns(3)
        banco = h7.text_input("Banco", value=d.get('Banco', ''))
        agencia = h8.text_input("Agência", value=d.get('Agência', ''))
        conta = h9.text_input("Conta", value=d.get('Conta', ''))
        
        rntrc = st.text_input("RNTRC", value=d.get('RNTRC', ''))
        obs = st.text_area("Observações", value=d.get('Observação', ''))

        if st.form_submit_button("Salvar / Atualizar"):
            payload = {
                "nome": nome, "telefone": tel, "cep": cep, "logradouro": log, "numero": num,
                "complemento": comp, "bairro": bairro, "municipio": mun, "uf": uf, "rg": rg,
                "cpf": cpf, "cnh": cnh, "uf_cnh": uf_cnh, "rntrc": rntrc, "banco": banco,
                "agencia": agencia, "conta": conta, "nasc": nasc, "emissao": emissao,
                "vencimento": venc, "categoria": cat, "filiacao": filiacao, "obs": obs
            }
            try:
                requests.post("https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec", json=payload)
                st.success("Dados salvos!")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

if st.button("Limpar Tela"):
    st.session_state.data = {}
    st.rerun()

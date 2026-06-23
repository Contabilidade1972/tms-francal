import streamlit as st
import requests

# URL da sua Implantação (Substitua pela URL da sua Nova Versão)
URL = "SUA_URL_AQUI"

st.set_page_config(layout="wide")
st.title("Cadastro de Motoristas - TMS FRANCAL")

if 'd' not in st.session_state: st.session_state.d = [""] * 23

cpf_busca = st.text_input("Buscar por CPF (apenas números)")
if st.button("Buscar Motorista"):
    try:
        resp = requests.get(f"{URL}?cpf={cpf_busca}", timeout=10).json()
        st.session_state.d = resp if isinstance(resp, list) else [""] * 23
        st.rerun()
    except: st.error("Erro na comunicação com a base.")

d = st.session_state.d

with st.form("motorista_form"):
    st.subheader("Dados Pessoais")
    c1, c2, c3 = st.columns(3)
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
    uf = c10.text_input("UF", value=d[8])
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
    cat = h6.text_input("Categoria", value=d[20])
    
    h7, h8, h9 = st.columns(3)
    banco = h7.text_input("Banco", value=d[14])
    ag = h8.text_input("Agência", value=d[15])
    conta = h9.text_input("Conta", value=d[16])
    
    filiacao = st.text_input("Filiação", value=d[21])
    obs = st.text_area("Observações", value=d[22])

    if st.form_submit_button("SALVAR / ATUALIZAR DADOS"):
        payload = {
            "nome": nome, "tel": tel, "cep": cep, "log": log, "num": num,
            "comp": comp, "bair": bairro, "mun": mun, "uf": uf, "rg": rg,
            "cpf": cpf, "cnh": cnh, "ufcnh": ufcnh, "rntrc": rntrc, "banco": banco,
            "ag": ag, "conta": conta, "nasc": nasc, "emis": emissao,
            "venc": venc, "cat": cat, "fil": filiacao, "obs": obs
        }
        try:
            requests.post(URL, json=payload)
            st.success("Dados salvos com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")

import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="TMS FRANCAL", layout="wide")

def get_sheet():
    # Carrega a chave única 'gcp_json'
    service_account_info = json.loads(st.secrets["gcp_json"])
    scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg").worksheet("REGISTRO_OPERACIONAL")

st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.radio("Navegação", ["Cadastro de Motorista", "Consulta/Auditoria"])

if menu == "Cadastro de Motorista":
    st.header("👤 Cadastro Completo de Motorista")
    with st.form("form_tms", clear_on_submit=False):
        cpf_busca = st.text_input("CPF para busca")
        if st.form_submit_button("Buscar CPF"):
            try:
                dados = get_sheet().get_all_values()
                for row in dados:
                    if len(row) > 10 and row[10] == cpf_busca:
                        st.session_state.data = row
                        st.success("Dados carregados!")
            except Exception as e: st.error(f"Erro: {e}")

        d = st.session_state.get('data', [""] * 23)
        
        # Grid Profissional (23 campos mapeados)
        c1, c2, c3 = st.columns(3)
        nome = c1.text_input("Nome", value=d[0])
        tel = c2.text_input("Telefone", value=d[1])
        cep = c3.text_input("CEP", value=d[2])
        logra = c1.text_input("Logradouro", value=d[3])
        num = c2.text_input("Número", value=d[4])
        compl = c3.text_input("Complemento", value=d[5])
        bairro = c1.text_input("Bairro", value=d[6])
        muni = c2.text_input("Município", value=d[7])
        uf = c3.text_input("UF", value=d[8])
        rg = c1.text_input("RG", value=d[9])
        cpf = c2.text_input("CPF", value=d[10])
        cnh = c3.text_input("CNH", value=d[11])
        ufcnh = c1.text_input("UF/CNH", value=d[12])
        rntrc = c2.text_input("RNTRC", value=d[13])
        banco = c3.text_input("Banco", value=d[14])
        agencia = c1.text_input("Agência", value=d[15])
        conta = c2.text_input("Conta", value=d[16])
        nasc = c2.text_input("Data Nasc/Emissão", value=d[17])
        venc = c3.text_input("Venc CNH", value=d[18])
        cat = c1.text_input("Categoria", value=d[19])
        fil = c2.text_input("Filiação", value=d[20])
        obs = st.text_area("Observação", value=d[21])

        if st.form_submit_button("Salvar no TMS"):
            st.success("Pronto para salvar.")

import streamlit as st
import requests
import re
import datetime

# Tenta importar bibliotecas críticas
try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    LIB_OK = True
except ImportError:
    LIB_OK = False

st.set_page_config(page_title="TMS FRANCAL - Sistema", layout="wide")

# Sidebar
with st.sidebar:
    st.title("TMS FRANCAL")
    pagina = st.radio("Navegação", ["Cadastro de Motorista", "Consulta/Auditoria"])

if not LIB_OK:
    st.error("Erro: As bibliotecas necessárias (gspread, oauth2client) não foram instaladas. Verifique seu arquivo requirements.txt no GitHub.")
    st.stop()

# Configuração de Conexão
def get_sheet():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg").worksheet("REGISTRO_OPERACIONAL")

# Lógica
if pagina == "Cadastro de Motorista":
    st.header("👤 Cadastro de Motorista")
    with st.form("form_motorista", clear_on_submit=True):
        cpf_input = st.text_input("CPF (Apenas números)", placeholder="00000000000")
        nome = st.text_input("Nome Completo")
        c1, c2 = st.columns(2)
        with c1:
            tel = st.text_input("Telefone Comercial")
        with c2:
            data_nasc = st.date_input("Data de Nascimento", min_value=datetime.date(1930, 1, 1))
        
        st.subheader("🏠 Endereço")
        cep = st.text_input("CEP")
        logradouro = st.text_input("Logradouro")
        cidade = st.text_input("Cidade")
        
        st.subheader("💳 Habilitação e Banco")
        cnh = st.text_input("Número da CNH")
        banco = st.text_input("Banco (Número e Nome)")
        conta = st.text_input("Conta (Ex: 1010101-01)")
        
        submit = st.form_submit_button("Salvar no TMS")

    if submit:
        try:
            sheet = get_sheet()
            sheet.append_row([nome, cpf_input, tel, str(data_nasc), cep, logradouro, cidade, cnh, banco, conta])
            st.success("Motorista cadastrado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")

elif pagina == "Consulta/Auditoria":
    st.header("🔍 Auditoria")
    if st.button("Carregar Dados"):
        try:
            sheet = get_sheet()
            st.table(sheet.get_all_values())
        except Exception as e:
            st.error(f"Erro na conexão: {e}")

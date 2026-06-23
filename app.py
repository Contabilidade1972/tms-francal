import streamlit as st
import requests
import re
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="TMS FRANCAL - Cadastro Motorista", layout="wide")

# Configuração da Conexão
def get_sheet():
    # Carrega as credenciais do Secrets
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg").worksheet("REGISTRO_OPERACIONAL")

with st.sidebar:
    st.title("TMS FRANCAL")
    menu = st.radio("Navegação", ["Cadastro de Motorista", "Consulta/Auditoria"])

if menu == "Cadastro de Motorista":
    st.header("👤 Cadastro Completo de Motorista")
    
    with st.form("form_completo", clear_on_submit=True):
        st.subheader("Dados Pessoais")
        cpf = st.text_input("CPF (XXX.XXX.XXX-XX)")
        nome = st.text_input("Nome Completo")
        c1, c2 = st.columns(2)
        with c1:
            tel = st.text_input("Telefone Comercial (XX)XXXXX-XXXX")
        with c2:
            data_nasc = st.date_input("Data de Nascimento", min_value=datetime.date(1930, 1, 1), format="DD/MM/YYYY")

        st.subheader("Endereço")
        cep = st.text_input("CEP")
        logradouro = st.text_input("Logradouro")
        cidade = st.text_input("Cidade")
        bairro = st.text_input("Bairro")
        num_comp = st.text_input("Número e Complemento")

        st.subheader("Habilitação e Banco")
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            uf_cnh = st.selectbox("UF/CNH", ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
            data_emissao = st.date_input("Data de Emissão CNH", format="DD/MM/YYYY")
            venc_cnh = st.date_input("Vencimento CNH", format="DD/MM/YYYY")
        with col_h2:
            banco = st.text_input("Banco (Número e Nome)")
            conta = st.text_input("Conta (Ex: 1010101-01)")

        submit = st.form_submit_button("Salvar no TMS")

    if submit:
        try:
            sheet = get_sheet()
            sheet.append_row([nome, cpf, tel, str(data_nasc), cep, logradouro, cidade, bairro, num_comp, uf_cnh, str(data_emissao), str(venc_cnh), banco, conta])
            st.success("Cadastro realizado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")

elif menu == "Consulta/Auditoria":
    st.header("🔍 Auditoria de Dados")
    if st.button("Carregar Base"):
        try:
            sheet = get_sheet()
            data = sheet.get_all_values()
            st.table(data)
        except Exception as e:
            st.error(f"Erro: {e}")

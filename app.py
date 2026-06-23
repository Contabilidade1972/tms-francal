import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

st.set_page_config(page_title="TMS FRANCAL - Cadastro Profissional", layout="wide")

# Função de Conexão Blindada
def get_sheet():
    # Carrega o dicionário do secrets
    creds_dict = st.secrets["gcp_service_account"]
    
    # Criamos o objeto de credenciais de forma direta
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    
    client = gspread.authorize(creds)
    return client.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg").worksheet("REGISTRO_OPERACIONAL")

st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.radio("Navegação", ["Cadastro de Motorista", "Consulta/Auditoria"])

if menu == "Cadastro de Motorista":
    st.header("👤 Cadastro de Motorista")
    
    # Formulário de Busca
    cpf_search = st.text_input("CPF para busca")
    if st.button("Buscar CPF"):
        try:
            sheet = get_sheet()
            data = sheet.get_all_values()
            found = False
            for row in data:
                # Ajuste o índice [10] para a coluna correta do seu CPF na planilha
                if row[10].strip() == cpf_search.strip():
                    st.session_state.motorista_data = row
                    st.success("Dados encontrados!")
                    found = True
                    break
            if not found:
                st.warning("CPF não encontrado.")
        except Exception as e:
            st.error(f"Erro na conexão: {e}")

    # Exibição dos dados (se houver)
    d = st.session_state.get('motorista_data', [""] * 23)
    
    with st.form("form_tms"):
        nome = st.text_input("Nome Completo", value=d[0])
        col1, col2 = st.columns(2)
        tel = col1.text_input("Telefone", value=d[1])
        data_nasc = col2.text_input("Data Nascimento/Emissão", value=d[7])
        
        # ... (Restante dos 23 campos mantendo a estrutura d[0] a d[22])
        cpf = st.text_input("CPF", value=d[10] if d[10] else cpf_search)
        
        submit = st.form_submit_button("Salvar no TMS")
        if submit:
            st.info("Funcionalidade de salvar ativada.")

elif menu == "Consulta/Auditoria":
    if st.button("Carregar Tabela"):
        try:
            st.table(get_sheet().get_all_values())
        except Exception as e:
            st.error(f"Erro: {e}")

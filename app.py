import streamlit as st
import requests
import re
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuração da Página
st.set_page_config(page_title="TMS FRANCAL - Cadastro Motorista", layout="wide")

# Configuração de Conexão com Google Sheets
def get_sheet():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg").worksheet("REGISTRO_OPERACIONAL")

# Sidebar de Navegação
with st.sidebar:
    st.title("TMS FRANCAL")
    st.markdown("---")
    pagina = st.radio("Menu", ["Cadastro de Motorista", "Consulta/Auditoria"])
    st.markdown("---")
    st.write(f"Usuário: Luciano Sacramento")

# Lógica de interface
if pagina == "Cadastro de Motorista":
    st.header("👤 Cadastro de Motorista")
    
    with st.form("form_motorista", clear_on_submit=True):
        # Busca de CPF
        cpf_input = st.text_input("Consultar CPF (Apenas números)", placeholder="Digite o CPF para buscar existência")
        
        c1, c2 = st.columns(2)
        with c1:
            nome = st.text_input("Nome Completo")
            tel = st.text_input("Telefone Comercial")
        with c2:
            data_nasc = st.date_input("Data de Nascimento", min_value=datetime.date(1930, 1, 1))
            email = st.text_input("E-mail")

        st.subheader("🏠 Endereço")
        cep = st.text_input("CEP")
        c_end1, c_end2 = st.columns(2)
        with c_end1:
            logradouro = st.text_input("Logradouro")
            cidade = st.text_input("Cidade")
        with c_end2:
            bairro = st.text_input("Bairro")
            num = st.text_input("Número")
        
        st.subheader("💳 Habilitação e Banco")
        c_hab1, c_hab2 = st.columns(2)
        with c_hab1:
            cnh = st.text_input("Número da CNH")
            uf_cnh = st.selectbox("UF/CNH", ["MG", "SP", "RJ", "ES", "RS", "PR", "SC", "BA", "PE", "CE", "AM", "DF", "GO", "MT", "MS", "PA", "RN", "MA", "PB", "AL", "SE", "PI", "TO", "RO", "AC", "AP", "RR"])
            venc_cnh = st.date_input("Vencimento CNH")
        with c_hab2:
            banco = st.text_input("Banco (Número e Nome)")
            agencia = st.text_input("Agência")
            conta = st.text_input("Conta (Ex: 1010101-01)")

        submit = st.form_submit_button("Salvar e Cadastrar no TMS")

    if submit:
        try:
            sheet = get_sheet()
            # Validação simples de duplicidade na planilha
            lista_cpfs = sheet.col_values(2) # Supondo que CPF esteja na coluna 2
            if cpf_input in lista_cpfs:
                st.error("ERRO: Este CPF já está cadastrado no sistema!")
            else:
                sheet.append_row([nome, cpf_input, tel, str(data_nasc), email, cep, logradouro, num, bairro, cidade, cnh, uf_cnh, str(venc_cnh), banco, agencia, conta])
                st.success("Motorista cadastrado com sucesso!")
        except Exception as e:
            st.error(f"Falha na conexão: {e}")

elif pagina == "Consulta/Auditoria":
    st.header("🔍 Consulta de Motoristas")
    if st.button("Carregar Base de Dados"):
        try:
            sheet = get_sheet()
            dados = sheet.get_all_values()
            st.dataframe(dados)
        except:
            st.error("Erro ao acessar a planilha.")

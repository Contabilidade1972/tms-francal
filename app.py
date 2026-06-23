import streamlit as st
import requests
import re
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuração da Página
st.set_page_config(page_title="TMS FRANCAL - Sistema de Gestão", layout="wide")

# Função de Conexão com Google Sheets
def get_sheet():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg").worksheet("REGISTRO_OPERACIONAL")

# Sidebar
with st.sidebar:
    st.title("TMS FRANCAL")
    menu = st.radio("Navegação", ["Cadastro de Motorista", "Consulta/Auditoria"])

# Lógica de Cadastro
if menu == "Cadastro de Motorista":
    st.header("👤 Cadastro Completo de Motorista")
    
    with st.form("form_motorista", clear_on_submit=False):
        # CPF com busca
        cpf = st.text_input("CPF (XXX.XXX.XXX-XX)")
        nome = st.text_input("Nome Completo")
        
        col1, col2 = st.columns(2)
        with col1:
            tel = st.text_input("Telefone Comercial (XX)XXXXX-XXXX")
        with col2:
            data_nasc = st.date_input("Data de Nascimento", min_value=datetime.date(1930, 1, 1))

        st.subheader("🏠 Endereço")
        cep = st.text_input("CEP")
        
        # Lógica ViaCEP
        logradouro, bairro, cidade = "", "", ""
        if cep and len(re.sub(r'\D', '', cep)) == 8:
            try:
                res = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()
                if "erro" not in res:
                    logradouro = res.get('logradouro', '')
                    bairro = res.get('bairro', '')
                    cidade = res.get('localidade', '')
            except: st.warning("Erro ao buscar CEP")
        
        c_end1, c_end2 = st.columns(2)
        with c_end1:
            logradouro = st.text_input("Logradouro", value=logradouro)
            cidade = st.text_input("Cidade", value=cidade)
        with c_end2:
            bairro = st.text_input("Bairro", value=bairro)
            num_comp = st.text_input("Número e Complemento")

        st.subheader("💳 Habilitação e Banco")
        c_hab1, c_hab2 = st.columns(2)
        with c_hab1:
            uf_cnh = st.selectbox("UF/CNH", ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"], index=12)
            data_emissao = st.date_input("Data de Emissão CNH")
            venc_cnh = st.date_input("Vencimento CNH")
        with c_hab2:
            bancos_lista = ["001 - BANCO DO BRASIL", "104 - CAIXA ECONOMICA", "341 - ITAU", "033 - SANTANDER", "237 - BRADESCO"]
            banco = st.selectbox("Banco", bancos_lista)
            conta = st.text_input("Conta (Ex: 1010101-01)")

        submit = st.form_submit_button("Salvar Motorista no TMS")

    if submit:
        try:
            sheet = get_sheet()
            # Validação de duplicidade pelo CPF
            if cpf in sheet.col_values(2): # Assumindo coluna 2
                st.error("ERRO: Motorista já cadastrado com este CPF!")
            else:
                sheet.append_row([nome, cpf, tel, str(data_nasc), cep, logradouro, cidade, bairro, num_comp, uf_cnh, str(data_emissao), str(venc_cnh), banco, conta])
                st.success("Motorista cadastrado com sucesso no TMS FRANCAL!")
        except Exception as e:
            st.error(f"Erro ao conectar ao banco de dados: {e}")

elif menu == "Consulta/Auditoria":
    st.header("🔍 Auditoria de Motoristas")
    if st.button("Carregar Registros"):
        try:
            sheet = get_sheet()
            data = sheet.get_all_values()
            st.table(data)
        except Exception as e:
            st.error(f"Erro ao buscar registros: {e}")

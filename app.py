import streamlit as st
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

st.set_page_config(page_title="TMS FRANCAL - Cadastro Profissional", layout="wide")

# Configuração de Conexão
def get_sheet():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg").worksheet("REGISTRO_OPERACIONAL")

# Variáveis Globais
ufs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.radio("Navegação", ["Cadastro de Motorista", "Consulta/Auditoria"])

if menu == "Cadastro de Motorista":
    st.header("👤 Cadastro de Motorista")
    
    # Inicializa campos de sessão
    if 'dados_motorista' not in st.session_state:
        st.session_state.dados_motorista = {}

    with st.form("form_tms", clear_on_submit=False):
        col_c1, col_c2 = st.columns([2, 1])
        with col_c1:
            cpf_pesquisa = st.text_input("CPF (Para busca/edição)", key="cpf_search")
        with col_c2:
            btn_buscar = st.form_submit_button("Buscar CPF")

        # Se buscar, preenche campos
        if btn_buscar:
            try:
                sheet = get_sheet()
                dados = sheet.get_all_values()
                for row in dados:
                    if row[10] == cpf_pesquisa: # Coluna K (índice 10) = CPF
                        st.session_state.dados_motorista = {"nome": row[0], "tel": row[1], "cep": row[2]} # ... Mapear todos
                        st.success("Dados encontrados!")
            except: st.error("Erro na busca.")

        # Campos do Formulário (A até W)
        st.subheader("Dados Pessoais")
        nome = st.text_input("Nome", value=st.session_state.dados_motorista.get('nome', ''))
        col1, col2 = st.columns(2)
        with col1:
            tel = st.text_input("Telefone Comercial")
            cpf = st.text_input("CPF", value=cpf_pesquisa)
            rg = st.text_input("RG")
        with col2:
            data_nasc = st.date_input("Data de Nascimento/Emissão")
            filia = st.text_input("Filiação")
            obs = st.text_area("Observação")

        st.subheader("Endereço")
        cep = st.text_input("CEP")
        col3, col4 = st.columns(2)
        with col3:
            logra = st.text_input("Logradouro")
            bairro = st.text_input("Bairro")
        with col4:
            num = st.text_input("Número")
            compl = st.text_input("Complemento")
            muni = st.text_input("Município")
            uf = st.selectbox("UF", ufs, index=12)

        st.subheader("Habilitação e Dados Bancários")
        col5, col6 = st.columns(2)
        with col5:
            cnh = st.text_input("CNH")
            uf_cnh = st.selectbox("UF/CNH", ufs)
            rntrc = st.text_input("RNTRC")
            cat_cnh = st.text_input("Categoria CNH")
        with col6:
            banco = st.text_input("Banco")
            agencia = st.text_input("Agência")
            conta = st.text_input("Conta")
            venc_cnh = st.date_input("Vencimento CNH")

        submit_final = st.form_submit_button("Salvar Registro")

    if submit_final:
        sheet = get_sheet()
        # Salva todos os 23 campos (A a W)
        sheet.append_row([nome, tel, cep, logra, num, compl, bairro, muni, uf, rg, cpf, cnh, uf_cnh, rntrc, banco, agencia, conta, str(data_nasc), str(venc_cnh), cat_cnh, filia, obs, ""])
        st.success("Dados salvos com sucesso!")

elif menu == "Consulta/Auditoria":
    st.header("🔍 Auditoria")
    if st.button("Carregar Dados"):
        st.table(get_sheet().get_all_values())

import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="TMS FRANCAL - Gestão", layout="wide")

def get_sheet():
    # Carrega o JSON que está no Secrets
    info = json.loads(st.secrets["gcp_json"])
    # Limpa quebras de linha para evitar erro de PEM
    info['private_key'] = info['private_key'].replace('\\n', '\n')
    
    scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    client = gspread.authorize(creds)
    # Abre a planilha pelo ID
    return client.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg").worksheet("REGISTRO_OPERACIONAL")

st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.radio("Navegação", ["Cadastro de Motorista", "Consulta/Auditoria"])

if 'data' not in st.session_state:
    st.session_state.data = [""] * 23

if menu == "Cadastro de Motorista":
    st.header("👤 Cadastro Completo de Motorista")
    
    with st.form("form_tms", clear_on_submit=False):
        c1, c2 = st.columns([4, 1])
        cpf_busca = c1.text_input("CPF para busca")
        if c2.form_submit_button("Buscar CPF"):
            try:
                sheet = get_sheet()
                dados = sheet.get_all_values()
                encontrado = False
                for row in dados:
                    # Verifica coluna K (índice 10)
                    if len(row) > 10 and row[10] == cpf_busca:
                        st.session_state.data = row
                        st.success("Dados carregados!")
                        encontrado = True
                        break
                if not encontrado:
                    st.warning("Motorista não encontrado.")
            except Exception as e:
                st.error(f"DETALHE DO ERRO: {e}")

        d = st.session_state.data
        
        # Mapeamento completo dos 23 campos (A até W)
        col1, col2, col3 = st.columns(3)
        nome = col1.text_input("Nome", value=d[0])
        tel = col2.text_input("Telefone Comercial", value=d[1])
        cep = col3.text_input("CEP", value=d[2])
        logra = col1.text_input("Logradouro", value=d[3])
        num = col2.text_input("Número", value=d[4])
        compl = col3.text_input("Complemento", value=d[5])
        bairro = col1.text_input("Bairro", value=d[6])
        muni = col2.text_input("Município", value=d[7])
        uf = col3.text_input("UF", value=d[8])
        rg = col1.text_input("RG", value=d[9])
        cpf = col2.text_input("CPF", value=d[10])
        cnh = col3.text_input("CNH", value=d[11])
        ufcnh = col1.text_input("UF/CNH", value=d[12])
        rntrc = col2.text_input("RNTRC", value=d[13])
        banco = col3.text_input("Banco", value=d[14])
        agencia = col1.text_input("Agência", value=d[15])
        conta = col2.text_input("Conta", value=d[16])
        nasc = col2.text_input("Data Nasc/Emissão", value=d[17])
        venc = col3.text_input("Venc CNH", value=d[18])
        cat = col1.text_input("Categoria", value=d[19])
        fil = col2.text_input("Filiação", value=d[20])
        obs = st.text_area("Observação", value=d[21])

        if st.form_submit_button("Salvar no TMS"):
            try:
                sheet = get_sheet()
                nova_linha = [nome, tel, cep, logra, num, compl, bairro, muni, uf, rg, cpf, cnh, ufcnh, rntrc, banco, agencia, conta, nasc, venc, cat, fil, obs, ""]
                sheet.append_row(nova_linha)
                st.success("Dados salvos com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

elif menu == "Consulta/Auditoria":
    st.header("🔍 Auditoria")
    if st.button("Carregar Dados"):
        try:
            st.table(get_sheet().get_all_values())
        except Exception as e:
            st.error(f"Erro: {e}")

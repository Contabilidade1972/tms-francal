import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

st.set_page_config(page_title="TMS FRANCAL - Cadastro Profissional", layout="wide")

def get_sheet():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg").worksheet("REGISTRO_OPERACIONAL")

# Inicializa sessão para manter dados
if 'motorista_data' not in st.session_state:
    st.session_state.motorista_data = None

st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.radio("Navegação", ["Cadastro de Motorista", "Consulta/Auditoria"])

if menu == "Cadastro de Motorista":
    st.header("👤 Cadastro de Motorista")
    
    with st.form("form_tms"):
        c1, c2 = st.columns([4, 1])
        with c1:
            cpf_search = st.text_input("CPF (Para buscar/editar)", key="cpf_input")
        with c2:
            btn_buscar = st.form_submit_button("Buscar CPF")

        if btn_buscar:
            try:
                sheet = get_sheet()
                all_data = sheet.get_all_values()
                # Procura o CPF na coluna K (índice 10)
                encontrado = False
                for row in all_data:
                    if row[10].strip() == cpf_search.strip():
                        st.session_state.motorista_data = row
                        encontrado = True
                        st.success("Dados carregados com sucesso!")
                        break
                if not encontrado:
                    st.warning("CPF não encontrado. Preencha os dados para um novo cadastro.")
                    st.session_state.motorista_data = None
            except Exception as e:
                st.error(f"Erro na busca: {e}")

        # Preenche os campos (se houver dados na sessão)
        d = st.session_state.motorista_data or [""] * 23
        
        nome = st.text_input("Nome Completo", value=d[0])
        col_tel, col_data = st.columns(2)
        tel = col_tel.text_input("Telefone Comercial", value=d[1])
        data_nasc = col_data.text_input("Data de Nascimento/Emissão", value=d[7])
        
        cpf = st.text_input("CPF", value=d[10] if d[10] else cpf_search)
        filia = st.text_input("Filiação", value=d[20])
        rg = st.text_input("RG", value=d[9])
        obs = st.text_area("Observação", value=d[21])

        st.subheader("Endereço")
        col_e1, col_e2 = st.columns(2)
        cep = col_e1.text_input("CEP", value=d[2])
        logra = col_e2.text_input("Logradouro", value=d[3])
        num = col_e1.text_input("Número", value=d[4])
        compl = col_e2.text_input("Complemento", value=d[5])
        bairro = col_e1.text_input("Bairro", value=d[6])
        muni = col_e2.text_input("Município", value=d[7])
        uf = st.selectbox("UF", ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"], index=10)

        st.subheader("Habilitação e Banco")
        col_h1, col_h2 = st.columns(2)
        cnh = col_h1.text_input("CNH", value=d[11])
        uf_cnh = col_h2.text_input("UF/CNH", value=d[12])
        rntrc = col_h1.text_input("RNTRC", value=d[13])
        cat_cnh = col_h2.text_input("Categoria CNH", value=d[19])
        banco = col_h1.text_input("Banco", value=d[14])
        agencia = col_h2.text_input("Agência", value=d[15])
        conta = col_h1.text_input("Conta", value=d[16])
        venc_cnh = col_h2.text_input("Vencimento CNH", value=d[18])

        submit_salvar = st.form_submit_button("Salvar Registro")

    if submit_salvar:
        try:
            sheet = get_sheet()
            novo_dado = [nome, tel, cep, logra, num, compl, bairro, muni, uf, rg, cpf, cnh, uf_cnh, rntrc, banco, agencia, conta, "", venc_cnh, cat_cnh, filia, obs, ""]
            sheet.append_row(novo_dado)
            st.success("Dados salvos com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")

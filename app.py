import streamlit as st
import pandas as pd

st.set_page_config(page_title="TMS FRANCAL", layout="wide")

# Link da sua planilha publicada como CSV
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-k3doFN8BGK5YL9su9avmaFLgV97SbE3erJdh0YDJxACO3nNrYX6XTO0a7rhRtUN9xcdeIsLWurAr/pub?gid=1127537998&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.radio("Navegação", ["Cadastro de Motorista", "Consulta/Auditoria"])

if menu == "Cadastro de Motorista":
    st.header("👤 Cadastro de Motorista")
    
    with st.form("form_tms"):
        cpf_busca = st.text_input("CPF para busca")
        if st.form_submit_button("Buscar"):
            try:
                df = load_data()
                # Coluna CPF é a 11ª (índice 10)
                resultado = df[df.iloc[:, 10].astype(str) == cpf_busca]
                if not resultado.empty:
                    st.session_state.dados = resultado.iloc[0].tolist()
                    st.success("Dados encontrados!")
                else:
                    st.warning("Motorista não encontrado.")
            except Exception as e:
                st.error(f"Erro na carga: {e}")

        d = st.session_state.get('dados', [""] * 23)
        
        # Grid Profissional
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
        nasc = c2.text_input("Data Nasc", value=d[17])
        venc = c3.text_input("Venc CNH", value=d[18])
        cat = c1.text_input("Categoria", value=d[19])
        fil = c2.text_input("Filiação", value=d[20])
        obs = st.text_area("Observação", value=d[21])

        st.form_submit_button("Salvar")

elif menu == "Consulta/Auditoria":
    st.table(load_data())

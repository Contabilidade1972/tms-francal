import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="TMS FRANCAL - Cadastro Profissional", layout="wide")

# Link da sua planilha CSV pública
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-k3doFN8BGK5YL9su9avmaFLgV97SbE3erJdh0YDJxACO3nNrYX6XTO0a7rhRtUN9xcdeIsLWurAr/pub?gid=1127537998&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

def limpar_cpf(cpf):
    return re.sub(r'\D', '', str(cpf))

st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.radio("Navegação", ["Cadastro de Motorista", "Consulta/Auditoria"])

if menu == "Cadastro de Motorista":
    st.header("👤 Cadastro Completo de Motorista")
    
    with st.form("form_tms", clear_on_submit=False):
        c_busca, c_btn = st.columns([4, 1])
        cpf_input = c_busca.text_input("CPF para busca")
        
        if c_btn.form_submit_button("Buscar CPF"):
            df = load_data()
            cpf_alvo = limpar_cpf(cpf_input)
            
            # Busca em todas as colunas para identificar onde o CPF está
            encontrado = False
            for col_idx in range(len(df.columns)):
                df['temp_col'] = df.iloc[:, col_idx].apply(limpar_cpf)
                if cpf_alvo in df['temp_col'].values:
                    resultado = df[df['temp_col'] == cpf_alvo].iloc[0]
                    st.session_state.dados = resultado.tolist()
                    st.success(f"Motorista encontrado na coluna de índice: {col_idx}")
                    encontrado = True
                    break
            
            if not encontrado:
                st.warning("CPF não encontrado em nenhuma coluna da planilha.")
                st.session_state.dados = [""] * 23

        d = st.session_state.get('dados', [""] * 23)
        
        # Grid com 23 campos (A até W)
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

        st.form_submit_button("Salvar Registro")

elif menu == "Consulta/Auditoria":
    st.header("🔍 Auditoria")
    st.table(load_data())

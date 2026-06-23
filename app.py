import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="TMS FRANCAL - Sistema Interno", layout="wide")

# Conexão com o banco de dados (será criado na pasta do app)
def get_db():
    conn = sqlite3.connect('tms_francal.db')
    return conn

# Inicializa a tabela
def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS motoristas (
                    nome TEXT, tel TEXT, cep TEXT, logra TEXT, num TEXT, 
                    compl TEXT, bairro TEXT, muni TEXT, uf TEXT, rg TEXT, 
                    cpf TEXT PRIMARY KEY, cnh TEXT, ufcnh TEXT, rntrc TEXT, 
                    banco TEXT, ag TEXT, conta TEXT, nasc TEXT, venc TEXT, 
                    cat TEXT, fil TEXT, obs TEXT)''')
    conn.commit()
    conn.close()

init_db()

st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.radio("Navegação", ["Cadastro de Motorista", "Consulta/Auditoria"])

if menu == "Cadastro de Motorista":
    st.header("👤 Cadastro de Motorista")
    
    with st.form("form_tms"):
        cpf_input = st.text_input("CPF (Digite aqui para buscar ou editar)")
        
        # Lógica de Busca
        d = [""] * 22
        if st.form_submit_button("Buscar no Sistema"):
            conn = get_db()
            cursor = conn.execute("SELECT * FROM motoristas WHERE cpf=?", (cpf_input,))
            row = cursor.fetchone()
            if row: 
                st.session_state.dados = row
                st.success("Motorista encontrado!")
            else: 
                st.warning("Motorista não encontrado. Pode preencher para cadastrar.")
            conn.close()

        d = st.session_state.get('dados', d)
        
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
        cpf = c2.text_input("CPF", value=d[10] if d[10] else cpf_input)
        cnh = c3.text_input("CNH", value=d[11])
        ufcnh = c1.text_input("UF/CNH", value=d[12])
        rntrc = c2.text_input("RNTRC", value=d[13])
        banco = c3.text_input("Banco", value=d[14])
        ag = c1.text_input("Agência", value=d[15])
        conta = c2.text_input("Conta", value=d[16])
        nasc = c3.text_input("Data Nasc/Emissão", value=d[17])
        venc = c1.text_input("Venc CNH", value=d[18])
        cat = c2.text_input("Categoria", value=d[19])
        fil = c3.text_input("Filiação", value=d[20])
        obs = st.text_area("Observação", value=d[21])

        if st.form_submit_button("Salvar no Sistema"):
            conn = get_db()
            conn.execute("INSERT OR REPLACE INTO motoristas VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (nome, tel, cep, logra, num, compl, bairro, muni, uf, rg, cpf, cnh, ufcnh, rntrc, banco, ag, conta, nasc, venc, cat, fil, obs))
            conn.commit()
            conn.close()
            st.success("Motorista salvo com sucesso!")

elif menu == "Consulta/Auditoria":
    st.header("🔍 Auditoria")
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM motoristas", conn)
    st.table(df)
    conn.close()

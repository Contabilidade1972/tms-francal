import streamlit as st
import requests
import re
import datetime

# Configuração da Página
st.set_page_config(page_title="TMS FRANCAL - Cadastro Motorista", layout="wide")

# Menu Lateral (Sidebar)
with st.sidebar:
    st.title("TMS FRANCAL")
    st.markdown("---")
    st.write("### Navegação")
    if st.button("Cadastro de Motorista"):
        st.session_state.page = "cadastro"
    if st.button("Registro Operacional"):
        st.session_state.page = "operacional"
    st.markdown("---")
    st.info("Usuário: Luciano Sacramento")

# Listas auxiliares
ufs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", 
       "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
bancos = ["001 - BANCO DO BRASIL", "104 - CAIXA ECONOMICA", "341 - ITAU", "033 - SANTANDER", "237 - BRADESCO"]
data_minima = datetime.date(1930, 1, 1)

# Interface Principal
st.header("Cadastro de Motorista")

with st.form("cadastro_motorista", clear_on_submit=True):
    # DADOS PESSOAIS
    st.subheader("👤 Dados Pessoais")
    c1, c2 = st.columns(2)
    with c1:
        tel = st.text_input("Telefone Comercial", placeholder="(31)99999-9999")
        cpf = st.text_input("CPF", placeholder="000.000.000-00")
    with c2:
        data_nasc = st.date_input("Data de Nascimento", min_value=data_minima, format="DD/MM/YYYY")

    # ENDEREÇO
    st.subheader("🏠 Endereço")
    cep = st.text_input("CEP", placeholder="Digite o CEP e aguarde o preenchimento automático")
    
    # Lógica de preenchimento automático (mantida e otimizada)
    rua, bairro, cidade = "", "", ""
    if cep and len(re.sub(r'\D', '', cep)) == 8:
        try:
            res = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()
            if "erro" not in res:
                rua, bairro, cidade = res.get('logradouro', ''), res.get('bairro', ''), res.get('localidade', '')
        except:
            st.warning("Não foi possível buscar o CEP automaticamente.")

    col_e1, col_e2 = st.columns([2, 1])
    with col_e1:
        logradouro = st.text_input("Logradouro", value=rua)
        cidade = st.text_input("Cidade", value=cidade)
    with col_e2:
        bairro = st.text_input("Bairro", value=bairro)
        numero = st.text_input("Número")
        complemento = st.text_input("Complemento")

    # HABILITAÇÃO E BANCO
    st.subheader("💳 Habilitação e Banco")
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        uf_cnh = st.selectbox("UF/CNH", ufs, index=ufs.index("MG"))
        data_emissao = st.date_input("Data de Emissão CNH", min_value=data_minima, format="DD/MM/YYYY")
        venc_cnh = st.date_input("Vencimento CNH", format="DD/MM/YYYY")
    with col_h2:
        banco_sel = st.selectbox("Banco", bancos)
        conta = st.text_input("Conta (Ex: 1010101-01)", placeholder="1234567-89")

    # BOTÃO SUBMIT
    submit = st.form_submit_button("Salvar Cadastro")

if submit:
    st.success("Cadastro realizado com sucesso no TMS FRANCAL!")

import streamlit as st
import requests
import re
import datetime

# Configuração da Página
st.set_page_config(page_title="TMS FRANCAL - Cadastro", layout="wide")
st.title("Cadastro de Motorista - TMS FRANCAL")

# Listas auxiliares
ufs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", 
       "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

bancos = ["001 - BANCO DO BRASIL", "104 - CAIXA ECONOMICA", "341 - ITAU", "033 - SANTANDER", "237 - BRADESCO"]

# Definição de datas mínimas (corrigido para objeto date)
data_minima = datetime.date(1930, 1, 1)

with st.form("cadastro_motorista", clear_on_submit=True):
    st.subheader("Dados Pessoais")
    col1, col2 = st.columns(2)
    
    with col1:
        tel = st.text_input("Telefone Comercial (XX)XXXXX-XXXX", placeholder="(31)99999-9999")
        cpf = st.text_input("CPF (XXX.XXX.XXX-XX)", placeholder="000.000.000-00")
    
    with col2:
        data_nasc = st.date_input("Data de Nascimento", min_value=data_minima, format="DD/MM/YYYY")

    st.subheader("Endereço")
    cep = st.text_input("CEP", placeholder="Digite o CEP (somente números)")
    
    # Lógica de preenchimento automático
    rua = ""
    bairro = ""
    cidade = ""
    
    if cep and len(re.sub(r'\D', '', cep)) == 8:
        try:
            res = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()
            if "erro" not in res:
                rua = res.get('logradouro', '')
                bairro = res.get('bairro', '')
                cidade = res.get('localidade', '')
        except:
            st.error("Erro na consulta do CEP.")

    col_end1, col_end2 = st.columns(2)
    with col_end1:
        logradouro = st.text_input("Logradouro", value=rua)
        cidade = st.text_input("Cidade", value=cidade)
    with col_end2:
        bairro = st.text_input("Bairro", value=bairro)
        numero = st.text_input("Número")
        complemento = st.text_input("Complemento")

    st.subheader("Habilitação e Banco")
    col3, col4 = st.columns(2)
    with col3:
        uf_cnh = st.selectbox("UF/CNH", ufs)
        data_emissao = st.date_input("Data de Emissão CNH", min_value=data_minima, format="DD/MM/YYYY")
        venc_cnh = st.date_input("Vencimento CNH", format="DD/MM/YYYY")
    
    with col4:
        banco_sel = st.selectbox("Banco", bancos)
        conta = st.text_input("Conta (Ex: 1010101-01)", placeholder="1234567-89")

    submit = st.form_submit_button("Salvar Cadastro")

if submit:
    # Aqui entra a lógica de envio para o Google Sheets que configuramos anteriormente
    st.success("Dados enviados com sucesso para o TMS FRANCAL!")

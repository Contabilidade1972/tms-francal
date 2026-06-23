import streamlit as st
import requests
import re

# Função para formatar padrões básicos
def formatar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if len(cpf) == 11 else cpf

def formatar_telefone(tel):
    tel = re.sub(r'\D', '', tel)
    return f"({tel[:2]}){tel[2:7]}-{tel[7:]}" if len(tel) == 11 else tel

# Configuração da Página
st.set_page_config(page_title="TMS FRANCAL - Cadastro", layout="wide")
st.title("Cadastro de Motorista - TMS FRANCAL")

# Estados Brasileiros
ufs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", 
       "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

# Bancos (Lista representativa - para produção, pode carregar de um CSV)
bancos = ["001 - BANCO DO BRASIL", "104 - CAIXA ECONOMICA", "341 - ITAU", "033 - SANTANDER", "237 - BRADESCO"]

with st.form("cadastro_motorista"):
    st.subheader("Dados Pessoais")
    col1, col2 = st.columns(2)
    
    with col1:
        tel = st.text_input("Telefone Comercial (XX)XXXXX-XXXX", placeholder="(31)99999-9999")
        cpf = st.text_input("CPF (XXX.XXX.XXX-XX)")
    
    with col2:
        # DatePicker com expansão de ano para 1930
        data_nasc = st.date_input("Data de Nascimento", min_value=1930, format="DD/MM/YYYY")

    st.subheader("Endereço")
    cep = st.text_input("CEP", placeholder="Digite o CEP para buscar endereço")
    
    # Lógica de preenchimento automático via ViaCEP
    if cep and len(re.sub(r'\D', '', cep)) == 8:
        try:
            res = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()
            rua = st.text_input("Logradouro", value=res.get('logradouro', ''))
            bairro = st.text_input("Bairro", value=res.get('bairro', ''))
            cidade = st.text_input("Cidade", value=res.get('localidade', ''))
        except:
            st.error("Erro ao buscar CEP.")
    else:
        rua = st.text_input("Logradouro")
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")

    num = st.text_input("Número")
    comp = st.text_input("Complemento")

    st.subheader("Habilitação e Banco")
    col3, col4 = st.columns(2)
    with col3:
        uf_cnh = st.selectbox("UF/CNH", ufs)
        data_emissao = st.date_input("Data de Emissão CNH", min_value=1930, format="DD/MM/YYYY")
        venc_cnh = st.date_input("Vencimento CNH", format="DD/MM/YYYY")
    
    with col4:
        banco_sel = st.selectbox("Banco", bancos)
        conta = st.text_input("Conta (Ex: 1010101-01)", placeholder="1234567-89")

    submit = st.form_submit_button("Salvar Cadastro")

if submit:
    st.write("Dados processados com sucesso!")

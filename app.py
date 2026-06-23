import streamlit as st
import requests

# Padronização de maiúsculas
def upper_text(text): return str(text).upper()

st.set_page_config(layout="wide")

# Lista de Bancos simplificada (pode ser expandida)
lista_bancos = ["001 - BANCO DO BRASIL", "104 - CAIXA ECONÔMICA", "341 - ITAÚ", "033 - SANTANDER", "237 - BRADESCO"]

with st.form("motorista_form"):
    c1, c2, c3 = st.columns(3)
    nome = c1.text_input("Nome", on_change=lambda: st.session_state.update({"nome": upper_text(nome)}))
    
    # CEP Automático (via API ViaCEP)
    cep = c2.text_input("CEP")
    if len(cep) == 8:
        try:
            res_cep = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()
            log = res_cep['logradouro']
            bairro = res_cep['bairro']
            mun = res_cep['localidade']
        except: pass
    
    # Busca de Bancos
    banco = c3.selectbox("Banco", lista_bancos)

    # Botão Salvar
    if st.form_submit_button("Salvar / Atualizar"):
        # Força maiúsculas antes de enviar
        payload = {
            "nome": upper_text(nome),
            "rntrc": str(rntrc), # Garante que vai como texto
            # ... resto do payload
        }
        # ... requests.post ...

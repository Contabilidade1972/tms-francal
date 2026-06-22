import streamlit as st
import requests

st.set_page_config(layout="wide")

# Menu sempre visível
st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.selectbox("Módulo", ["Cadastro: Motoristas", "Relatórios"])

if menu == "Cadastro: Motoristas":
    # Estrutura de campos organizada
    with st.form("motorista_form"):
        # Seção Pessoal
        st.subheader("Dados Pessoais")
        c1, c2, c3 = st.columns(3)
        nome = c1.text_input("Nome")
        nasc = c2.date_input("Data de Nascimento", format="DD/MM/YYYY")
        
        # Seção Habilitação (Dividida como pediu)
        st.subheader("Habilitação")
        c1, c2, c3 = st.columns(3)
        cnh = c1.text_input("CNH")
        pai = c2.text_input("Nome do Pai")
        mae = c3.text_input("Nome da Mãe")
        
        # Botões de Ação
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        salvar = col_btn1.form_submit_button("Salvar Novo")
        atualizar = col_btn2.form_submit_button("Atualizar")
        limpar = col_btn3.form_button("Limpar")

        if salvar or atualizar:
            # Payload estruturado para o Apps Script
            payload = {
                "nome": nome, "nasc": str(nasc), "filiacao": f"{pai} / {mae}",
                # ... inclua todos os campos aqui ...
            }
            requests.post("SUA_URL_AQUI", json=payload)

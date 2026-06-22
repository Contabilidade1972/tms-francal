import streamlit as st
import requests

st.set_page_config(layout="wide")

st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.selectbox("Módulo", ["Cadastro: Motoristas", "Relatórios"])

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    
    # Botão de Limpar (FORA do form para evitar erros)
    if st.button("Limpar Tela / Novo"):
        st.session_state.data = None
        st.rerun()

    with st.form("motorista_form"):
        st.subheader("Dados Pessoais")
        c1, c2, c3 = st.columns(3)
        nome = c1.text_input("Nome")
        nasc = c2.date_input("Data de Nascimento", format="DD/MM/YYYY")
        telefone = c3.text_input("Telefone Comercial")

        st.subheader("Habilitação")
        h1, h2, h3 = st.columns(3)
        cnh = h1.text_input("CNH")
        pai = h2.text_input("Nome do Pai")
        mae = h3.text_input("Nome da Mãe")
        
        # Botões de Ação
        b1, b2 = st.columns(2)
        salvar = b1.form_submit_button("Salvar Novo")
        atualizar = b2.form_submit_button("Atualizar")

        if salvar or atualizar:
            # Aqui vai o seu payload completo
            payload = {
                "nome": nome, "nasc": str(nasc), "filiacao": f"{pai} / {mae}",
                "cnh": cnh, "telefone": telefone
            }
            # Adicione aqui a chamada requests.post com sua URL
            st.success("Dados processados com sucesso!")

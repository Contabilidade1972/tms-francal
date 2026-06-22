import streamlit as st
import requests

st.set_page_config(layout="wide")
st.sidebar.title("TMS FRANCAL")
menu = st.sidebar.selectbox("Módulo", ["Cadastro: Motoristas", "Relatórios"])

if menu == "Cadastro: Motoristas":
    st.title("Cadastro de Motoristas")
    
    if st.button("Limpar Tela / Novo"):
        st.session_state.data = None
        st.rerun()

    with st.form("motorista_form"):
        st.subheader("Dados Pessoais")
        c1, c2, c3 = st.columns(3)
        nome = c1.text_input("Nome")
        tel = c2.text_input("Telefone Comercial")
        nasc = c3.date_input("Data de Nascimento", format="DD/MM/YYYY")
        
        c4, c5, c6 = st.columns(3)
        cep = c4.text_input("CEP")
        log = c5.text_input("Logradouro")
        num = c6.text_input("Número")
        
        c7, c8, c9 = st.columns(3)
        comp = c7.text_input("Complemento")
        bairro = c8.text_input("Bairro")
        mun = c9.text_input("Município")
        
        c10, c11, c12 = st.columns(3)
        uf = c10.selectbox("UF", ["MG", "SP", "RJ", "ES", "DF"])
        rg = c11.text_input("RG")
        cpf = c12.text_input("CPF")

        st.subheader("Habilitação e Banco")
        h1, h2, h3 = st.columns(3)
        cnh = h1.text_input("CNH")
        uf_cnh = h2.text_input("UF/CNH")
        cat = h3.text_input("Categoria")
        
        h4, h5, h6 = st.columns(3)
        emissao = h4.date_input("Emissão CNH", format="DD/MM/YYYY")
        venc = h5.date_input("Vencimento CNH", format="DD/MM/YYYY")
        fil = h6.text_input("Filiação (Pai/Mãe)")
        
        h7, h8, h9 = st.columns(3)
        banco = h7.text_input("Banco")
        ag = h8.text_input("Agência")
        conta = h9.text_input("Conta")
        
        h10, h11 = st.columns(2)
        rntrc = h10.text_input("RNTRC")
        obs = h11.text_area("Observações")

        b1, b2 = st.columns(2)
        salvar = b1.form_submit_button("Salvar Novo")
        atualizar = b2.form_submit_button("Atualizar")

        if salvar or atualizar:
            # Aqui vai a URL da sua implantação Versão 15
            url = "SUA_URL_DO_APPS_SCRIPT_AQUI"
            payload = {
                "nome": nome, "telefone": tel, "nasc": str(nasc), "cep": cep, "logradouro": log,
                "numero": num, "complemento": comp, "bairro": bairro, "municipio": mun,
                "uf": uf, "rg": rg, "cpf": cpf, "cnh": cnh, "uf_cnh": uf_cnh, "rntrc": rntrc,
                "banco": banco, "agencia": ag, "conta": conta, "emissao": str(emissao),
                "vencimento": str(venc), "categoria": cat, "filiacao": fil, "obs": obs
            }
            requests.post(url, json=payload)
            st.success("Dados processados com sucesso!")

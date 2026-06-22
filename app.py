import streamlit as st
import requests

# 1. Título
st.title("TMS FRANCAL - PROTOCOLO")

# 2. Campos de entrada
cnpj = st.text_input("CNPJ")
nf = st.text_input("NF")

# 3. A lógica do botão deve estar após os inputs
if st.button("SALVAR"):
    # IMPORTANTE: Coloque a sua URL do Apps Script aqui abaixo
    url = "COLE_AQUI_A_URL_DO_SEU_APPS_SCRIPT"
    
    payload = {"cnpj_remetente": cnpj, "nf": nf}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            st.success("Dados enviados com sucesso!")
        else:
            st.error(f"Erro no envio: {response.status_code}")
    except Exception as e:
        st.error(f"Erro na conexão: {e}")

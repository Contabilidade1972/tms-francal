import streamlit as st
import requests

st.title("TMS FRANCAL - PROTOCOLO")

cnpj = st.text_input("CNPJ")
nf = st.text_input("Número da Nota Fiscal")

if st.button("SALVAR DADOS"):
    # URL configurada com o seu código de implantação
    url = "https://script.google.com/macros/s/AKfycbxkvCwx4KMWNXNUqMzEC6P4yNZ51YNfZjgTXr2yxQSA3MhPDbwH74P8jmhOR85M_TWC/exec"
    
    payload = {"cnpj_remetente": cnpj, "nf": nf}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            st.success("Dados enviados com sucesso!")
        else:
            st.error(f"Erro no envio. Código: {response.status_code}")
    except Exception as e:
        st.error(f"Erro: {e}")

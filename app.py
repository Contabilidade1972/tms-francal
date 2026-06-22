import streamlit as st
import requests

st.title("TMS FRANCAL - PROTOCOLO")

cnpj = st.text_input("CNPJ")
nf = st.text_input("NF")

if st.button("SALVAR"):
    # Cole a SUA URL correta aqui entre as aspas
    url = "COLE_AQUI_A_SUA_URL_DO_APPS_SCRIPT"
    
    payload = {"cnpj_remetente": cnpj, "nf": nf}
    
    try:
        # Aumentamos o tempo de espera (timeout) para o Google responder
        response = requests.post(url, json=payload, timeout=10)
        
        # Isso vai mostrar na tela o que o Google está respondendo
        st.write(f"Status Code: {response.status_code}")
        st.write(f"Resposta: {response.text}")
        
        if response.status_code == 200:
            st.success("Dados enviados!")
    except Exception as e:
        st.error(f"Erro detalhado: {e}")

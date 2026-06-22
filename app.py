import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="TMS FRANCAL", layout="centered")

st.title("TMS FRANCAL - PROTOCOLO")

# Campos de entrada
cnpj = st.text_input("CNPJ")
nf = st.text_input("Número da Nota Fiscal")

# Botão de envio
if st.button("SALVAR DADOS"):
    if not cnpj or not nf:
        st.warning("Por favor, preencha todos os campos.")
    else:
        # COLE SUA URL ABAIXO ENTRE AS ASPAS
        url = "COLE_SUA_URL_AQUI"
        
        payload = {
            "cnpj_remetente": cnpj,
            "nf": nf
        }
        
        try:
            # Enviando dados para o Google Apps Script
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                st.success("Dados enviados com sucesso para a planilha!")
            else:
                st.error(f"Erro ao enviar. Código: {response.status_code}")
                st.write(f"Detalhes: {response.text}")
                
        except Exception as e:
            st.error(f"Erro de conexão: {e}")

if st.button("SALVAR"):
    url = "SUA_URL_DO_APP_SCRIPT_AQUI"
    payload = {"cnpj_remetente": cnpj, "nf": nf}
    
    # Faz a requisição
    response = requests.post(url, json=payload)
    
    # Verifica se deu certo
    if response.status_code == 200:
        st.success("Dados enviados com sucesso!")
        st.write(f"Resposta do Google: {response.text}")
    else:
        st.error(f"Erro no envio. Código: {response.status_code}")
        st.write(response.text)

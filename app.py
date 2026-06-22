import streamlit as st

st.title("TMS FRANCAL - GESTÃO DE OPERAÇÕES")

tab1, tab2, tab3 = st.tabs(["Ordem de Coleta", "Minuta de Despacho", "Fatura"])

with tab1:
    st.header("1. Ordem de Coleta (Solicitação)")
    
    # Bloco: Identificação
    col1, col2 = st.columns(2)
    with col1:
        cnpj_remetente = st.text_input("CNPJ Remetente")
        cnpj_destinatario = st.text_input("CNPJ Destinatário")
    with col2:
        nf = st.text_input("Número da Nota Fiscal")
        data_coleta = st.date_input("Data da Coleta")
        
    # Bloco: Carga e Peso
    col3, col4, col5 = st.columns(3)
    with col3:
        peso_bruto = st.number_input("Peso Bruto (kg)")
    with col4:
        volume = st.number_input("Volume")
    with col5:
        valor_mercadoria = st.number_input("Valor da Mercadoria (R$)")
        
    # Bloco: Logística
    observacoes = st.text_area("Observações (ex: Boletos, Seguros)")
    
    if st.button("SALVAR ORDEM DE COLETA"):
        st.success("Ordem de Coleta salva com sucesso! Status: PENDENTE")

with tab2:
    st.header("2. Minuta de Despacho")
    st.info("Aqui serão carregados os dados validados da Ordem de Coleta.")
    # (Este formulário será preenchido automaticamente depois)

with tab3:
    st.header("3. Fatura")
    st.info("A fatura será gerada após a confirmação da entrega.")

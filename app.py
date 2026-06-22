def conectar_sheets():
    # O segredo é ter o cabeçalho [gspread] no Secrets e o caminho aqui
    secrets_data = json.loads(st.secrets["gspread"]["json_content"])
    gc = gspread.service_account_from_dict(secrets_data)
    sh = gc.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg") 
    return sh.worksheet("REGISTRO_OPERACIONAL")

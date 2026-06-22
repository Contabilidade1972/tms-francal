def conectar_sheets():
    # Carrega como um dicionário Python real, sem precisar de json.loads()
    import json
    creds = json.loads(st.secrets["GCP_JSON"])
    gc = gspread.service_account_from_dict(creds)
    sh = gc.open_by_key("1RFiXPxCLPTMBdGWVtPohslcSfgB8ef1_ZyU0IA9_Fgg")
    return sh.worksheet("REGISTRO_OPERACIONAL")

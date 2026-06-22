creds_dict = st.secrets["gspread"]["gcp_service_account"]
# O gspread já entende o dicionário direto, não precisa de json.loads!
gc = gspread.service_account_from_dict(json.loads(creds_dict))

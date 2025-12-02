# Vendor Onboarding & KYC (Streamlit + SQLite)

## Run
1. python -m venv venv
2. activate venv
3. pip install -r requirements.txt
4. mkdir uploads
5. streamlit run app.py

## Demo steps
- Register as Vendor -> upload docs -> copy Vendor ID
- Switch to Admin -> review -> Approve/Reject
- Vendor -> check status using Vendor ID

## Files
- app.py : main app
- vendors.db : created automatically
- uploads/ : uploaded docs stored here

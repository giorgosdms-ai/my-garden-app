import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Διαχείριση Κήπου", layout="wide")

# -------------------------------------------------------------
# 1. Σύνδεση με Google Sheets (Authentication)
# -------------------------------------------------------------
@st.cache_resource
def get_sheet():
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    private_key = creds_dict["private_key"]
    private_key = private_key.replace("\\n", "\n").strip()
    
    if not private_key.startswith("-----BEGIN PRIVATE KEY-----"):
        private_key = f"-----BEGIN PRIVATE KEY-----\n{private_key}\n-----END PRIVATE KEY-----\n"
        
    creds_dict["private_key"] = private_key

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(credentials)
    
    if isinstance(st.secrets["SPREADSHEET_ID"], dict):
        sheet_id = st.secrets["SPREADSHEET_ID"]["SPREADSHEET_ID"]
    else:
        sheet_id = st.secrets["SPREADSHEET_ID"]
        
    return client.open_by_key(sheet_id).sheet1

try:
    sheet = get_sheet()
except Exception as e:
    st.error(f"Σφάλμα σύνδεσης με το Google Sheet: {e}")
    st.stop()

# -------------------------------------------------------------
# 2. Διαχείριση Δεδομένων (Load / Save)
# -------------------------------------------------------------
def load_data():
    try:
        data = sheet.get_all_records()
        if not data:
            return pd.DataFrame(columns=["Ημερομηνία", "Εργασία", "Ποσό", "Εβδομάδα", "Κατάσταση"])
        return pd.DataFrame(data)
    except Exception as e:
        st.warning(f"Δεν βρέθηκαν δεδομένα ή υπήρξε σφάλμα ανάγνωσης: {e}")
        return pd.DataFrame(columns=["Ημερομηνία", "Εργασία", "Ποσό", "Εβδομάδα", "Κατάσταση"])

def save_data(df):
    try:
        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
    except Exception as e:
        st.error(f"Σφάλμα αποθήκευσης: {e}")

# -------------------------------------------------------------
# 3. Διεπαφή Χρήστη (UI) - Καρτέλες
# -------------------------------------------------------------
st.title("🌱 Διαχείριση Κήπου & Εργασιών")

tab_prog, tab_pay, tab_weeks, tab_add = st.tabs(["📅 Πρόγραμμα", "💰 Πληρωμές", "📆 Εβδομάδες", "➕ Προσθήκη"])

df = load_data()

with tab_prog:
    st.header("Πρόγραμμα Εργασιών")
    if df.empty:
        st.info("Δεν υπάρχουν καταχωρημένες εργασίες ακόμη.")
    else:
        st.dataframe(df, use_container_width=True)
        
with tab_pay:
    st.header("Διαχείριση Πληρωμών")
    if not df.empty and "Ποσό" in df.columns:
        total = df["Ποσό"].apply(pd.to_numeric, errors='coerce').sum()
        st.metric(label="Συνολικό Ποσό", value=f"{total} €")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Δεν υπάρχουν δεδομένα πληρωμών.")

with tab_weeks:
    st.header("Εβδομαδιαία Προβολή")
    if not df.empty and "Εβδομάδα" in df.columns:
        weeks = df["Εβδομάδα"].unique()
        selected_week = st.selectbox("Επιλέξτε Εβδομάδα", weeks)
        filtered_df = df[df["Εβδομάδα"] == selected_week]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("Δεν βρέθηκαν δεδομένα εβδομάδων.")

with tab_add:
    st.header("Προσθήκη Νέας Εγγραφής")
    with st.form("add_form"):
        date_val = st.date_input("Ημερομηνία", datetime.today())
        task_val = st.text_input("Εργασία")
        amount_val = st.number_input("Ποσό (€)", min_value=0.0, step=10.0)
        week_val = st.text_input("Εβδομάδα (π.χ. Εβδομάδα 1)")
        status_val = st.selectbox("Κατάσταση", ["Εκκρεμεί", "Ολοκληρώθηκε"])
        
        submitted = st.form_submit_button("Αποθήκευση")
        if submitted:
            new_row = pd.DataFrame([{
                "Ημερομηνία": str(date_val),
                "Εργασία": task_val,
                "Ποσό": amount_val,
                "Εβδομάδα": week_val,
                "Κατάσταση": status_val
            }])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            save_data(updated_df)
            st.success("Η εγγραφή αποθηκεύτηκε με επιτυχία!")
            st.rerun()

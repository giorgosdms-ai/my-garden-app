import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Διαχείριση Κήπου", layout="wide")

# -------------------------------------------------------------
# 1. Σύνδεση με Google Sheets (Authentication) - ΥΠΕΡ-ΚΑΘΑΡΙΣΜΟΣ
# -------------------------------------------------------------
@st.cache_resource
def get_sheet():
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    # Καθαρισμός του private key από τυχόν περιττά σύμβολα ή κενά
    private_key = str(creds_dict["private_key"])
    private_key = private_key.replace("\\n", "\n")
    
    # Ανεξαρτήτως πώς μπήκε, το ξαναφτιάχνουμε σωστά
    if "BEGIN PRIVATE KEY" in private_key:
        # Απομόνωση μόνο του κλειδιού ανάμεσα στα headers
        lines = [line.strip() for line in private_key.split("\n") if line.strip()]
        clean_lines = []
        capture = False
        for line in lines:
            if "BEGIN PRIVATE KEY" in line:
                capture = True
                continue
            if "END PRIVATE KEY" in line:
                capture = False
                break
            if capture:
                clean_lines.append(line)
        
        key_body = "".join(clean_lines)
        private_key = f"-----BEGIN PRIVATE KEY-----\n{key_body}\n-----END PRIVATE KEY-----\n"
        
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
    st.error(f"Σφάλμα σύνδεσης: {e}")
    st.info("💡 Αν βλέπεις ακόμα σφάλμα PEM, πήγαινε στα Settings -> Secrets στο Streamlit Cloud και βεβαιώσου ότι το private_key είναι σε μια ενιαία γραμμή με \\n.")
    st.stop()

# -------------------------------------------------------------
# 2. Διαχείριση Δεδομένων
# -------------------------------------------------------------
def load_data():
    try:
        data = sheet.get_all_records()
        if not data:
            return pd.DataFrame(columns=["Ημερομηνία", "Εργασία", "Ποσό", "Εβδομάδα", "Κατάσταση"])
        return pd.DataFrame(data)
    except Exception as e:
        return pd.DataFrame(columns=["Ημερομηνία", "Εργασία", "Ποσό", "Εβδομάδα", "Κατάσταση"])

def save_data(df):
    try:
        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
    except Exception as e:
        st.error(f"Σφάλμα αποθήκευσης: {e}")

# -------------------------------------------------------------
# 3. Διεπαφή Χρήστη
# -------------------------------------------------------------
st.title("🌱 Διαχείριση Κήπου & Εργασιών")
tab_prog, tab_pay, tab_weeks, tab_add = st.tabs(["📅 Πρόγραμμα", "💰 Πληρωμές", "📆 Εβδομάδες", "➕ Προσθήκη"])

df = load_data()

with tab_prog:
    st.header("Πρόγραμμα Εργασιών")
    st.dataframe(df, use_container_width=True)
        
with tab_pay:
    st.header("Διαχείριση Πληρωμών")
    if not df.empty and "Ποσό" in df.columns:
        total = df["Ποσό"].apply(pd.to_numeric, errors='coerce').sum()
        st.metric(label="Συνολικό Ποσό", value=f"{total} €")
        st.dataframe(df, use_container_width=True)

with tab_weeks:
    st.header("Εβδομαδιαία Προβολή")
    if not df.empty and "Εβδομάδα" in df.columns:
        weeks = df["Εβδομάδα"].unique()
        selected_week = st.selectbox("Επιλέξτε Εβδομάδα", weeks)
        st.dataframe(df[df["Εβδομάδα"] == selected_week], use_container_width=True)

with tab_add:
    st.header("Προσθήκη Νέας Εγγραφής")
    with st.form("add_form"):
        date_val = st.date_input("Ημερομηνία", datetime.today())
        task_val = st.text_input("Εργασία")
        amount_val = st.number_input("Ποσό (€)", min_value=0.0, step=10.0)
        week_val = st.text_input("Εβδομάδα")
        status_val = st.selectbox("Κατάσταση", ["Εκκρεμεί", "Ολοκληρώθηκε"])
        
        if st.form_submit_button("Αποθήκευση"):
            new_row = pd.DataFrame([{"Ημερομηνία": str(date_val), "Εργασία": task_val, "Ποσό": amount_val, "Εβδομάδα": week_val, "Κατάσταση": status_val}])
            save_data(pd.concat([df, new_row], ignore_index=True))
            st.success("Αποθηκεύτηκε!")
            st.rerun()

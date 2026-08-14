import streamlit as st
import gspread
import calendar
from datetime import date, datetime, timedelta

# Ρύθμιση σελίδας
st.set_page_config(page_title="Πρόγραμμα Κήπων", page_icon="🌿", layout="centered")

# Ασφαλής ανανέωση σελίδας
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# Σύνδεση με Google Sheets μέσω Secrets
@st.cache_resource
def get_gspread_client():
    credentials = dict(st.secrets["gcp_service_account"])
    # Διόρθωση private key αν χρειάζεται
    if "private_key" in credentials:
        credentials["private_key"] = credentials["private_key"].replace("\\n", "\n")
    return gspread.service_account_from_dict(credentials)

try:
    gc = get_gspread_client()
    spreadsheet_id = st.secrets["SPREADSHEET_ID"]
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.sheet1
except Exception as e:
    st.error(f"Σφάλμα σύνδεσης με το Google Sheet: {e}")
    st.stop()

# Συνάρτηση φόρτωσης δεδομένων
def load_data():
    try:
        records = worksheet.get_all_records()
        return records
    except Exception:
        return []

# Συνάρτηση αποθήκευσης εγγραφής
def add_record(garden_name, day, time_slot, notes):
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    worksheet.append_row([date_str, garden_name, day, time_slot, notes])

# CSS για καθαρή εμφανιση σε κινητά
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("🌿 Πρόγραμμα Κήπων")

# Φόρτωση υπαρχουσών εγγραφών
data = load_data()

# Φόρμα καταχώρησης
with st.form("garden_form", clear_on_submit=True):
    st.subheader("➕ Νέα Καταχώρηση")
    garden_name = st.text_input("Όνομα Κήπου / Πελάτη")
    
    days = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή", "Σάββατο", "Κυριακή"]
    day = st.selectbox("Ημέρα", days)
    
    time_slot = st.text_input("Ώρα (π.χ. 09:00 - 11:00)", "09:00")
    notes = st.text_area("Σημειώσεις")
    
    submitted = st.form_submit_submitted = st.form_submit_button("Αποθήκευση")
    if submitted:
        if garden_name:
            add_record(garden_name, day, time_slot, notes)
            st.success(f"Η καταχώρηση για '{garden_name}' αποθηκεύτηκε στο Google Sheet!")
            safe_rerun()
        else:
            st.warning("Παρακαλώ συμπληρώστε το όνομα του κήπου.")

st.divider()

# Προβολή Καταχωρήσεων
st.subheader("📋 Πρόγραμμα")
if data:
    for item in reversed(data):
        with st.expander(f"📍 {item.get('Όνομα Κήπου', item.get('Garden', 'Κήπος'))} - {item.get('Ημέρα', item.get('Day', ''))}"):
            st.write(f"**Ώρα:** {item.get('Ώρα', item.get('Time', '-'))}")
            st.write(f"**Σημειώσεις:** {item.get('Σημειώσεις', item.get('Notes', '-'))}")
            st.caption(f"Ημ/νία καταχώρησης: {item.get('Ημερομηνία', item.get('Date', '-'))}")
else:
    st.info("Δεν υπάρχουν ακόμα καταχωρήσεις.")

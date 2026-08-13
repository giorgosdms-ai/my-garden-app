import streamlit as st
import json
import os
import calendar
from datetime import datetime

st.set_page_config(page_title="Πρόγραμμα Κήπων", page_icon="🌿", layout="centered")

# Custom CSS για πολύ μαζεμένο σχεδιασμό στο κινητό
st.markdown("""
<style>
    .block-container { padding-top: 1rem; padding-bottom: 2rem; padding-left: 0.5rem; padding-right: 0.5rem; }
    div[data-testid="stVerticalBlock"] > div { gap: 0.2rem; }
    h3 { margin-top: 0.6rem !important; margin-bottom: 0.2rem !important; font-size: 1.15rem !important; }
    hr { margin-top: 0.4rem !important; margin-bottom: 0.4rem !important; }
    .stCheckbox { margin-bottom: 0px; }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "gardens_data.json"
PASSWORD_SECRET = "1619"

ALL_WEEKS = ["Εβδομάδα Α", "Εβδομάδα Β", "Εβδομάδα Γ", "Εβδομάδα Δ"]
FORTNIGHT_AC = ["Εβδομάδα Α", "Εβδομάδα Γ"] 
FORTNIGHT_BD = ["Εβδομάδα Β", "Εβδομάδα Δ"]
DAYS_GREEK = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή", "Σάββατο", "Κυριακή"]
MONTHS_SHORT = ["Ιαν", "Φεβ", "Μαρ", "Απρ", "Μαι", "Ιουν", "Ιουλ", "Αυγ", "Σεπ", "Οκτ", "Νοε", "Δεκ"]
MONTHS_FULL = ["Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάιος", "Ιούνιος", "Ιούλιος", "Αύγουστος", "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"]

# 🛠️ Συνάρτηση υπολογισμού εβδομάδας μήνα (Α, Β, Γ, Δ)
def get_week_name(day_num):
    if day_num <= 7:
        return "Εβδομάδα Α"
    elif day_num <= 14:
        return "Εβδομάδα Β"
    elif day_num <= 21:
        return "Εβδομάδα Γ"
    else:
        return "Εβδομάδα Δ"

# 📁 Αποθήκευση & Φόρτωση
def save_data():
    data = {
        "my_gardens": st.session_state.my_gardens,
        "extra_events": st.session_state.extra_events
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = json.load(f)
            if isinstance(content, list):
                return content, []
            return content.get("my_gardens", []), content.get("extra_events", [])
    return None, None

def get_default_gardens():
    default_paid = {m: False for m in MONTHS_SHORT}
    return [
        {"name": "Αχιλλέας", "day": "Δευτέρα", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid.copy()},
        {"name": "Ξανθος", "day": "Δευτέρα", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy()},
        {"name": "Γλυφαδα", "day": "Τρίτη", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid.copy()},
        {"name": "Σταθης", "day": "Τετάρτη", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid.copy()},
        {"name": "Μετόχιο", "day": "Πέμπτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy()},
        {"name": "Μάριος", "day": "Παρασκευή", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy()},
    ]

# Επαναφορά Δεδομένων
if st.sidebar.button("⚠️ Επαναφορά Αρχικών Δεδομένων"):
    st.session_state.my_gardens = get_default_gardens()
    st.session_state.extra_events = []
    save_data()
    st.rerun()

st.title("🌿 Πρόγραμμα Κήπων")

password = st.text_input("🔑 Κωδικός πρόσβασης:", type="password")

if password == PASSWORD_SECRET:
    if "my_gardens" not in st.session_state or "extra_events" not in st.session_state:
        saved_g, saved_e = load_data()
        st.session_state.my_gardens = saved_g if saved_g is not None else get_default_gardens()
        st.session_state.extra_events = saved_e if saved_e is not None else []
        save_data()

    view_mode = st.radio("📌 **Προβολή:**", ["📅 Πλήρες Μηνιαίο Πρόγραμμα", "➕ Προσθήκη Έκτακτου"], horizontal=True)

    if view_mode == "📅 Πλήρες Μηνιαίο Πρόγραμμα":
        
        col_m, col_y = st.columns(2)
        selected_month_num = col_m.selectbox("Μήνας:", range(1, 13), index=datetime.now().month-1, format_func=lambda x: MONTHS_FULL[x-1])
        selected_year = col_y.number_input("Έτος:", value=datetime.now().year, step=1)

        search_query = st.text_input("🔍 Αναζήτηση Κήπου:", placeholder="Όνομα κήπου...")

        def render_month_picker(garden_idx, key_prefix):
            g = st.session_state.my_gardens[garden_idx]
            pm = g.get("paid_months", {})
            paid_list = [m for m in MONTHS_SHORT if pm.get(m, False)]
            status_text = "🟢 " + ", ".join(paid_list) if paid_list else "🔴 Καμία"
            
            st.caption(f"Πληρωμές: {status_text}")
            
            for row in range(0, 12, 4):
                cols = st.columns(4)
                for col_idx in range(4):
                    m_idx = row + col_idx
                    if m_idx < 12:
                        m = MONTHS_SHORT[m_idx]
                        is_checked = pm.get(m, False)
                        new_val = cols[col_idx].checkbox(m, value=is_checked, key=f"{key_prefix}_{m}_{garden_idx}")
                        if new_val != is_checked:
                            st.session_state.my_gardens[garden_idx]["paid_months"][m] = new_val
                            save_data()
                            st.rerun()

        if search_query.strip():
            st.subheader(f"🔎 Αποτελέσματα για: '{search_query}'")
            for idx, g in enumerate(st.session_state.my_gardens):
                if search_query.lower() in g["name"].lower():
                    weeks_str = ", ".join([w.replace("Εβδομάδα ", "") for w in g.get('weeks', [])])
                    st.write(f"📌 **{g['name']}** | {g['day']} | Εβδ: {weeks_str}")
                    render_month_picker(idx, "search")
                    st.divider()
        else:
            num_days = calendar.monthrange(selected_year, selected_month_num)[1]

            # 📆 ΕΜΦΑΝΙΣΗ ΟΛΟΥ ΤΟΥ ΜΗΝΑ ΜΕ ΤΗ ΣΕΙΡΑ (1 έως 30/31)
            for day_num in range(1, num_days + 1):
                day_dt = datetime(selected_year, selected_month_num, day_num)
                date_str = day_dt.strftime("%Y-%m-%d")
                greek_day_name = DAYS_GREEK[day_dt.weekday()]
                
                # Παραλείπουμε τις Κυριακές (αν θέλεις)
                if greek_day_name == "Κυριακή":
                    continue

                week_code = get_week_name(day_num)

                # 1. Τακτικοί κήποι για αυτή τη μέρα/εβδομάδα
                matching_gardens = [
                    (idx, g) for idx, g in enumerate(st.session_state.my_gardens)
                    if g["day"] == greek_day_name and week_code in g.get("weeks", [])
                ]

                # 2. Έκτακτα ραντεβού για αυτή την ημερομηνία
                matching_extras = [
                    ev for ev in st.session_state.extra_events
                    if ev["date"] == date_str
                ]

                # Τίτλος Ημέρας (π.χ. Δευτέρα 03/08 - [Εβδομάδα Α])
                st.markdown(f"### 📌 {greek_day_name} {day_num:02d}/{selected_month_num:02d} <small style='color:gray;'>({week_code})</small>", unsafe_allow_html=True)

                # ⚡ Έκτακτα Ραντεβού
                if matching_extras:
                    for ex in matching_extras:
                        st.warning(f"⚡ **{ex['time']} - {ex['title']}**" + (f" ({ex['notes']})" if ex.get('notes') else ""))

                # 🌿 Τακτικοί Κήποι
                if not matching_gardens and not matching_extras:
                    st.caption("_Καμία εργασία_")
                else:
                    for idx, g in matching_gardens:
                        # Checkbox & Όνομα στην ίδια γραμμή
                        st.checkbox(f"🌿 **{g['name']}**", key=f"chk_{date_str}_{idx}_{g['name']}")
                        
                        # Σημειώσεις & Πληρωμές σε μικρό Popover
                        with st.popover(f"📝 Σημειώσεις ({g['name']})"):
                            render_month_picker(idx, f"main_{date_str}")
                            user_note = st.text_area("Σημείωση:", value=g.get("notes", ""), key=f"note_{date_str}_{idx}", height=60)
                            if user_note != g.get("notes", ""):
                                st.session_state.my_gardens[idx]["notes"] = user_note
                                save_data()

                st.markdown("---")

    else:
        # --- ΠΡΟΣΘΗΚΗ ΕΚΤΑΚΤΟΥ ---
        st.subheader("➕ Προσθήκη Έκτακτου Ραντεβού")

        ex_date = st.date_input("Ημερομηνία:", datetime.now())
        ex_time = st.time_input("Ώρα:", datetime.strptime("10:00", "%H:%M").time())
        ex_title = st.text_input("Περιγραφή / Όνομα:")
        ex_note = st.text_area("Σημείωση (προαιρετικά):", height=60)

        if st.button("✅ Αποθήκευση στο Πρόγραμμα"):
            if ex_title.strip():
                new_event = {
                    "date": ex_date.strftime("%Y-%m-%d"),
                    "time": ex_time.strftime("%H:%M"),
                    "title": ex_title,
                    "notes": ex_note
                }
                st.session_state.extra_events.append(new_event)
                save_data()
                st.success(f"Προστέθηκε επιτυχώς για τις {ex_date.strftime('%d/%m/%Y')}!")
                st.rerun()

elif password != "":
    st.error("❌ Λάθος κωδικός πρόσβασης!")

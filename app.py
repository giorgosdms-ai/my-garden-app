import streamlit as st
import json
import os
import calendar
from datetime import datetime

st.set_page_config(page_title="Πρόγραμμα Κήπων", page_icon="🌿", layout="centered")

# CSS για καθαρή & σφιχτή προβολή στο κινητό
st.markdown("""
<style>
    .block-container { padding-top: 0.8rem; padding-bottom: 1.5rem; padding-left: 0.5rem; padding-right: 0.5rem; }
    div[data-testid="stVerticalBlock"] > div { gap: 0.2rem; }
    h3 { margin-top: 0.6rem !important; margin-bottom: 0.2rem !important; font-size: 1.1rem !important; color: #ff4b4b; }
    hr { margin-top: 0.4rem !important; margin-bottom: 0.4rem !important; }
    .stCheckbox { margin-bottom: 0px; }
    .streamlit-expanderHeader { font-size: 0.95rem !important; font-weight: 600; padding: 4px 8px !important; }
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

# 🛠️ Υπολογισμός εβδομάδας (Α, Β, Γ, Δ)
def get_week_name(day_num):
    if day_num <= 7:
        return "Εβδομάδα Α"
    elif day_num <= 14:
        return "Εβδομάδα Β"
    elif day_num <= 21:
        return "Εβδομάδα Γ"
    else:
        return "Εβδομάδα Δ"

# 🌿 ΠΛΗΡΗΣ ΑΡΧΙΚΗ ΛΙΣΤΑ ΚΗΠΩΝ
def get_default_gardens():
    default_paid = {m: False for m in MONTHS_SHORT}
    return [
        # ΔΕΥΤΕΡΑ
        {"name": "Αχιλλέας", "day": "Δευτέρα", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid.copy()},
        {"name": "Ξανθος", "day": "Δευτέρα", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy()},
        
        # ΤΡΙΤΗ (Προστέθηκαν όλοι οι κήποι της Τρίτης)
        {"name": "Γλυφαδα", "day": "Τρίτη", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid.copy()},
        {"name": "Κήπος Τρίτης 2", "day": "Τρίτη", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid.copy()},
        {"name": "Κήπος Τρίτης 3", "day": "Τρίτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy()},
        
        # ΤΕΤΑΡΤΗ
        {"name": "Σταθης", "day": "Τετάρτη", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid.copy()},
        
        # ΠΕΜΠΤΗ
        {"name": "Μετόχιο", "day": "Πέμπτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy()},
        
        # ΠΑΡΑΣΚΕΥΗ
        {"name": "Μάριος", "day": "Παρασκευή", "weeks": FORTNIGHT_AC, "notes": "", "paid_notes": default_paid.copy(), "paid_months": default_paid.copy()},
    ]

def save_data():
    data = {
        "my_gardens": st.session_state.my_gardens,
        "extra_events": st.session_state.extra_events
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                content = json.load(f)
                if isinstance(content, list):
                    return content, []
                return content.get("my_gardens", []), content.get("extra_events", [])
        except:
            return None, None
    return None, None

st.title("🌿 Πρόγραμμα Κήπων")

password = st.text_input("🔑 Κωδικός πρόσβασης:", type="password")

if password == PASSWORD_SECRET:
    if "my_gardens" not in st.session_state or "extra_events" not in st.session_state:
        saved_g, saved_e = load_data()
        
        # 🔄 ΑΥΤΟΜΑΤΟΣ ΕΛΕΓΧΟΣ: Αν η Τρίτη έχει μόνο 1 κήπο στο αποθηκευμένο αρχείο, κάνε εξαναγκασμένη ανανέωση!
        if saved_g is not None:
            tue_count = sum(1 for g in saved_g if g.get("day") == "Τρίτη")
            if tue_count <= 1:
                saved_g = get_default_gardens()

        st.session_state.my_gardens = saved_g if saved_g is not None else get_default_gardens()
        st.session_state.extra_events = saved_e if saved_e is not None else []
        save_data()

    view_mode = st.radio("📌 **Προβολή:**", ["📅 Πλήρες Μηνιαίο Πρόγραμμα", "➕ Προσθήκη / Διαχείριση"], horizontal=True)

    if view_mode == "📅 Πλήρες Μηνιαίο Πρόγραμμα":
        
        col_m, col_y = st.columns(2)
        selected_month_num = col_m.selectbox("Μήνας:", range(1, 13), index=datetime.now().month-1, format_func=lambda x: MONTHS_FULL[x-1])
        selected_year = col_y.number_input("Έτος:", value=datetime.now().year, step=1)

        search_query = st.text_input("🔍 Αναζήτηση Κήπου:", placeholder="Γράψε όνομα...")

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

            # 📆 ΕΜΦΑΝΙΣΗ ΗΜΕΡΩΝ ΜΗΝΑ
            for day_num in range(1, num_days + 1):
                day_dt = datetime(selected_year, selected_month_num, day_num)
                date_str = day_dt.strftime("%Y-%m-%d")
                greek_day_name = DAYS_GREEK[day_dt.weekday()]
                
                if greek_day_name == "Κυριακή":
                    continue

                week_code = get_week_name(day_num)

                matching_gardens = [
                    (idx, g) for idx, g in enumerate(st.session_state.my_gardens)
                    if g["day"] == greek_day_name and week_code in g.get("weeks", [])
                ]

                matching_extras = [
                    ev for ev in st.session_state.extra_events
                    if ev["date"] == date_str
                ]

                st.markdown(f"### 📌 {greek_day_name} {day_num:02d}/{selected_month_num:02d} <small style='color:gray;'>({week_code})</small>", unsafe_allow_html=True)

                if matching_extras:
                    for ex in matching_extras:
                        st.warning(f"⚡ **{ex['time']} - {ex['title']}**" + (f" ({ex['notes']})" if ex.get('notes') else ""))

                if not matching_gardens and not matching_extras:
                    st.caption("_Καμία εργασία_")
                else:
                    for idx, g in matching_gardens:
                        st.checkbox(f"🌿 **{g['name']}**", key=f"chk_{date_str}_{idx}_{g['name']}")
                        
                        with st.expander(f"📝 Σημειώσεις & Πληρωμές ({g['name']})", expanded=False):
                            render_month_picker(idx, f"main_{date_str}")
                            user_note = st.text_area("Σημείωση:", value=g.get("notes", ""), key=f"note_{date_str}_{idx}", height=60)
                            if user_note != g.get("notes", ""):
                                st.session_state.my_gardens[idx]["notes"] = user_note
                                save_data()

                st.markdown("---")

    else:
        # --- ΠΡΟΣΘΗΚΗ / ΔΙΑΧΕΙΡΙΣΗ ---
        tab1, tab2, tab3 = st.tabs(["➕ Νέος Κήπος", "⚡ Νέο Έκτακτο", "🗑️ Διαγραφή Κήπου"])

        with tab1:
            st.subheader("Προσθήκη Τακτικού Κήπου")
            new_name = st.text_input("Όνομα Κήπου / Πελάτη:")
            new_day = st.selectbox("Ημέρα:", DAYS_GREEK[:6])
            
            st.write("Σε ποιες εβδομάδες πηγαίνεις;")
            w_a = st.checkbox("Εβδομάδα Α (1η-7η)", value=True)
            w_b = st.checkbox("Εβδομάδα Β (8η-14η)", value=False)
            w_c = st.checkbox("Εβδομάδα Γ (15η-21η)", value=True)
            w_d = st.checkbox("Εβδομάδα Δ (22η-31η)", value=False)

            selected_weeks = []
            if w_a: selected_weeks.append("Εβδομάδα Α")
            if w_b: selected_weeks.append("Εβδομάδα Β")
            if w_c: selected_weeks.append("Εβδομάδα Γ")
            if w_d: selected_weeks.append("Εβδομάδα Δ")

            if st.button("✅ Προσθήκη Κήπου"):
                if new_name.strip():
                    default_paid = {m: False for m in MONTHS_SHORT}
                    st.session_state.my_gardens.append({
                        "name": new_name,
                        "day": new_day,
                        "weeks": selected_weeks,
                        "notes": "",
                        "paid_months": default_paid
                    })
                    save_data()
                    st.success(f"Ο κήπος '{new_name}' προστέθηκε!")
                    st.rerun()

        with tab2:
            st.subheader("Προσθήκη Έκτακτου Ραντεβού")
            ex_date = st.date_input("Ημερομηνία:", datetime.now())
            ex_time = st.time_input("Ώρα:", datetime.strptime("10:00", "%H:%M").time())
            ex_title = st.text_input("Περιγραφή:")
            ex_note = st.text_area("Σημείωση:", height=60)

            if st.button("✅ Αποθήκευση Έκτακτου"):
                if ex_title.strip():
                    new_event = {
                        "date": ex_date.strftime("%Y-%m-%d"),
                        "time": ex_time.strftime("%H:%M"),
                        "title": ex_title,
                        "notes": ex_note
                    }
                    st.session_state.extra_events.append(new_event)
                    save_data()
                    st.success("Το έκτακτο προστέθηκε!")
                    st.rerun()

        with tab3:
            st.subheader("Διαγραφή Κήπου")
            garden_names = [g["name"] for g in st.session_state.my_gardens]
            if garden_names:
                to_delete = st.selectbox("Επίλεξε κήπο για διαγραφή:", garden_names)
                if st.button("🗑️ Διαγραφή Κήπου"):
                    st.session_state.my_gardens = [g for g in st.session_state.my_gardens if g["name"] != to_delete]
                    save_data()
                    st.success(f"Ο κήπος '{to_delete}' διαγράφηκε!")
                    st.rerun()

elif password != "":
    st.error("❌ Λάθος κωδικός πρόσβασης!")

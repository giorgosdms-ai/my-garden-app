import streamlit as st
import json
import os
import calendar
from datetime import datetime

st.set_page_config(page_title="Πρόγραμμα Κήπων", page_icon="🌿", layout="wide")

DATA_FILE = "gardens_data.json"
PASSWORD_SECRET = "1619"

ALL_WEEKS = ["Εβδομάδα Α", "Εβδομάδα Β", "Εβδομάδα Γ", "Εβδομάδα Δ"]
FORTNIGHT_AC = ["Εβδομάδα Α", "Εβδομάδα Γ"] 
FORTNIGHT_BD = ["Εβδομάδα Β", "Εβδομάδα Δ"]
DAYS_GREEK = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή", "Σάββατο", "Κυριακή"]
MONTHS_SHORT = ["Ιαν", "Φεβ", "Μαρ", "Απρ", "Μαι", "Ιουν", "Ιουλ", "Αυγ", "Σεπ", "Οκτ", "Νοε", "Δεκ"]
MONTHS_FULL = ["Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάιος", "Ιούνιος", "Ιούλιος", "Αύγουστος", "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"]

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
            # Συμβατότητα με παλαιότερη μορφή
            if isinstance(content, list):
                return content, []
            return content.get("my_gardens", []), content.get("extra_events", [])
    return None, None

def get_default_gardens():
    default_paid = {m: False for m in MONTHS_SHORT}
    return [
        # --- ΔΕΥΤΕΡΑ ---
        {"name": "Αχιλλέας", "day": "Δευτέρα", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Ξανθος", "day": "Δευτέρα", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Αιγίνης", "day": "Δευτέρα", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Τεγεας", "day": "Δευτέρα", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Ιωαννιδης", "day": "Δευτέρα", "weeks": ["Εβδομάδα Α"], "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Πετραν", "day": "Δευτέρα", "weeks": ["Εβδομάδα Β"], "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Αγίας Λαύρας", "day": "Δευτέρα", "weeks": ["Εβδομάδα Γ"], "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "28ης", "day": "Δευτέρα", "weeks": ["Εβδομάδα Δ"], "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        
        # --- ΤΡΙΤΗ ---
        {"name": "Γλυφαδα", "day": "Τρίτη", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Αγιος Δημήτριος 1", "day": "Τρίτη", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Αγιος Δημήτριος 2", "day": "Τρίτη", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Βουλα", "day": "Τρίτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "βερα λω φαληρο", "day": "Τρίτη", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Πετρούλα", "day": "Τρίτη", "weeks": ["Εβδομάδα Α"], "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        
        # --- ΤΕΤΑΡΤΗ ---
        {"name": "Σταθης", "day": "Τετάρτη", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Μενιδι", "day": "Τετάρτη", "weeks": ALL_WEEKS, "notes": "", "paid_notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Ανθουσων", "day": "Τετάρτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Μακης", "day": "Τετάρτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Αλέξανδρος", "day": "Τετάρτη", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Άνω Λιόσια", "day": "Τετάρτη", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Δίπλα από Στάθη", "day": "Τετάρτη", "weeks": ["Εβδομάδα Β"], "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Μεταμόρφωση", "day": "Τετάρτη", "weeks": ["Εβδομάδα Γ"], "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        
        # --- ΠΕΜΠΤΗ ---
        {"name": "Μετόχιο", "day": "Πέμπτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Μαρουσι", "day": "Πέμπτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Μικράς Ασίας Αλέξανδρος", "day": "Πέμπτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Μικρας Ασιας 2", "day": "Πέμπτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "καβαλας", "day": "Πέμπτη", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Ροζελα", "day": "Πέμπτη", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "βερα λω ψυχικό", "day": "Πέμπτη", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        {"name": "Αλικη", "day": "Πέμπτη", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
        
        # --- ΠΑΡΑΣΚΕΥΗ ---
        {"name": "Μάριος", "day": "Παρασκευή", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid.copy(), "is_extra": False},
    ]

# Επαναφορά Δεδομένων
if st.sidebar.button("⚠️ Επαναφορά Αρχικών Δεδομένων"):
    st.session_state.my_gardens = get_default_gardens()
    st.session_state.extra_events = []
    save_data()
    st.rerun()

st.title("🌿 Πρόγραμμα & Ημερολόγιο Κήπων 2026")

password = st.text_input("🔑 Δώσε τον κωδικό πρόσβασης:", type="password")

if password == PASSWORD_SECRET:
    if "my_gardens" not in st.session_state or "extra_events" not in st.session_state:
        saved_g, saved_e = load_data()
        st.session_state.my_gardens = saved_g if saved_g is not None else get_default_gardens()
        st.session_state.extra_events = saved_e if saved_e is not None else []
        save_data()

    # Επιλογή Προβολής: Εβδομαδιαίο Πρόγραμμα ή Μηνιαίο Ημερολόγιο
    view_mode = st.radio("📌 **Επίλεξε Προβολή:**", ["📅 Μηνιαίο Ημερολόγιο & Εξτραδάκια", "📋 Εβδομαδιαίο Πρόγραμμα Κήπων"], horizontal=True)

    if view_mode == "📅 Μηνιαίο Ημερολόγιο & Εξτραδάκια":
        st.header("📅 Ημερολόγιο & Έκτακτα Ραντεβού")
        
        col_m, col_y = st.columns(2)
        # Προεπιλογή Αύγουστος 2026 (index 7)
        selected_month_num = col_m.selectbox("Μήνας:", range(1, 13), index=7, format_func=lambda x: MONTHS_FULL[x-1])
        selected_year = col_y.number_input("Έτος:", value=2026, step=1)

        st.markdown(f"### 🗓️ {MONTHS_FULL[selected_month_num-1]} {selected_year}")

        # ⚡ Φόρμα Προσθήκης Έκτακτου Ραντεβού
        with st.expander("⚡ **Προσθήκη Εξτραδακίου με Ημερομηνία & Ώρα**", expanded=True):
            c1, c2, c3 = st.columns([2, 1, 1])
            ex_date = c1.date_input("Ημερομηνία:", datetime(selected_year, selected_month_num, 21))
            ex_time = c2.time_input("Ώρα:", datetime.strptime("10:00", "%H:%M").time())
            ex_title = c3.text_input("Περιγραφή / Όνομα:")
            ex_note = st.text_area("📝 Σημείωση (προαιρετικά):", height=60, key="cal_ex_note")

            if st.button("➕ Αποθήκευση στο Ημερολόγιο"):
                if ex_title.strip():
                    new_event = {
                        "date": ex_date.strftime("%Y-%m-%d"),
                        "time": ex_time.strftime("%H:%M"),
                        "title": ex_title,
                        "notes": ex_note
                    }
                    st.session_state.extra_events.append(new_event)
                    save_data()
                    st.success(f"Προστέθηκε: {ex_title} στις {ex_date.strftime('%d/%m/%Y')} ώρα {ex_time.strftime('%H:%M')}")
                    st.rerun()

        st.divider()

        # Εμφάνιση Ημερών Μήνα
        cal = calendar.monthcalendar(selected_year, selected_month_num)
        
        for week in cal:
            cols = st.columns(7)
            for day_idx in range(7):
                day_num = week[day_idx]
                if day_num != 0:
                    day_str = f"{selected_year}-{selected_month_num:02d}-{day_num:02d}"
                    greek_day_name = DAYS_GREEK[day_idx]
                    
                    with cols[day_idx]:
                        st.markdown(f"**{day_num} {MONTHS_SHORT[selected_month_num-1]}**\n_{greek_day_name}_")
                        
                        # Βρες εξτραδάκια για αυτή τη μέρα
                        day_events = [e for e in st.session_state.extra_events if e["date"] == day_str]
                        
                        for ev_idx, ev in enumerate(day_events):
                            st.info(f"⏰ **{ev['time']}**\n⚡ **{ev['title']}**\n_{ev.get('notes', '')}_")
                            if st.button("🗑️", key=f"del_ev_{day_str}_{ev_idx}"):
                                st.session_state.extra_events.remove(ev)
                                save_data()
                                st.rerun()

    else:
        # --- ΕΒΔΟΜΑΔΙΑΙΟ ΠΡΟΓΡΑΜΜΑ (ΠΡΟΗΓΟΥΜΕΝΗ ΠΡΟΒΟΛΗ) ---
        search_query = st.text_input("🔍 **Αναζήτηση Κήπου / Εργασίας:**", placeholder="Γράψε όνομα κήπου...")
        week = st.radio("🗓️ **Επίλεξε Εβδομάδα:**", ALL_WEEKS, horizontal=True)

        def render_month_picker(garden_idx, key_prefix):
            g = st.session_state.my_gardens[garden_idx]
            pm = g.get("paid_months", {})
            paid_list = [m for m in MONTHS_SHORT if pm.get(m, False)]
            status_text = "🟢 Πληρωμένοι: " + ", ".join(paid_list) if paid_list else "🔴 Καμία πληρωμή"
            
            st.markdown(f"**💶 Πληρωμές 2026:** _{status_text}_")
            
            for row in range(0, 12, 3):
                cols = st.columns(3)
                for col_idx in range(3):
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
                    st.write(f"📌 **{g['name']}** | Ημέρα: **{g['day']}** | Εβδ: **{weeks_str}**")
                    render_month_picker(idx, "search")
                    note = st.text_area("📝 Σημειώσεις:", value=g.get("notes", ""), key=f"search_note_{idx}", height=70)
                    if note != g.get("notes", ""):
                        st.session_state.my_gardens[idx]["notes"] = note
                        save_data()
                    st.divider()
        else:
            for day in DAYS_GREEK[:6]: # Δευτέρα έως Σάββατο
                matching_gardens = [
                    (idx, g) for idx, g in enumerate(st.session_state.my_gardens)
                    if g["day"] == day and week in g.get("weeks", [])
                ]
                
                with st.expander(f"📌 {day} ({len(matching_gardens)} κήποι/εργασίες)"):
                    if not matching_gardens:
                        st.write("*Δεν υπάρχουν κήποι ή εργασίες.*")
                    for idx, g in matching_gardens:
                        weeks_str = ", ".join([w.replace("Εβδομάδα ", "") for w in g.get('weeks', [])])
                        st.checkbox(f"🌿 **{g['name']}** (Εβδ: {weeks_str})", key=f"chk_{week}_{day}_{idx}_{g['name']}")
                        
                        render_month_picker(idx, f"main_{week}_{day}")

                        user_note = st.text_area(
                            "📝 Σημειώσεις:",
                            value=g.get("notes", ""),
                            key=f"note_{week}_{day}_{idx}_{g['name']}",
                            height=75
                        )
                        if user_note != g.get("notes", ""):
                            st.session_state.my_gardens[idx]["notes"] = user_note
                            save_data()

                        col1, col2 = st.columns(2)
                        if col1.button("✏️ Αλλαγή", key=f"edit_{day}_{idx}"):
                            st.session_state.editing = idx
                            st.rerun()
                        if col2.button("🗑️ Διαγραφή", key=f"del_{day}_{idx}"):
                            st.session_state.my_gardens.pop(idx)
                            save_data()
                            st.rerun()
                        st.divider()

elif password != "":
    st.error("❌ Λάθος κωδικός πρόσβασης!")

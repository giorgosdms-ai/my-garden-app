import streamlit as st
import json
import os
import calendar
from datetime import datetime, timedelta

st.set_page_config(page_title="Πρόγραμμα Κήπων", page_icon="🌿")

DATA_FILE = "gardens_data.json"
PASSWORD_SECRET = "1619"

ALL_WEEKS = ["Εβδομάδα Α", "Εβδομάδα Β", "Εβδομάδα Γ", "Εβδομάδα Δ"]
FORTNIGHT_AC = ["Εβδομάδα Α", "Εβδομάδα Γ"] 
FORTNIGHT_BD = ["Εβδομάδα Β", "Εβδομάδα Δ"]
DAYS_GREEK = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή", "Σάββατο", "Κυριακή"]
MONTHS_SHORT = ["Ιαν", "Φεβ", "Μαρ", "Απρ", "Μαι", "Ιουν", "Ιουλ", "Αυγ", "Σεπ", "Οκτ", "Νοε", "Δεκ"]
MONTHS_FULL = ["Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάιος", "Ιούνιος", "Ιούλιος", "Αύγουστος", "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"]

# 🛠️ Συνάρτηση υπολογισμού εβδομάδας μήνα (Α, Β, Γ, Δ) βάσει ημέρας μήνα
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

password = st.text_input("🔑 Δώσε τον κωδικό πρόσβασης:", type="password")

if password == PASSWORD_SECRET:
    if "my_gardens" not in st.session_state or "extra_events" not in st.session_state:
        saved_g, saved_e = load_data()
        st.session_state.my_gardens = saved_g if saved_g is not None else get_default_gardens()
        st.session_state.extra_events = saved_e if saved_e is not None else []
        save_data()

    view_mode = st.radio("📌 **Επίλεξε Προβολή:**", ["📋 Εβδομαδιαίο Πρόγραμμα", "📅 Ημερολόγιο Μήνα & Εξτραδάκια"], horizontal=True)

    if view_mode == "📋 Εβδομαδιαίο Πρόγραμμα":
        st.subheader("🗓️ Εβδομαδιαίο Πρόγραμμα με Ημερομηνίες")
        
        # Επιλογή ημερομηνίας αναφοράς (προεπιλογή η σημερινή)
        ref_date = st.date_input("📆 **Επίλεξε Ημερομηνία για να δεις την Εβδομάδα της:**", datetime.now())
        
        # Υπολογισμός Δευτέρας της επιλεγμένης εβδομάδας
        monday_date = ref_date - timedelta(days=ref_date.weekday())
        
        st.info(f"📅 Εβδομάδα από **{monday_date.strftime('%d/%m/%Y')}** έως **{(monday_date + timedelta(days=6)).strftime('%d/%m/%Y')}**")

        search_query = st.text_input("🔍 **Αναζήτηση Κήπου:**", placeholder="Γράψε όνομα κήπου...")

        def render_month_picker(garden_idx, key_prefix):
            g = st.session_state.my_gardens[garden_idx]
            pm = g.get("paid_months", {})
            paid_list = [m for m in MONTHS_SHORT if pm.get(m, False)]
            status_text = "🟢 " + ", ".join(paid_list) if paid_list else "🔴 Καμία πληρωμή"
            
            st.markdown(f"**💶 Πληρωμές:** _{status_text}_")
            
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
                    st.divider()
        else:
            # Προβολή των 7 ημερών της συγκεκριμένης εβδομάδας
            for i in range(6): # Δευτέρα έως Σάββατο
                current_day_date = monday_date + timedelta(days=i)
                date_str = current_day_date.strftime("%Y-%m-%d")
                greek_day_name = DAYS_GREEK[i]
                week_code = get_week_name(current_day_date.day)

                # 1. Βρες τακτικούς κήπους
                matching_gardens = [
                    (idx, g) for idx, g in enumerate(st.session_state.my_gardens)
                    if g["day"] == greek_day_name and week_code in g.get("weeks", [])
                ]

                # 2. Βρες έκτακτα ραντεβού που ορίστηκαν ΑΚΡΙΒΩΣ για αυτή την ημερομηνία
                matching_extras = [
                    ev for ev in st.session_state.extra_events
                    if ev["date"] == date_str
                ]

                total_items = len(matching_gardens) + len(matching_extras)
                extra_badge = f" ⚡ [{len(matching_extras)} έκτακτα]" if matching_extras else ""
                
                header_title = f"📌 {greek_day_name} {current_day_date.strftime('%d/%m')} - ({week_code}){extra_badge}"

                with st.expander(header_title, expanded=bool(matching_extras)):
                    # Εμφάνιση Έκτακτων Εργασιών Πρώτα
                    if matching_extras:
                        st.markdown("⚡ **Έκτακτες Εργασίες Ημερομηνίας:**")
                        for ex in matching_extras:
                            st.warning(f"⏰ **{ex['time']}** | **{ex['title']}**\n\n_{ex.get('notes', '')}_")
                        st.divider()

                    # Εμφάνιση Τακτικών Κήπων
                    if not matching_gardens and not matching_extras:
                        st.write("*Δεν υπάρχουν προγραμματισμένες εργασίες.*")

                    for idx, g in matching_gardens:
                        weeks_str = ", ".join([w.replace("Εβδομάδα ", "") for w in g.get('weeks', [])])
                        st.checkbox(f"🌿 **{g['name']}**", key=f"chk_{date_str}_{idx}_{g['name']}")
                        render_month_picker(idx, f"main_{date_str}")
                        
                        user_note = st.text_area("📝 Σημειώσεις:", value=g.get("notes", ""), key=f"note_{date_str}_{idx}", height=70)
                        if user_note != g.get("notes", ""):
                            st.session_state.my_gardens[idx]["notes"] = user_note
                            save_data()
                        st.divider()

    else:
        # --- ΗΜΕΡΟΛΟΓΙΟ ΜΗΝΑ ---
        st.subheader("📅 Ημερολόγιο & Έκτακτα Ραντεβού")
        
        col_m, col_y = st.columns(2)
        selected_month_num = col_m.selectbox("Μήνας:", range(1, 13), index=datetime.now().month-1, format_func=lambda x: MONTHS_FULL[x-1])
        selected_year = col_y.number_input("Έτος:", value=datetime.now().year, step=1)

        with st.expander("➕ **Προσθήκη Νέου Εξτραδακίου**", expanded=True):
            ex_date = st.date_input("Ημερομηνία:", datetime.now())
            ex_time = st.time_input("Ώρα:", datetime.strptime("10:00", "%H:%M").time())
            ex_title = st.text_input("Περιγραφή / Όνομα:")
            ex_note = st.text_area("📝 Σημείωση (προαιρετικά):", height=60, key="cal_ex_note")

            if st.button("✅ Αποθήκευση στο Ημερολόγιο"):
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

        st.divider()

        num_days = calendar.monthrange(selected_year, selected_month_num)[1]

        for day_num in range(1, num_days + 1):
            day_dt = datetime(selected_year, selected_month_num, day_num)
            day_str = day_dt.strftime("%Y-%m-%d")
            greek_day_name = DAYS_GREEK[day_dt.weekday()]
            week_label = get_week_name(day_num)
            
            day_events = [e for e in st.session_state.extra_events if e["date"] == day_str]
            
            badge = f" ⚡ [{len(day_events)} εξτραδάκι/α]" if day_events else ""
            label = f"📆 {day_num} {MONTHS_SHORT[selected_month_num-1]} ({greek_day_name}) - [{week_label}]{badge}"

            with st.expander(label, expanded=bool(day_events)):
                if not day_events:
                    st.write("_Δεν υπάρχει κάποιο εξτραδάκι για αυτή τη μέρα._")
                else:
                    for ev_idx, ev in enumerate(day_events):
                        st.markdown(f"⏰ **Ώρα: {ev['time']}** - ⚡ **{ev['title']}**")
                        if ev.get("notes"):
                            st.caption(f"📝 {ev['notes']}")
                        
                        if st.button("🗑️ Διαγραφή", key=f"del_ev_{day_str}_{ev_idx}"):
                            st.session_state.extra_events.remove(ev)
                            save_data()
                            st.rerun()

elif password != "":
    st.error("❌ Λάθος κωδικός πρόσβασης!")

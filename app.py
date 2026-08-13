import streamlit as st

st.set_page_config(page_title="Πρόγραμμα Κήπων", page_icon="🌿")

if st.sidebar.button("⚠️ Καθαρισμός δεδομένων (Reset)"):
    st.session_state.clear()
    st.rerun()

st.title("🌿 Πρόγραμμα Κήπων 2026")

PASSWORD_SECRET = "1619"
password = st.text_input("🔑 Δώσε τον κωδικό πρόσβασης:", type="password")

ALL_WEEKS = ["Εβδομάδα Α", "Εβδομάδα Β", "Εβδομάδα Γ", "Εβδομάδα Δ"]
FORTNIGHT_AC = ["Εβδομάδα Α", "Εβδομάδα Γ"] 
FORTNIGHT_BD = ["Εβδομάδα Β", "Εβδομάδα Δ"]
DAYS = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή", "Σάββατο"]

MONTHS_SHORT = ["Ιαν", "Φεβ", "Μαρ", "Απρ", "Μαι", "Ιουν", "Ιουλ", "Αυγ", "Σεπ", "Οκτ", "Νοε", "Δεκ"]

if password == PASSWORD_SECRET:
    if "my_gardens" not in st.session_state:
        # Αρχικοποίηση - Όλοι οι μήνες ξεκινάνε ως μη πληρωμένοι (False)
        default_paid_months = {m: False for m in MONTHS_SHORT}
        
        st.session_state.my_gardens = [
            # --- ΔΕΥΤΕΡΑ ---
            {"name": "Αχιλλέας", "day": "Δευτέρα", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Ξανθος", "day": "Δευτέρα", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Αιγίνης", "day": "Δευτέρα", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Τεγεας", "day": "Δευτέρα", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Ιωαννιδης", "day": "Δευτέρα", "weeks": ["Εβδομάδα Α"], "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Πετραν", "day": "Δευτέρα", "weeks": ["Εβδομάδα Β"], "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Αγίας Λαύρας", "day": "Δευτέρα", "weeks": ["Εβδομάδα Γ"], "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "28ης", "day": "Δευτέρα", "weeks": ["Εβδομάδα Δ"], "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            
            # --- ΤΡΙΤΗ ---
            {"name": "Γλυφαδα", "day": "Τρίτη", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Αγιος Δημήτριος 1", "day": "Τρίτη", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Αγιος Δημήτριος 2", "day": "Τρίτη", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Βουλα", "day": "Τρίτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "βερα λω φαληρο", "day": "Τρίτη", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Πετρούλα", "day": "Τρίτη", "weeks": ["Εβδομάδα Α"], "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            
            # --- ΤΕΤΑΡΤΗ ---
            {"name": "Σταθης", "day": "Τετάρτη", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Μενιδι", "day": "Τετάρτη", "weeks": ALL_WEEKS, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Ανθουσων", "day": "Τετάρτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Μακης", "day": "Τετάρτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Αλέξανδρος", "day": "Τετάρτη", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Άνω Λιόσια", "day": "Τετάρτη", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Δίπλα από Στάθη", "day": "Τετάρτη", "weeks": ["Εβδομάδα Β"], "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Μεταμόρφωση", "day": "Τετάρτη", "weeks": ["Εβδομάδα Γ"], "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            
            # --- ΠΕΜΠΤΗ ---
            {"name": "Μετόχιο", "day": "Πέμπτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Μαρουσι", "day": "Πέμπτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Μικράς Ασιας 1", "day": "Πέμπτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Μικρας Ασιας 2", "day": "Πέμπτη", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "καβαλας", "day": "Πέμπτη", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Ροζελα", "day": "Πέμπτη", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "βερα λω ψυχικό", "day": "Πέμπτη", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            {"name": "Αλικη", "day": "Πέμπτη", "weeks": FORTNIGHT_BD, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
            
            # --- ΠΑΡΑΣΚΕΥΗ ---
            {"name": "Μάριος", "day": "Παρασκευή", "weeks": FORTNIGHT_AC, "notes": "", "paid_months": default_paid_months.copy(), "is_extra": False},
        ]

    # 🔍 Μπάρα Αναζήτησης
    search_query = st.text_input("🔍 **Αναζήτηση Κήπου / Εργασίας:**", placeholder="Γράψε όνομα κήπου...")

    week = st.radio("🗓️ **Επίλεξε Εβδομάδα:**", ALL_WEEKS, horizontal=True)

    # Συνάρτηση εμφάνισης πλέγματος μηνών 2026
    def render_month_picker(garden_idx, key_prefix):
        g = st.session_state.my_gardens[garden_idx]
        pm = g.get("paid_months", {m: False for m in MONTHS_SHORT})
        
        paid_list = [m for m, status in pm.items() if status]
        status_text = "🟢 Πληρωμένοι: " + ", ".join(paid_list) if paid_list else "🔴 Καμία πληρωμή"
        
        st.markdown(f"**💶 Πληρωμές 2026:** _{status_text}_")
        
        # 4 στήλες x 3 γραμμές για τους 12 μήνες
        cols = st.columns(4)
        for i, m in enumerate(MONTHS_SHORT):
            col = cols[i % 4]
            is_checked = pm.get(m, False)
            new_val = col.checkbox(m, value=is_checked, key=f"{key_prefix}_{m}_{garden_idx}")
            if new_val != is_checked:
                st.session_state.my_gardens[garden_idx]["paid_months"][m] = new_val
                st.rerun()

    if search_query.strip():
        st.subheader(f"🔎 Αποτελέσματα για: '{search_query}'")
        found = False
        for idx, g in enumerate(st.session_state.my_gardens):
            if search_query.lower() in g["name"].lower():
                found = True
                weeks_str = ", ".join([w.replace("Εβδομάδα ", "") for w in g.get('weeks', [])])
                badge = "⚡ (Εξτραδάκι)" if g.get("is_extra") else ""
                st.write(f"📌 **{g['name']}** {badge} | Ημέρα: **{g['day']}** | Εβδ: **{weeks_str}**")
                
                render_month_picker(idx, "search")
                
                note = st.text_area("📝 Σημειώσεις:", value=g.get("notes", ""), key=f"search_note_{idx}", height=70)
                st.session_state.my_gardens[idx]["notes"] = note
                st.divider()
        if not found:
            st.info("Δεν βρέθηκε κήπος με αυτό το όνομα.")
    else:
        for day in DAYS:
            matching_gardens = [
                (idx, g) for idx, g in enumerate(st.session_state.my_gardens)
                if g["day"] == day and week in g.get("weeks", [])
            ]
            
            with st.expander(f"📌 {day} ({len(matching_gardens)} κήποι/εργασίες)"):
                if not matching_gardens:
                    st.write("*Δεν υπάρχουν κήποι ή εργασίες.*")
                for idx, g in matching_gardens:
                    weeks_str = ", ".join([w.replace("Εβδομάδα ", "") for w in g.get('weeks', [])])
                    extra_tag = " ⚡ [ΕΞΤΡΑΔΑΚΙ]" if g.get("is_extra") else ""
                    
                    st.checkbox(f"🌿 **{g['name']}**{extra_tag} (Εβδ: {weeks_str})", key=f"chk_{week}_{day}_{idx}_{g['name']}")
                    
                    # Εμφάνιση Μηνών Πληρωμής
                    render_month_picker(idx, f"main_{week}_{day}")

                    # Σημειώσεις
                    user_note = st.text_area(
                        "📝 Σημειώσεις:",
                        value=g.get("notes", ""),
                        key=f"note_{week}_{day}_{idx}_{g['name']}",
                        height=75,
                        placeholder="Γράψε σημειώσεις εδώ..."
                    )
                    if user_note != g.get("notes", ""):
                        st.session_state.my_gardens[idx]["notes"] = user_note

                    col1, col2 = st.columns(2)
                    if col1.button("✏️ Αλλαγή", key=f"edit_{day}_{idx}"):
                        st.session_state.editing = idx
                        st.rerun()
                    if col2.button("🗑️ Διαγραφή", key=f"del_{day}_{idx}"):
                        st.session_state.my_gardens.pop(idx)
                        st.rerun()
                    st.divider()

    # Φόρμα Επεξεργασίας
    if "editing" in st.session_state:
        idx = st.session_state.editing
        if idx < len(st.session_state.my_gardens):
            g = st.session_state.my_gardens[idx]
            st.info(f"✏️ Επεξεργασία: **{g['name']}**")
            new_name = st.text_input("Όνομα:", value=g["name"])
            new_day = st.selectbox("Ημέρα:", DAYS, index=DAYS.index(g["day"]))
            new_weeks = st.multiselect("Εβδομάδες:", ALL_WEEKS, default=g.get("weeks", ALL_WEEKS))
            new_notes = st.text_area("Σημειώσεις:", value=g.get("notes", ""))
            new_extra = st.checkbox("⚡ Είναι έκτακτο / εξτραδάκι", value=g.get("is_extra", False))
            
            c_save, c_cancel = st.columns(2)
            if c_save.button("✅ Αποθήκευση"):
                if new_weeks:
                    st.session_state.my_gardens[idx]["name"] = new_name
                    st.session_state.my_gardens[idx]["day"] = new_day
                    st.session_state.my_gardens[idx]["weeks"] = new_weeks
                    st.session_state.my_gardens[idx]["notes"] = new_notes
                    st.session_state.my_gardens[idx]["is_extra"] = new_extra
                    del st.session_state.editing
                    st.rerun()
            if c_cancel.button("❌ Ακύρωση"):
                del st.session_state.editing
                st.rerun()

    # ⚡ Προσθήκη Έκτακτου / Εξτραδακίου
    st.markdown("---")
    with st.expander("⚡ Προσθήκη Έκτακτης Εργασίας / Εξτραδάκι"):
        extra_name = st.text_input("Περιγραφή Εργασίας / Κήπου:", key="ex_name")
        extra_day = st.selectbox("Ημέρα:", DAYS, key="ex_day")
        extra_weeks = st.multiselect("Εβδομάδες που αφορά:", ALL_WEEKS, default=[week], key="ex_weeks")
        extra_notes = st.text_area("Σημειώσεις:", key="ex_notes")
        
        if st.button("➕ Προσθήκη Εξτραδακίου"):
            if extra_name.strip() and extra_weeks:
                st.session_state.my_gardens.append({
                    "name": extra_name,
                    "day": extra_day,
                    "weeks": extra_weeks,
                    "notes": extra_notes,
                    "paid_months": {m: False for m in MONTHS_SHORT},
                    "is_extra": True
                })
                st.rerun()

    # ➕ Προσθήκη Τακτικού Κήπου
    with st.expander("➕ Προσθήκη Νέου Τακτικού Κήπου"):
        add_name = st.text_input("Όνομα:")
        add_day = st.selectbox("Ημέρα:", DAYS, key="add_day")
        add_weeks = st.multiselect("Εβδομάδες:", ALL_WEEKS, default=ALL_WEEKS, key="add_weeks")
        add_notes = st.text_area("Σημειώσεις:", key="add_notes")
        
        if st.button("➕ Προσθήκη Κήπου"):
            if add_name.strip() and add_weeks:
                st.session_state.my_gardens.append({
                    "name": add_name,
                    "day": add_day,
                    "weeks": add_weeks,
                    "notes": add_notes,
                    "paid_months": {m: False for m in MONTHS_SHORT},
                    "is_extra": False
                })
                st.rerun()

elif password != "":
    st.error("❌ Λάθος κωδικός πρόσβασης!")

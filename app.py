import streamlit as st

st.set_page_config(page_title="Πρόγραμμα Κήπων", page_icon="🌿")

if st.sidebar.button("⚠️ Καθαρισμός δεδομένων (Reset)"):
    st.session_state.clear()
    st.rerun()

st.title("🌿 Πρόγραμμα Κήπων")

PASSWORD_SECRET = "1619"
password = st.text_input("🔑 Δώσε τον κωδικό πρόσβασης:", type="password")

ALL_WEEKS = ["Εβδομάδα Α", "Εβδομάδα Β", "Εβδομάδα Γ", "Εβδομάδα Δ"]
FORTNIGHT_AC = ["Εβδομάδα Α", "Εβδομάδα Γ"] 
FORTNIGHT_BD = ["Εβδομάδα Β", "Εβδομάδα Δ"]
DAYS = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή"]

if password == PASSWORD_SECRET:
    if "my_gardens" not in st.session_state:
        st.session_state.my_gardens = [
            # --- ΔΕΥΤΕΡΑ ---
            {"name": "Αχιλλέας", "day": "Δευτέρα", "weeks": ALL_WEEKS, "notes": ""},
            {"name": "Ξανθος", "day": "Δευτέρα", "weeks": FORTNIGHT_AC, "notes": ""},
            {"name": "Αιγίνης", "day": "Δευτέρα", "weeks": FORTNIGHT_AC, "notes": ""},
            {"name": "Τεγεας", "day": "Δευτέρα", "weeks": FORTNIGHT_BD, "notes": ""},
            {"name": "Ιωαννιδης", "day": "Δευτέρα", "weeks": ["Εβδομάδα Α"], "notes": ""},
            {"name": "Πετραν", "day": "Δευτέρα", "weeks": ["Εβδομάδα Β"], "notes": ""},
            {"name": "Αγίας Λαύρας", "day": "Δευτέρα", "weeks": ["Εβδομάδα Γ"], "notes": ""},
            {"name": "28ης", "day": "Δευτέρα", "weeks": ["Εβδομάδα Δ"], "notes": ""},
            
            # --- ΤΡΙΤΗ ---
            {"name": "Γλυφαδα", "day": "Τρίτη", "weeks": ALL_WEEKS, "notes": ""},
            {"name": "Αγιος Δημήτριος 1", "day": "Τρίτη", "weeks": ALL_WEEKS, "notes": ""},
            {"name": "Αγιος Δημήτριος 2", "day": "Τρίτη", "weeks": ALL_WEEKS, "notes": ""},
            {"name": "Βουλα", "day": "Τρίτη", "weeks": FORTNIGHT_AC, "notes": ""},
            {"name": "βερα λω φαληρο", "day": "Τρίτη", "weeks": FORTNIGHT_BD, "notes": ""},
            {"name": "Πετρούλα", "day": "Τρίτη", "weeks": ["Εβδομάδα Α"], "notes": ""},
            
            # --- ΤΕΤΑΡΤΗ ---
            {"name": "Σταθης", "day": "Τετάρτη", "weeks": ALL_WEEKS, "notes": ""},
            {"name": "Μενιδι", "day": "Τετάρτη", "weeks": ALL_WEEKS, "notes": ""},
            {"name": "Ανθουσων", "day": "Τετάρτη", "weeks": FORTNIGHT_AC, "notes": ""},
            {"name": "Μακης", "day": "Τετάρτη", "weeks": FORTNIGHT_AC, "notes": ""},
            {"name": "Αλέξανδρος", "day": "Τετάρτη", "weeks": FORTNIGHT_BD, "notes": ""},
            {"name": "Άνω Λιόσια", "day": "Τετάρτη", "weeks": FORTNIGHT_BD, "notes": ""},
            {"name": "Δίπλα από Στάθη", "day": "Τετάρτη", "weeks": ["Εβδομάδα Β"], "notes": ""},
            {"name": "Μεταμόρφωση", "day": "Τετάρτη", "weeks": ["Εβδομάδα Γ"], "notes": ""},
            
            # --- ΠΕΜΠΤΗ ---
            {"name": "Μετόχιο", "day": "Πέμπτη", "weeks": FORTNIGHT_AC, "notes": ""},
            {"name": "Μαρουσι", "day": "Πέμπτη", "weeks": FORTNIGHT_AC, "notes": ""},
            {"name": "Μικράς Ασιας 1", "day": "Πέμπτη", "weeks": FORTNIGHT_AC, "notes": ""},
            {"name": "Μικρας Ασιας 2", "day": "Πέμπτη", "weeks": FORTNIGHT_AC, "notes": ""},
            {"name": "καβαλας", "day": "Πέμπτη", "weeks": FORTNIGHT_BD, "notes": ""},
            {"name": "Ροζελα", "day": "Πέμπτη", "weeks": FORTNIGHT_BD, "notes": ""},
            {"name": "βερα λω ψυχικό", "day": "Πέμπτη", "weeks": FORTNIGHT_BD, "notes": ""},
            {"name": "Αλικη", "day": "Πέμπτη", "weeks": FORTNIGHT_BD, "notes": ""},
            
            # --- ΠΑΡΑΣΚΕΥΗ ---
            {"name": "Μάριος", "day": "Παρασκευή", "weeks": FORTNIGHT_AC, "notes": ""},
        ]

    week = st.radio("🗓️ **Επίλεξε Εβδομάδα:**", ALL_WEEKS, horizontal=True)

    for day in DAYS:
        matching_gardens = [
            (idx, g) for idx, g in enumerate(st.session_state.my_gardens)
            if g["day"] == day and week in g.get("weeks", [])
        ]
        
        with st.expander(f"📌 {day} ({len(matching_gardens)} κήποι)"):
            if not matching_gardens:
                st.write("*Δεν υπάρχουν κήποι.*")
            for idx, g in matching_gardens:
                weeks_str = ", ".join([w.replace("Εβδομάδα ", "") for w in g['weeks']])
                
                # Checkbox Κήπου
                st.checkbox(f"🌿 **{g['name']}** (Εβδ: {weeks_str})", key=f"chk_{week}_{day}_{idx}_{g['name']}")
                
                # Πεδίο για Σημειώσεις κάτω από κάθε κήπο
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
            
            c_save, c_cancel = st.columns(2)
            if c_save.button("✅ Αποθήκευση"):
                if new_weeks:
                    st.session_state.my_gardens[idx] = {
                        "name": new_name,
                        "day": new_day,
                        "weeks": new_weeks,
                        "notes": new_notes
                    }
                    del st.session_state.editing
                    st.rerun()
            if c_cancel.button("❌ Ακύρωση"):
                del st.session_state.editing
                st.rerun()

    # Φόρμα Προσθήκης
    st.markdown("---")
    with st.expander("➕ Προσθήκη Νέου Κήπου"):
        add_name = st.text_input("Όνομα:")
        add_day = st.selectbox("Ημέρα:", DAYS, key="add_day")
        add_weeks = st.multiselect("Εβδομάδες:", ALL_WEEKS, default=ALL_WEEKS, key="add_weeks")
        add_notes = st.text_area("Σημειώσεις (προαιρετικό):", key="add_notes")
        
        if st.button("➕ Προσθήκη"):
            if add_name.strip() and add_weeks:
                st.session_state.my_gardens.append({
                    "name": add_name,
                    "day": add_day,
                    "weeks": add_weeks,
                    "notes": add_notes
                })
                st.rerun()

elif password != "":
    st.error("❌ Λάθος κωδικός πρόσβασης!")

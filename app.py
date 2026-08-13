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
            {"name": "Αχιλλέας", "day": "Δευτέρα", "weeks": ALL_WEEKS},
            {"name": "Ξανθος", "day": "Δευτέρα", "weeks": FORTNIGHT_AC},
            {"name": "Αιγίνης", "day": "Δευτέρα", "weeks": FORTNIGHT_AC},
            {"name": "Τεγεας", "day": "Δευτέρα", "weeks": FORTNIGHT_BD},
            {"name": "Ιωαννιδης", "day": "Δευτέρα", "weeks": ["Εβδομάδα Α"]},
            {"name": "Πετραν", "day": "Δευτέρα", "weeks": ["Εβδομάδα Β"]},
            {"name": "Αγίας Λαύρας", "day": "Δευτέρα", "weeks": ["Εβδομάδα Γ"]},
            {"name": "28ης", "day": "Δευτέρα", "weeks": ["Εβδομάδα Δ"]},
            
            # --- ΤΡΙΤΗ ---
            {"name": "Γλυφαδα", "day": "Τρίτη", "weeks": ALL_WEEKS},
            {"name": "Αγιος Δημήτριος 1", "day": "Τρίτη", "weeks": ALL_WEEKS},
            {"name": "Αγιος Δημήτριος 2", "day": "Τρίτη", "weeks": ALL_WEEKS},
            {"name": "Βουλα", "day": "Τρίτη", "weeks": FORTNIGHT_AC},
            {"name": "βερα λω φαληρο", "day": "Τρίτη", "weeks": FORTNIGHT_BD},
            {"name": "Πετρούλα", "day": "Τρίτη", "weeks": ["Εβδομάδα Α"]},
            
            # --- ΤΕΤΑΡΤΗ ---
            {"name": "Σταθης", "day": "Τετάρτη", "weeks": ALL_WEEKS},
            {"name": "Μενιδι", "day": "Τετάρτη", "weeks": ALL_WEEKS},
            {"name": "Ανθουσων", "day": "Τετάρτη", "weeks": FORTNIGHT_AC},
            {"name": "Μακης", "day": "Τετάρτη", "weeks": FORTNIGHT_AC},
            {"name": "Αλέξανδρος", "day": "Τετάρτη", "weeks": FORTNIGHT_BD},
            {"name": "Άνω Λιόσια", "day": "Τετάρτη", "weeks": FORTNIGHT_BD},
            {"name": "Δίπλα από Στάθη", "day": "Τετάρτη", "weeks": ["Εβδομάδα Β"]},
            {"name": "Μεταμόρφωση", "day": "Τετάρτη", "weeks": ["Εβδομάδα Γ"]},
            
            # --- ΠΕΜΠΤΗ ---
            {"name": "Μετόχιο", "day": "Πέμπτη", "weeks": FORTNIGHT_AC},
            {"name": "Μαρουσι", "day": "Πέμπτη", "weeks": FORTNIGHT_AC},
            {"name": "Μικράς Ασιας 1", "day": "Πέμπτη", "weeks": FORTNIGHT_AC},
            {"name": "Μικρας Ασιας 2", "day": "Πέμπτη", "weeks": FORTNIGHT_AC},
            {"name": "καβαλας", "day": "Πέμπτη", "weeks": FORTNIGHT_BD},
            {"name": "Ροζελα", "day": "Πέμπτη", "weeks": FORTNIGHT_BD},
            {"name": "βερα λω ψυχικό", "day": "Πέμπτη", "weeks": FORTNIGHT_BD},
            {"name": "Αλικη", "day": "Πέμπτη", "weeks": FORTNIGHT_BD},
            
            # --- ΠΑΡΑΣΚΕΥΗ ---
            {"name": "Μάριος", "day": "Παρασκευή", "weeks": FORTNIGHT_AC},
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
                st.checkbox(f"🌿 **{g['name']}** (Εβδ: {weeks_str})", key=f"chk_{week}_{day}_{idx}_{g['name']}")
                
                col1, col2 = st.columns(2)
                if col1.button("✏️ Αλλαγή", key=f"edit_{day}_{idx}"):
                    st.session_state.editing = idx
                    st.rerun()
                if col2.button("🗑️ Διαγραφή", key=f"del_{day}_{idx}"):
                    st.session_state.my_gardens.pop(idx)
                    st.rerun()
                st.divider()

    if "editing" in st.session_state:
        idx = st.session_state.editing
        g = st.session_state.my_gardens[idx]
        st.info(f"✏️ Επεξεργασία: **{g['name']}**")
        new_name = st.text_input("Όνομα:", value=g["name"])
        new_day = st.selectbox("Ημέρα:", DAYS, index=DAYS.index(g["day"]))
        new_weeks = st.multiselect("Εβδομάδες:", ALL_WEEKS, default=g.get("weeks", ALL_WEEKS))
        
        c_save, c_cancel = st.columns(2)
        if c_save.button("✅ Αποθήκευση"):
            st.session_state.my_gardens[idx] = {"name": new_name, "day": new_day, "weeks": new_weeks}
            del st.session_state.editing
            st.rerun()
        if c_cancel.button("❌ Ακύρωση"):
            del st.session_state.editing
            st.rerun()

    st.markdown("---")
    with st.expander("➕ Προσθήκη"):
        add_name = st.text_input("Όνομα:")
        add_day = st.selectbox("Ημέρα:", DAYS)
        add_weeks = st.multiselect("Εβδομάδες:", ALL_WEEKS)
        if st.button("➕ Προσθήκη"):
            if add_name and add_weeks:
                st.session_state.my_gardens.append({"name": add_name, "day": add_day, "weeks": add_weeks})
                st.rerun()
elif password != "":
    st.error("❌ Λάθος!")

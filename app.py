import streamlit as st

st.set_page_config(page_title="Πρόγραμμα Κήπων", page_icon="🌿")

# Κουμπί επαναφοράς στην αριστερή μπάρα (Sidebar)
if st.sidebar.button("⚠️ Καθαρισμός δεδομένων (Reset)"):
    st.session_state.clear()
    st.rerun()

st.title("🌿 Πρόγραμμα Κήπων")

PASSWORD_SECRET = "1619"
password = st.text_input("🔑 Δώσε τον κωδικό πρόσβασης:", type="password")

ALL_WEEKS = ["Εβδομάδα Α", "Εβδομάδα Β", "Εβδομάδα Γ", "Εβδομάδα Δ"]
FORTNIGHT = ["Εβδομάδα Α", "Εβδομάδα Γ"]  # 2 φορές τον μήνα
DAYS = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή"]

if password == PASSWORD_SECRET:
    # Πλήρης αρχική λίστα με τις νέες ρυθμίσεις σου
    if "my_gardens" not in st.session_state:
        st.session_state.my_gardens = [
            # --- ΔΕΥΤΕΡΑ ---
            {"name": "Αχιλλέας", "day": "Δευτέρα", "weeks": ALL_WEEKS}, # Κάθε εβδομάδα
            {"name": "Ξανθος", "day": "Δευτέρα", "weeks": FORTNIGHT},
            {"name": "Ιωαννιδης", "day": "Δευτέρα", "weeks": ["Εβδομάδα Α"]}, # 1 φορά τον μήνα
            {"name": "Αιγίνης", "day": "Δευτέρα", "weeks": FORTNIGHT},
            {"name": "Τεγεας", "day": "Δευτέρα", "weeks": FORTNIGHT},
            {"name": "Πετραν", "day": "Δευτέρα", "weeks": ["Εβδομάδα Α"]}, # 1 φορά τον μήνα
            {"name": "Αγίας Λαύρας", "day": "Δευτέρα", "weeks": ["Εβδομάδα Α"]}, # 1 φορά τον μήνα
            {"name": "28ης", "day": "Δευτέρα", "weeks": ["Εβδομάδα Α"]}, # 1 φορά τον μήνα
            
            # --- ΤΡΙΤΗ ---
            {"name": "Γλυφαδα", "day": "Τρίτη", "weeks": ALL_WEEKS}, # Κάθε εβδομάδα
            {"name": "Αγιος Δημήτριος 1", "day": "Τρίτη", "weeks": ALL_WEEKS}, # Κάθε εβδομάδα
            {"name": "Αγιος Δημήτριος 2", "day": "Τρίτη", "weeks": ALL_WEEKS}, # Κάθε εβδομάδα
            {"name": "Βουλα", "day": "Τρίτη", "weeks": FORTNIGHT},
            {"name": "βερα λω φαληρο", "day": "Τρίτη", "weeks": FORTNIGHT},
            {"name": "Πετρούλα", "day": "Τρίτη", "weeks": ["Εβδομάδα Α"]}, # 1 φορά τον μήνα
            
            # --- ΤΕΤΑΡΤΗ ---
            {"name": "Σταθης", "day": "Τετάρτη", "weeks": ALL_WEEKS}, # Κάθε εβδομάδα
            {"name": "Μενιδι", "day": "Τετάρτη", "weeks": ALL_WEEKS}, # Κάθε εβδομάδα
            {"name": "Δίπλα από Στάθη", "day": "Τετάρτη", "weeks": ["Εβδομάδα Α"]}, # 1 φορά τον μήνα
            {"name": "Ανθουσων", "day": "Τετάρτη", "weeks": FORTNIGHT},
            {"name": "Μακης", "day": "Τετάρτη", "weeks": FORTNIGHT},
            {"name": "Αλέξανδρος", "day": "Τετάρτη", "weeks": FORTNIGHT},
            {"name": "Μεταμόρφωση", "day": "Τετάρτη", "weeks": FORTNIGHT},
            {"name": "Άνω Λιόσια", "day": "Τετάρτη", "weeks": FORTNIGHT},
            
            # --- ΠΕΜΠΤΗ ---
            {"name": "Μετόχιο", "day": "Πέμπτη", "weeks": FORTNIGHT},
            {"name": "Μαρουσι", "day": "Πέμπτη", "weeks": FORTNIGHT},
            {"name": "Μικράς Ασιας 1", "day": "Πέμπτη", "weeks": FORTNIGHT},
            {"name": "Μικρας Ασιας 2", "day": "Πέμπτη", "weeks": FORTNIGHT},
            {"name": "καβαλας", "day": "Πέμπτη", "weeks": FORTNIGHT},
            {"name": "Ροζελα", "day": "Πέμπτη", "weeks": FORTNIGHT},
            {"name": "βερα λω ψυχικό", "day": "Πέμπτη", "weeks": FORTNIGHT},
            {"name": "Αλικη", "day": "Πέμπτη", "weeks": FORTNIGHT},
            
            # --- ΠΑΡΑΣΚΕΥΗ ---
            {"name": "Μάριος", "day": "Παρασκευή", "weeks": ["Εβδομάδα Α"]}, # 1 φορά τον μήνα
        ]

    # Επιλογή Εβδομάδας για προβολή
    week = st.radio("🗓️ **Επίλεξε Εβδομάδα:**", ALL_WEEKS, horizontal=True)

    # Εμφάνιση ανά ημέρα
    for day in DAYS:
        matching_gardens = [
            (idx, g) for idx, g in enumerate(st.session_state.my_gardens)
            if g["day"] == day and week in g.get("weeks", [])
        ]
        
        with st.expander(f"📌 {day} ({len(matching_gardens)} κήποι)"):
            if not matching_gardens:
                st.write("*Δεν υπάρχουν κήποι για αυτή την εβδομάδα.*")
            for idx, g in matching_gardens:
                weeks_str = ", ".join([w.replace("Εβδομάδα ", "") for w in g['weeks']])
                
                # Checkbox για σημείωση
                st.checkbox(f"🌿 **{g['name']}** (Εβδ: {weeks_str})", key=f"chk_{week}_{day}_{idx}_{g['name']}")
                
                # Κουμπιά Αλλαγής και Διαγραφής
                col1, col2 = st.columns(2)
                if col1.button("✏️ Αλλαγή", key=f"edit_{day}_{idx}"):
                    st.session_state.editing = idx
                    st.rerun()
                if col2.button("🗑️ Διαγραφή", key=f"del_{day}_{idx}"):
                    st.session_state.my_gardens.pop(idx)
                    st.rerun()
                st.divider()

    # Φόρμα Επεξεργασίας Κήπου
    if "editing" in st.session_state:
        idx = st.session_state.editing
        if idx < len(st.session_state.my_gardens):
            g = st.session_state.my_gardens[idx]
            st.info(f"✏️ Επεξεργασία κήπου: **{g['name']}**")
            new_name = st.text_input("Όνομα:", value=g["name"])
            new_day = st.selectbox("Ημέρα:", DAYS, index=DAYS.index(g["day"]))
            
            new_weeks = st.multiselect(
                "Σε ποιες εβδομάδες εμφανίζεται;", 
                ALL_WEEKS, 
                default=g.get("weeks", ALL_WEEKS)
            )
            
            c_save, c_cancel = st.columns(2)
            if c_save.button("✅ Αποθήκευση"):
                if new_weeks:
                    st.session_state.my_gardens[idx] = {"name": new_name, "day": new_day, "weeks": new_weeks}
                    del st.session_state.editing
                    st.rerun()
                else:
                    st.error("Πρέπει να διαλέξεις τουλάχιστον μία εβδομάδα!")
            if c_cancel.button("❌ Ακύρωση"):
                del st.session_state.editing
                st.rerun()

    # Φόρμα Προσθήκης Νέου Κήπου
    st.markdown("---")
    with st.expander("➕ Προσθήκη Νέου Κήπου"):
        add_name = st.text_input("Όνομα κήπου:")
        add_day = st.selectbox("Ημέρα:", DAYS, key="add_day")
        add_weeks = st.multiselect("Εβδομάδες που πηγαίνεις:", ALL_WEEKS, default=ALL_WEEKS, key="add_weeks")
        
        if st.button("➕ Προσθήκη"):
            if add_name.strip() and add_weeks:
                st.session_state.my_gardens.append({"name": add_name, "day": add_day, "weeks": add_weeks})
                st.success(f"Ο κήπος '{add_name}' προστέθηκε!")
                st.rerun()
            elif not add_weeks:
                st.warning("Παρακαλώ επίλεξε τουλάχιστον μία εβδομάδα.")

elif password != "":
    st.error("❌ Λάθος κωδικός πρόσβασης!")

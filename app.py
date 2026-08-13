import streamlit as st

st.set_page_config(page_title="Πρόγραμμα Κήπων", page_icon="🌿")

# Κουμπί επαναφοράς στην αριστερή μπάρα (αν ποτέ χρειαστεί)
if st.sidebar.button("⚠️ Καθαρισμός δεδομένων (Reset)"):
    st.session_state.clear()
    st.rerun()

st.title("🌿 Πρόγραμμα Κήπων")

PASSWORD_SECRET = "1619"
password = st.text_input("🔑 Δώσε τον κωδικό πρόσβασης:", type="password")

if password == PASSWORD_SECRET:
    # Επιλογές συχνότητας
    freq_options = ["Εβδομαδιαίος", "Εβδομάδα Α", "Εβδομάδα Β", "Μία φορά τον μήνα"]

    # Πλήρης αρχική λίστα κήπων
    if "my_gardens" not in st.session_state:
        st.session_state.my_gardens = [
            # Δευτέρα
            {"name": "Αχιλλέας", "day": "Δευτέρα", "freq": "Εβδομαδιαίος"},
            {"name": "Ξανθος", "day": "Δευτέρα", "freq": "Εβδομαδιαίος"},
            {"name": "Ιωαννιδης", "day": "Δευτέρα", "freq": "Εβδομάδα Α"},
            {"name": "Αιγίνης", "day": "Δευτέρα", "freq": "Εβδομαδιαίος"},
            {"name": "Τεγεας", "day": "Δευτέρα", "freq": "Εβδομαδιαίος"},
            # Τρίτη
            {"name": "Βουλα", "day": "Τρίτη", "freq": "Εβδομαδιαίος"},
            {"name": "Γλυφαδα", "day": "Τρίτη", "freq": "Εβδομαδιαίος"},
            {"name": "Αγιος Δημήτριος 1", "day": "Τρίτη", "freq": "Εβδομαδιαίος"},
            {"name": "Αγιος Δημήτριος 2", "day": "Τρίτη", "freq": "Εβδομαδιαίος"},
            {"name": "βερα λω φαληρο", "day": "Τρίτη", "freq": "Εβδομαδιαίος"},
            # Τετάρτη
            {"name": "Σταθης", "day": "Τετάρτη", "freq": "Εβδομαδιαίος"},
            {"name": "Ανθουσων", "day": "Τετάρτη", "freq": "Εβδομαδιαίος"},
            {"name": "Μενιδι", "day": "Τετάρτη", "freq": "Εβδομαδιαίος"},
            {"name": "Μακης", "day": "Τετάρτη", "freq": "Εβδομαδιαίος"},
            {"name": "Αλέξανδρος", "day": "Τετάρτη", "freq": "Εβδομαδιαίος"},
            {"name": "Μεταμόρφωση", "day": "Τετάρτη", "freq": "Εβδομαδιαίος"},
            # Πέμπτη
            {"name": "Μετόχιο", "day": "Πέμπτη", "freq": "Εβδομαδιαίος"},
            {"name": "Μαρουσι", "day": "Πέμπτη", "freq": "Εβδομαδιαίος"},
            {"name": "Μικράς Ασιας 1", "day": "Πέμπτη", "freq": "Εβδομαδιαίος"},
            {"name": "Μικρας Ασιας 2", "day": "Πέμπτη", "freq": "Εβδομαδιαίος"},
            {"name": "καβαλας", "day": "Πέμπτη", "freq": "Εβδομαδιαίος"},
            {"name": "Ροζελα", "day": "Πέμπτη", "freq": "Εβδομαδιαίος"},
            {"name": "βερα λω ψυχικό", "day": "Πέμπτη", "freq": "Εβδομαδιαίος"},
            {"name": "Αλικη", "day": "Πέμπτη", "freq": "Εβδομαδιαίος"},
            # Παρασκευή
            {"name": "Τάκης", "day": "Παρασκευή", "freq": "Εβδομαδιαίος"},
            {"name": "Γεωργία", "day": "Παρασκευή", "freq": "Εβδομαδιαίος"},
            {"name": "Μάριος", "day": "Παρασκευή", "freq": "Εβδομαδιαίος"},
        ]

    # Επιλογή Εβδομάδας
    week = st.radio("🗓️ **Επίλεξε Εβδομάδα:**", ["Εβδομάδα Α", "Εβδομάδα Β"], horizontal=True)
    days = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή"]

    # Εμφάνιση ανά ημέρα
    for day in days:
        matching_gardens = [
            (idx, g) for idx, g in enumerate(st.session_state.my_gardens)
            if g["day"] == day and (g["freq"] == "Εβδομαδιαίος" or g["freq"] == week or g["freq"] == "Μία φορά τον μήνα")
        ]
        
        with st.expander(f"📌 {day} ({len(matching_gardens)} κήποι)"):
            if not matching_gardens:
                st.write("*Δεν υπάρχουν κήποι για αυτή την ημέρα.*")
            for idx, g in matching_gardens:
                # Checkbox για σημείωση
                st.checkbox(f"🌿 {g['name']} ({g['freq']})", key=f"chk_{week}_{day}_{idx}_{g['name']}")
                
                # Κουμπιά Διαχείρισης
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
            st.info(f"✏️ Επεξεργασία κήπου: **{g['name']}**")
            new_name = st.text_input("Όνομα:", value=g["name"])
            new_day = st.selectbox("Ημέρα:", days, index=days.index(g["day"]))
            new_freq = st.selectbox("Συχνότητα:", freq_options, index=freq_options.index(g["freq"]))
            
            c_save, c_cancel = st.columns(2)
            if c_save.button("✅ Αποθήκευση"):
                st.session_state.my_gardens[idx] = {"name": new_name, "day": new_day, "freq": new_freq}
                del st.session_state.editing
                st.rerun()
            if c_cancel.button("❌ Ακύρωση"):
                del st.session_state.editing
                st.rerun()

    # Φόρμα Προσθήκης Νέου Κήπου
    st.markdown("---")
    with st.expander("➕ Προσθήκη Νέου Κήπου"):
        add_name = st.text_input("Όνομα κήπου:")
        add_day = st.selectbox("Ημέρα:", days, key="add_day")
        add_freq = st.selectbox("Συχνότητα:", freq_options, key="add_freq")
        if st.button("➕ Προσθήκη"):
            if add_name.strip():
                st.session_state.my_gardens.append({"name": add_name, "day": add_day, "freq": add_freq})
                st.success(f"Ο κήπος '{add_name}' προστέθηκε!")
                st.rerun()

elif password != "":
    st.error("❌ Λάθος κωδικός πρόσβασης!")

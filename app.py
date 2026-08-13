import streamlit as st

st.set_page_config(page_title="Πρόγραμμα Κήπων", page_icon="🌿")
st.title("🌿 Πρόγραμμα Κήπων")

# 1. Ασφάλεια - Κωδικός
PASSWORD_SECRET = "1619"
password = st.text_input("🔑 Δώσε τον κωδικό πρόσβασης:", type="password")

if password == PASSWORD_SECRET:
    # 2. Λίστα με όλους τους κήπους σου
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

    # 3. Επιλογή Εβδομάδας
    week = st.radio("🗓️ **Επίλεξε Εβδομάδα:**", ["Εβδομάδα Α", "Εβδομάδα Β"], horizontal=True)
    st.subheader(f"📋 Πρόγραμμα: {week}")

    days = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή"]

    # 4. Εμφάνιση Προγράμματος
    for day in days:
        day_gardens = [
            g for g in st.session_state.my_gardens
            if g["day"] == day and (g["freq"] == "Εβδομαδιαίος" or g["freq"] == week)
        ]
        
        with st.expander(f"📌 {day} ({len(day_gardens)} κήποι)"):
            if not day_gardens:
                st.write("*Δεν υπάρχουν κήποι για αυτή την ημέρα.*")
            for idx, g in enumerate(day_gardens):
                st.checkbox(f"🌿 {g['name']} ({g['freq']})", key=f"chk_{week}_{day}_{idx}_{g['name']}")
                
                # Κουμπιά Διαχείρισης
                col_e, col_d = st.columns(2)
                if col_e.button(f"✏️ Αλλαγή", key=f"ed_{week}_{day}_{idx}_{g['name']}"):
                    st.session_state.editing_garden = g
                    st.rerun()
                if col_d.button(f"🗑️ Διαγραφή", key=f"del_{week}_{day}_{idx}_{g['name']}"):
                    st.session_state.my_gardens.remove(g)
                    st.rerun()
                st.divider()

    # 5. Φόρμα Επεξεργασίας (εμφανίζεται μόνο όταν πατάς "✏️ Αλλαγή")
    if "editing_garden" in st.session_state:
        g = st.session_state.editing_garden
        st.info(f"✏️ Επεξεργάζεσαι τον κήπο: **{g['name']}**")
        new_name = st.text_input("Όνομα:", value=g["name"])
        new_day = st.selectbox("Ημέρα:", days, index=days.index(g["day"]))
        new_freq = st.selectbox("Συχνότητα:", ["Εβδομαδιαίος", "Εβδομάδα Α", "Εβδομάδα Β"], index=["Εβδομαδιαίος", "Εβδομάδα Α", "Εβδομάδα Β"].index(g["freq"]))
        
        if st.button("💾 Αποθήκευση Αλλαγής"):
            g["name"] = new_name
            g["day"] = new_day
            g["freq"] = new_freq
            del st.session_state.editing_garden
            st.rerun()

    st.markdown("---")

    # 6. Προσθήκη Νέου Κήπου
    with st.expander("➕ Προσθήκη Νέου Κήπου"):
        add_name = st.text_input("Όνομα νέου κήπου:")
        add_day = st.selectbox("Ημέρα:", days)
        add_freq = st.selectbox("Συχνότητα:", ["Εβδομαδιαίος", "Εβδομάδα Α", "Εβδομάδα Β"])
        if st.button("➕ Προσθήκη στη Λίστα"):
            if add_name:
                st.session_state.my_gardens.append({"name": add_name, "day": add_day, "freq": add_freq})
                st.success(f"Ο κήπος '{add_name}' προστέθηκε!")
                st.rerun()

elif password != "":
    st.error("❌ Λάθος κωδικός πρόσβασης!")

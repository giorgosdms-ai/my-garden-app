import streamlit as st

st.title("🌿 Πρόγραμμα Κήπων")
PASSWORD_SECRET = "1619"
password = st.text_input("Δώσε τον κωδικό πρόσβασης:", type="password")

if password == PASSWORD_SECRET:
    if "my_gardens" not in st.session_state:
        st.session_state.my_gardens = [
            {"name": "Αχιλλέας", "day": "Δευτέρα", "freq": "Εβδομαδιαίος"},
            {"name": "Ιωαννιδης", "day": "Δευτέρα", "freq": "Εβδομάδα Α"},
            {"name": "Μεταμόρφωση", "day": "Τετάρτη", "freq": "Εβδομαδιαίος"},
        ]

    week = st.radio("🗓️ Επιλογή:", ["Εβδομάδα Α", "Εβδομάδα Β"], horizontal=True)
    days = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή"]

    for day in days:
        with st.expander(f"📌 {day}"):
            for idx, g in enumerate(st.session_state.my_gardens):
                if g["day"] == day and (g["freq"] == "Εβδομαδιαίος" or g["freq"] == week):
                    # Εμφάνιση ονόματος
                    st.write(f"🌿 **{g['name']}** ({g['freq']})")
                    
                    # Κουμπιά σε πιο φαρδιές στήλες για να φαίνονται σίγουρα
                    col1, col2 = st.columns(2)
                    if col1.button("🗑️ Διαγραφή", key=f"del_{day}_{idx}"):
                        st.session_state.my_gardens.pop(idx)
                        st.rerun()
                    if col2.button("✏️ Επεξεργασία", key=f"edit_{day}_{idx}"):
                        st.session_state.editing = idx
                        st.rerun()
                    st.divider()

    # Επεξεργασία (μόνο όταν πατηθεί το κουμπί)
    if "editing" in st.session_state:
        idx = st.session_state.editing
        g = st.session_state.my_gardens[idx]
        st.info(f"Επεξεργάζεσαι τον/την: {g['name']}")
        new_name = st.text_input("Όνομα:", g["name"])
        new_day = st.selectbox("Ημέρα:", days, index=days.index(g["day"]))
        new_freq = st.selectbox("Συχνότητα:", ["Εβδομαδιαίος", "Εβδομάδα Α", "Εβδομάδα Β"], index=["Εβδομαδιαίος", "Εβδομάδα Α", "Εβδομάδα Β"].index(g["freq"]))
        
        if st.button("✅ Αποθήκευση Αλλαγών"):
            st.session_state.my_gardens[idx] = {"name": new_name, "day": new_day, "freq": new_freq}
            del st.session_state.editing
            st.rerun()

    # Εργαλείο αποθήκευσης
    st.markdown("---")
    if st.button("💾 Δημιουργία κώδικα για μόνιμη αποθήκευση"):
        st.code(f"st.session_state.my_gardens = {st.session_state.my_gardens}")

elif password != "":
    st.error("❌ Λάθος κωδικός!")

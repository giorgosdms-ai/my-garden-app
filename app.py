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

    # Εμφάνιση
    for g in st.session_state.my_gardens:
        if g["freq"] == "Εβδομαδιαίος" or g["freq"] == week:
            st.markdown(f"---")
            st.write(f"🌿 **{g['name']}** - *{g['day']}* ({g['freq']})")
            
            # Κουμπιά έξω από expander
            c1, c2 = st.columns(2)
            if c1.button("🗑️ Διαγραφή", key=f"del_{g['name']}"):
                st.session_state.my_gardens.remove(g)
                st.rerun()
            if c2.button("✏️ Επεξεργασία", key=f"edit_{g['name']}"):
                st.session_state.editing = g
                st.rerun()

    # Επεξεργασία
    if "editing" in st.session_state:
        g = st.session_state.editing
        st.warning("Επεξεργασία κήπου:")
        new_name = st.text_input("Όνομα:", g["name"])
        new_day = st.selectbox("Ημέρα:", days, index=days.index(g["day"]))
        new_freq = st.selectbox("Συχνότητα:", ["Εβδομαδιαίος", "Εβδομάδα Α", "Εβδομάδα Β"], index=["Εβδομαδιαίος", "Εβδομάδα Α", "Εβδομάδα Β"].index(g["freq"]))
        
        if st.button("✅ Αποθήκευση"):
            g.update({"name": new_name, "day": new_day, "freq": new_freq})
            del st.session_state.editing
            st.rerun()

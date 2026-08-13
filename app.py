import streamlit as st

st.set_page_config(page_title="Πρόγραμμα Κήπων", page_icon="🌿")

# ΚΟΥΜΠΙ ΚΑΘΑΡΙΣΜΟΥ (Το "πυρηνικό όπλο" για να ξεκολλήσει)
if st.sidebar.button("⚠️ ΚΑΘΑΡΙΣΜΟΣ ΔΕΔΟΜΕΝΩΝ (Reset)"):
    st.session_state.clear()
    st.rerun()

st.title("🌿 Πρόγραμμα Κήπων")

PASSWORD_SECRET = "1619"
password = st.text_input("🔑 Δώσε τον κωδικό:", type="password")

if password == PASSWORD_SECRET:
    # Αρχική λίστα
    if "my_gardens" not in st.session_state:
        st.session_state.my_gardens = [
            {"name": "Αχιλλέας", "day": "Δευτέρα", "freq": "Εβδομαδιαίος"},
            {"name": "Ξανθος", "day": "Δευτέρα", "freq": "Εβδομαδιαίος"},
            {"name": "Ιωαννιδης", "day": "Δευτέρα", "freq": "Εβδομάδα Α"},
        ]

    week = st.radio("🗓️ Εβδομάδα:", ["Εβδομάδα Α", "Εβδομάδα Β"], horizontal=True)
    
    # Εμφάνιση
    for idx, g in enumerate(st.session_state.my_gardens):
        if g["freq"] == "Εβδομαδιαίος" or g["freq"] == week:
            # Εδώ βάζουμε τα κουμπιά δίπλα στο όνομα
            st.write(f"🌿 **{g['name']}**")
            c1, c2 = st.columns(2)
            if c1.button("✏️ Αλλαγή", key=f"edit_{idx}"):
                st.session_state.editing = idx
                st.rerun()
            if c2.button("🗑️ Διαγραφή", key=f"del_{idx}"):
                st.session_state.my_gardens.pop(idx)
                st.rerun()
            st.divider()

    # Επεξεργασία
    if "editing" in st.session_state:
        idx = st.session_state.editing
        g = st.session_state.my_gardens[idx]
        st.info(f"Επεξεργασία: {g['name']}")
        new_name = st.text_input("Όνομα:", g["name"])
        if st.button("✅ Αποθήκευση"):
            st.session_state.my_gardens[idx]["name"] = new_name
            del st.session_state.editing
            st.rerun()

import streamlit as st

st.set_page_config(page_title="Πρόγραμμα Κήπων", page_icon="🌿")

if st.sidebar.button("⚠️ Καθαρισμός δεδομένων (Reset)"):
    st.session_state.clear()
    st.rerun()

st.title("🌿 Πρόγραμμα Κήπων")

PASSWORD_SECRET = "1619"
password = st.text_input("🔑 Δώσε τον κωδικό πρόσβασης:", type="password")

if password == PASSWORD_SECRET:
    if "my_gardens" not in st.session_state:
        st.session_state.my_gardens = [
            {"name": "Αχιλλέας", "day": "Δευτέρα", "freq": "Εβδομαδιαίος"},
            {"name": "Ξανθος", "day": "Δευτέρα", "freq": "Εβδομαδιαίος"},
            {"name": "Ιωαννιδης", "day": "Δευτέρα", "freq": "Εβδομάδα Α"},
        ]

    # Επιλογή συχνότητας για φιλτράρισμα
    freq_options = ["Εβδομαδιαίος", "Εβδομάδα Α", "Εβδομάδα Β", "Μία φορά τον μήνα"]
    week = st.radio("🗓️ Επίλεξε Εβδομάδα:", ["Εβδομάδα Α", "Εβδομάδα Β"], horizontal=True)
    days = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή"]

    for day in days:
        matching_gardens = [
            (idx, g) for idx, g in enumerate(st.session_state.my_gardens)
            if g["day"] == day and (g["freq"] == "Εβδομαδιαίος" or g["freq"] == week or g["freq"] == "Μία φορά τον μήνα")
        ]
        
        with st.expander(f"📌 {day} ({len(matching_gardens)} κήποι)"):
            for idx, g in matching_gardens:
                st.write(f"🌿 **{g['name']}** (*{g['freq']}*)")
                col1, col2 = st.columns(2)
                if col1.button("✏️ Αλλαγή", key=f"edit_{day}_{idx}"):
                    st.session_state.editing = idx
                    st.rerun()
                if col2.button("🗑️ Διαγραφή", key=f"del_{day}_{idx}"):
                    st.session_state.my_gardens.pop(idx)
                    st.rerun()
                st.divider()

    # Επεξεργασία
    if "editing" in st.session_state:
        idx = st.session_state.editing
        g = st.session_state.my_gardens[idx]
        st.info(f"✏️ Επεξεργασία: **{g['name']}**")
        new_name = st.text_input("Όνομα:", value=g["name"])
        new_day = st.selectbox("Ημέρα:", days, index=days.index(g["day"]))
        new_freq = st.selectbox("Συχνότητα:", freq_options, index=freq_options.index(g["freq"]))
        
        if st.button("✅ Αποθήκευση"):
            st.session_state.my_gardens[idx] = {"name": new_name, "day": new_day, "freq": new_freq}
            del st.session_state.editing
            st.rerun()

    # Προσθήκη
    st.markdown("---")
    with st.expander("➕ Προσθήκη Νέου Κήπου"):
        add_name = st.text_input("Όνομα κήπου:")
        add_day = st.selectbox("Ημέρα:", days, key="add_day")
        add_freq = st.selectbox("Συχνότητα:", freq_options, key="add_freq")
        if st.button("➕ Προσθήκη"):
            if add_name.strip():
                st.session_state.my_gardens.append({"name": add_name, "day": add_day, "freq": add_freq})
                st.rerun()

import streamlit as st

st.set_page_config(page_title="Πρόγραμμα Κήπων", page_icon="🌿", layout="centered")

st.title("🌿 Πρόγραμμα Κήπων")

# Κωδικός πρόσβασης
PASSWORD_SECRET = "1619"
password = st.text_input("🔑 Δώσε τον κωδικό πρόσβασης:", type="password")

if password == PASSWORD_SECRET:
    # Αρχική λίστα κήπων (αν δεν υπάρχει ήδη στη μνήμη)
    if "my_gardens" not in st.session_state:
        st.session_state.my_gardens = [
            {"name": "Αχιλλέας", "day": "Δευτέρα", "freq": "Εβδομαδιαίος"},
            {"name": "Ξανθος", "day": "Δευτέρα", "freq": "Εβδομάδα Α"},
            {"name": "Ιωαννιδης", "day": "Δευτέρα", "freq": "Εβδομάδα Α"},
            {"name": "Αιγίνης", "day": "Δευτέρα", "freq": "Εβδομάδα Α"},
            {"name": "Τεγεας", "day": "Δευτέρα", "freq": "Εβδομάδα Α"},
            {"name": "Μεταμόρφωση", "day": "Τετάρτη", "freq": "Εβδομαδιαίος"},
        ]

    st.markdown("---")
    
    # Επιλογή Εβδομάδας
    week = st.radio("🗓️ Επίλεξε Εβδομάδα:", ["Εβδομάδα Α", "Εβδομάδα Β"], horizontal=True)
    st.header(f"📋 Πρόγραμμα: {week}")

    days = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή"]

    # Εμφάνιση προγράμματος ανά ημέρα
    for day in days:
        # Φιλτράρισμα κήπων για την ημέρα και την εβδομάδα
        day_gardens = [
            g for g in st.session_state.my_gardens 
            if g["day"] == day and (g["freq"] == "Εβδομαδιαίος" or g["freq"] == week)
        ]
        
        with st.expander(f"📌 {day} ({len(day_gardens)} κήποι)"):
            if not day_gardens:
                st.write("*Δεν υπάρχουν προγραμματισμένοι κήποι.*")
            for g in day_gardens:
                col_name, col_edit, col_del = st.columns([0.5, 0.25, 0.25])
                col_name.write(f"🌿 **{g['name']}** ({g['freq']})")
                
                # Κουμπί Επεξεργασίας
                if col_edit.button("✏️ Αλλαγή", key=f"edit_{g['name']}_{day}"):
                    st.session_state.editing_garden = g
                    st.rerun()
                
                # Κουμπί Διαγραφής
                if col_del.button("🗑️ Διαγραφή", key=f"del_{g['name']}_{day}"):
                    st.session_state.my_gardens.remove(g)
                    st.rerun()

    # Φόρμα Επεξεργασίας Κήπου
    if "editing_garden" in st.session_state:
        g = st.session_state.editing_garden
        st.info(f"✏️ Επεξεργασία κήπου: **{g['name']}**")
        
        new_name = st.text_input("Όνομα Κήπου:", value=g["name"])
        new_day = st.selectbox("Ημέρα:", days, index=days.index(g["day"]))
        new_freq = st.selectbox("Συχνότητα:", ["Εβδομαδιαίος", "Εβδομάδα Α", "Εβδομάδα Β"], index=["Εβδομαδιαίος", "Εβδομάδα Α", "Εβδομάδα Β"].index(g["freq"]))
        
        col_save, col_cancel = st.columns(2)
        if col_save.button("✅ Αποθήκευση"):
            g["name"] = new_name
            g["day"] = new_day
            g["freq"] = new_freq
            del st.session_state.editing_garden
            st.success("Οι αλλαγές αποθηκεύτηκαν!")
            st.rerun()
            
        if col_cancel.button("❌ Ακύρωση"):
            del st.session_state.editing_garden
            st.rerun()

    st.markdown("---")

    # Προσθήκη Νέου Κήπου
    with st.expander("➕ Προσθήκη Νέου Κήπου"):
        add_name = st.text_input("Όνομα νέου κήπου:")
        add_day = st.selectbox("Ημέρα νέου κήπου:", days, key="add_day")
        add_freq = st.selectbox("Συχνότητα νέου κήπου:", ["Εβδομαδιαίος", "Εβδομάδα Α", "Εβδομάδα Β"], key="add_freq")
        
        if st.button("➕ Προσθήκη στη Λίστα"):
            if add_name.strip() != "":
                st.session_state.my_gardens.append({"name": add_name, "day": add_day, "freq": add_freq})
                st.success(f"Ο κήπος '{add_name}' προστέθηκε!")
                st.rerun()
            else:
                st.warning("Παρακαλώ γράψε ένα όνομα.")

    # Εργαλείο Μόνιμης Αποθήκευσης στον Κώδικα
    st.markdown("---")
    if st.button("💾 Δημιουργία κώδικα για μόνιμη αποθήκευση στο GitHub"):
        st.code(f"st.session_state.my_gardens = {st.session_state.my_gardens}")
        st.info("Αν θέλεις οι αλλαγές να μείνουν για πάντα, αντιγράψτε τον παραπάνω κώδικα και βάλτε τον στο GitHub!")

elif password != "":
    st.error("❌ Λάθος κωδικός πρόσβασης!")

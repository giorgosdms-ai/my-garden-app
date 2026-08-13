import streamlit as st

# 1. Τίτλος Εφαρμογής
st.title("🌿 Πρόγραμμα Κήπων")

# 2. Ασφάλεια - Κωδικός
password = st.text_input("Δώσε τον κωδικό πρόσβασης:", type="password")

if password == "1619":
    st.success("✅ Πρόσβαση εγκρίθηκε!")
    
    # Αρχικοποίηση προγράμματος στη μνήμη
    if "schedule" not in st.session_state:
        st.session_state.schedule = {
            "Δευτέρα": ["Αχιλλέας", "Ξανθος", "ιωαννιδης", "Αιγίνης", "Τεγεας",],
            "Τρίτη": ["Βουλα", "Γλυφαδα", "Αγιος Δημήτριος 1", "Αγιος Δημήτριος 2"],
            "Τετάρτη": ["Σταθης", "Ανθουσων", "Μενιδι", "Μακης", "Αλέξανδρος",],
            "Πέμπτη": ["Μετόχιο", "Μαρουσι", "Μικράς Ασιας 1", "Μικρας Ασιας 2" "καβαλας"],
            "Παρασκευή": ["Τάκης", "Γεωργία", "Μάριος"]
        }

    # 3. Φόρμα Προσθήκης Έκτακτου Κήπου
    st.subheader("➕ Προσθήκη Έκτακτου Κήπου")
    selected_day = st.selectbox("Επίλεξε Ημέρα:", list(st.session_state.schedule.keys()))
    new_garden = st.text_input("Όνομα Πελάτη / Κήπου:")
    
    if st.button("Προσθήκη στο Πρόγραμμα"):
        if new_garden:
            st.session_state.schedule[selected_day].append(new_garden)
            st.toast(f"Προστέθηκε ο κήπος '{new_garden}' για την {selected_day}!")

    st.divider()

    # 4. Εμφάνιση Εβδομαδιαίου Προγράμματος
    st.subheader("📅 Εβδομαδιαίο Πρόγραμμα")
    for day, gardens in st.session_state.schedule.items():
        with st.expander(f"📌 {day} ({len(gardens)} κήποι)"):
            for garden in gardens:
                st.write(f"• {garden}")

elif password != "":
    st.error("❌ Λάθος κωδικός!")

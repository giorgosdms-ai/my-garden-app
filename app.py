import streamlit as st

# 1. Τίτλος Εφαρμογής
st.title("🌿 Πρόγραμμα Κήπων")

# 2. Ασφάλεια - Κωδικός Πρόσβασης
PASSWORD_SECRET = "1619"  # Ο κωδικός σου

password = st.text_input("Δώσε τον κωδικό πρόσβασης:", type="password")

if password == PASSWORD_SECRET:
    st.success("✅ Πρόσβαση εγκρίθηκε!")
    st.markdown("---")

    # 3. Επιλογή Εβδομάδας (Α ή Β)
    week = st.radio("🗓️ **Επίλεξε Εβδομάδα:**", ["Εβδομάδα Α", "Εβδομάδα Β"], horizontal=True)

    # 4. Αρχικοποίηση Προγράμματος με τους δικούς σου κήπους
    if "schedule_A" not in st.session_state:
        st.session_state.schedule_A = {
            "Δευτέρα": ["Αχιλλέας", "Ξανθος", "Ιωαννιδης", "Αιγίνης", "Τεγεας"],
            "Τρίτη": ["Βουλα", "Γλυφαδα", "Αγιος Δημήτριος 1", "Αγιος Δημήτριος 2", "βερα λω φαληρο"],
            "Τετάρτη": ["Σταθης", "Ανθουσων", "Μενιδι", "Μακης", "Αλέξανδρος"],
            "Πέμπτη": ["Μετόχιο", "Μαρουσι", "Μικράς Ασιας 1", "Μικρας Ασιας 2", "καβαλας", "Ροζελα", "βερα λω ψυχικό", "Αλικη"],
            "Παρασκευή": ["Τάκης", "Γεωργία", "Μάριος"]
        }

    if "schedule_B" not in st.session_state:
        st.session_state.schedule_B = {
            "Δευτέρα": ["Αχιλλέας", "Ξανθος", "Ιωαννιδης", "Αιγίνης", "Τεγεας"],
            "Τρίτη": ["Βουλα", "Γλυφαδα", "Αγιος Δημήτριος 1", "Αγιος Δημήτριος 2", "βερα λω φαληρο"],
            "Τετάρτη": ["Σταθης", "Ανθουσων", "Μενιδι", "Μακης", "Αλέξανδρος"],
            "Πέμπτη": ["Μετόχιο", "Μαρουσι", "Μικράς Ασιας 1", "Μικρας Ασιας 2", "καβαλας", "Ροζελα", "βερα λω ψυχικό", "Αλικη"],
            "Παρασκευή": ["Τάκης", "Γεωργία", "Μάριος"]
        }

    # Επιλογή τρέχοντος προγράμματος
    current_schedule = st.session_state.schedule_A if week == "Εβδομάδα Α" else st.session_state.schedule_B

    st.subheader(f"📋 Πρόγραμμα: {week}")

    # 5. Εμφάνιση Προγράμματος ανά Ημέρα με Checkboxes
    for day, jobs in current_schedule.items():
        with st.expander(f"📌 {day} ({len(jobs)} κήποι)"):
            for job in jobs:
                st.checkbox(f"🌿 {job}", key=f"{week}_{day}_{job}")

    st.markdown("---")

    # 6. Προσθήκη Νέου Κήπου
    st.subheader("➕ Προσθήκη Νέου Κήπου")
    
    col1, col2 = st.columns(2)
    with col1:
        target_week = st.selectbox("Σε ποια εβδομάδα μπαίνει;", ["Εβδομάδα Α", "Εβδομάδα Β", "Και στις δύο"])
        target_day = st.selectbox("Ποια ημέρα;", ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή"])
    
    with col2:
        garden_name = st.text_input("Όνομα / Διεύθυνση Κήπου:")
        freq = st.selectbox("Συχνότητα:", ["Εβδομαδιαίος", "15θήμερος", "Μηνιαίος"])
        add_btn = st.button("➕ Προσθήκη στο Πρόγραμμα")

    if add_btn and garden_name:
        full_name = f"{garden_name} ({freq})" if freq != "Εβδομαδιαίος" else garden_name
        if target_week in ["Εβδομάδα Α", "Και στις δύο"]:
            st.session_state.schedule_A[target_day].append(full_name)
        if target_week in ["Εβδομάδα Β", "Και στις δύο"]:
            st.session_state.schedule_B[target_day].append(full_name)
        
        st.success(f"Ο κήπος '{full_name}' προστέθηκε επιτυχώς!")
        st.rerun()

elif password != "":
    st.error("❌ Λάθος κωδικός πρόσβασης!")


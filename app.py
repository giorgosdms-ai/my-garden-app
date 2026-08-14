import calendar
from datetime import date, datetime, timedelta
import json
import os
import streamlit as st
import base64
from google.oauth2.service_account import Credentials
import gspread

# -------------------------------------------------------------
# 1. Σύνδεση με Google Sheets (Authentication)
# -------------------------------------------------------------
# -------------------------------------------------------------
@st.cache_resource
def get_sheet():
    # Παίρνουμε αντίγραφο του dictionary από τα secrets
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    # Διόρθωση και καθαρισμός του private key
    private_key = creds_dict["private_key"]
    # Αντικαθιστούμε τα literal "\n" με πραγματικές αλλαγές γραμμής και αφαιρούμε κενά
    private_key = private_key.replace("\\n", "\n").strip()
    
    # Βεβαιωνόμαστε ότι το κλειδί έχει τη σωστή δομή (headers)
    if not private_key.startswith("-----BEGIN PRIVATE KEY-----"):
        private_key = f"-----BEGIN PRIVATE KEY-----\n{private_key}\n-----END PRIVATE KEY-----\n"
        
    creds_dict["private_key"] = private_key

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(credentials)
    
    # Υποστήριξη είτε για SPREADSHEET_ID ως string είτε ως nested dictionary
    if isinstance(st.secrets["SPREADSHEET_ID"], dict):
        sheet_id = st.secrets["SPREADSHEET_ID"]["SPREADSHEET_ID"]
    else:
        sheet_id = st.secrets["SPREADSHEET_ID"]
        
    return client.open_by_key(sheet_id).sheet1

sheet = get_sheet()


# -------------------------------------------------------------
# 2. Ρυθμίσεις Εφαρμογής & CSS
# -------------------------------------------------------------
st.set_page_config(
    page_title="Πρόγραμμα Κήπων", page_icon="🌿", layout="centered"
)

# Ασφαλής ανανέωση σελίδας
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

st.markdown(
    """
<style>
    .block-container { padding-top: 1rem; padding-bottom: 2rem; padding-left: 0.5rem; padding-right: 0.5rem; }
    div[data-testid="stVerticalBlock"] > div { gap: 0.3rem; }
    h3 { margin-top: 0.5rem !important; margin-bottom: 0.2rem !important; font-size: 1.1rem !important; color: #2e7d32; }
    hr { margin-top: 0.4rem !important; margin-bottom: 0.4rem !important; }
</style>
""",
    unsafe_allow_html=True,
)

PASSWORD_SECRET = "1619"

ALL_WEEKS = ["Εβδομάδα Α", "Εβδομάδα Β", "Εβδομάδα Γ", "Εβδομάδα Δ"]
WEEKS_AC = ["Εβδομάδα Α", "Εβδομάδα Γ"]
WEEKS_BD = ["Εβδομάδα Β", "Εβδομάδα Δ"]
WEEKS_A_ONLY = ["Εβδομάδα Α"]

DAYS_GREEK = [
    "Δευτέρα",
    "Τρίτη",
    "Τετάρτη",
    "Πέμπτη",
    "Παρασκευή",
    "Σάββατο",
    "Κυριακή",
]
MONTHS_SHORT = [
    "Ιαν",
    "Φεβ",
    "Μαρ",
    "Απρ",
    "Μαι",
    "Ιουν",
    "Ιουλ",
    "Αυγ",
    "Σεπ",
    "Οκτ",
    "Νοε",
    "Δεκ",
]
MONTHS_FULL = [
    "Ιανουάριος",
    "Φεβρουάριος",
    "Μάρτιος",
    "Απρίλιος",
    "Μάιος",
    "Ιούνιος",
    "Ιούλιος",
    "Αύγουστος",
    "Σεπτέμβριος",
    "Οκτώβριος",
    "Νοέμβριος",
    "Δεκέμβριος",
]

# -------------------------------------------------------------
# 3. Βοηθητικές Συναρτήσεις
# -------------------------------------------------------------
def get_orthodox_easter(year):
    a = year % 19
    b = year % 4
    c = year % 7
    d = (19 * a + 15) % 30
    e = (2 * b + 4 * c + 6 * d + 6) % 7
    f = d + e
    if f <= 9:
        day = 22 + f
        month = 3
    else:
        day = f - 9
        month = 4
    easter_julian = date(year, month, day)
    return easter_julian + timedelta(days=13)

def get_greek_holidays(year):
    easter = get_orthodox_easter(year)
    holidays = {
        f"{year}-01-01": "Πρωτοχρονιά",
        f"{year}-01-06": "Θεοφάνεια",
        f"{year}-03-25": "25η Μαρτίου",
        f"{year}-05-01": "Πρωτομαγιά",
        f"{year}-08-15": "Δεκαπενταύγουστος",
        f"{year}-10-28": "28η Οκτωβρίου",
        f"{year}-12-25": "Χριστούγεννα",
        f"{year}-12-26": "Σύναξη Θεοτόκου",
        (easter - timedelta(days=48)).strftime("%Y-%m-%d"): "Καθαρά Δευτέρα",
        (easter - timedelta(days=2)).strftime("%Y-%m-%d"): "Μεγάλη Παρασκευή",
        (easter - timedelta(days=1)).strftime("%Y-%m-%d"): "Μεγάλο Σάββατο",
        easter.strftime("%Y-%m-%d"): "Πάσχα",
        (easter + timedelta(days=1)).strftime("%Y-%m-%d"): "Δευτέρα του Πάσχα",
        (easter + timedelta(days=50)).strftime("%Y-%m-%d"): "Αγίου Πνεύματος",
    }
    return holidays

def get_week_name(day_num):
    if day_num <= 7:
        return "Εβδομάδα Α"
    elif day_num <= 14:
        return "Εβδομάδα Β"
    elif day_num <= 21:
        return "Εβδομάδα Γ"
    else:
        return "Εβδομάδα Δ"

def get_default_gardens():
    default_paid = {m: False for m in MONTHS_SHORT}
    gardens_raw = [
        ("Αχιλλέας", "Δευτέρα", ALL_WEEKS),
        ("28ης", "Δευτέρα", WEEKS_A_ONLY),
        ("Αγίας Λαύρας", "Δευτέρα", WEEKS_A_ONLY),
        ("Ξάνθος", "Δευτέρα", WEEKS_AC),
        ("Αιγίνης", "Δευτέρα", WEEKS_AC),
        ("Τεγέας", "Δευτέρα", WEEKS_BD),
        ("Ιωαννίδης", "Δευτέρα", WEEKS_BD),
        ("Πετραν", "Δευτέρα", WEEKS_BD),
        ("Άγιος Δημήτριος 1", "Τρίτη", ALL_WEEKS),
        ("Άγιος Δημήτριος 2", "Τρίτη", ALL_WEEKS),
        ("Γλυφάδα", "Τρίτη", ALL_WEEKS),
        ("Πετρούλα", "Τρίτη", WEEKS_A_ONLY),
        ("Βούλα", "Τρίτη", WEEKS_AC),
        ("Βέρα λω Φάληρο", "Τρίτη", WEEKS_BD),
        ("Στάθης", "Τετάρτη", ALL_WEEKS),
        ("Μενίδι", "Τετάρτη", ALL_WEEKS),
        ("Μεταμόρφωση", "Τετάρτη", WEEKS_A_ONLY),
        ("Δίπλα από Στάθη", "Τετάρτη", WEEKS_A_ONLY),
        ("Ανθουσών", "Τετάρτη", WEEKS_AC),
        ("Μάκης", "Τετάρτη", WEEKS_AC),
        ("Αλέξανδρος", "Τετάρτη", WEEKS_BD),
        ("Άνω Λιόσια", "Τετάρτη", WEEKS_BD),
        ("Μετόχιο", "Πέμπτη", WEEKS_AC),
        ("Μαρούσι", "Πέμπτη", WEEKS_AC),
        ("Μικράς Ασίας Αλέξανδρος", "Πέμπτη", WEEKS_AC),
        ("Μικράς Ασίας 2", "Πέμπτη", WEEKS_AC),
        ("Καβάλας", "Πέμπτη", WEEKS_BD),
        ("Ροζέλα", "Πέμπτη", WEEKS_BD),
        ("Βέρα λω Ψυχικό", "Πέμπτη", WEEKS_BD),
        ("Αλίκη", "Πέμπτη", WEEKS_BD),
        ("Μάριος", "Παρασκευή", WEEKS_AC),
    ]
    return [
        {
            "name": g[0],
            "day": g[1],
            "weeks": g[2].copy(),
            "notes": "",
            "paid_months": default_paid.copy(),
        }
        for g in gardens_raw
    ]

# -------------------------------------------------------------
# 4. Συναρτήσεις Αποθήκευσης & Φόρτωσης στο Google Sheets
# -------------------------------------------------------------
def save_data():
    data = {
        "my_gardens": st.session_state.my_gardens,
        "extra_events": st.session_state.extra_events,
        "leaves": st.session_state.leaves,
    }
    json_str = json.dumps(data, ensure_ascii=False)
    sheet.update('A1', [[json_str]])

def load_data():
    try:
        val = sheet.acell('A1').value
        if not val:
            return None, None, None
        content = json.loads(val)
        return (
            content.get("my_gardens", []),
            content.get("extra_events", []),
            content.get("leaves", []),
        )
    except Exception:
        return None, None, None

# -------------------------------------------------------------
# 5. Κυρίως Εφαρμογή (UI)
# -------------------------------------------------------------
st.title("🌿 Πρόγραμμα Κήπων")

if st.sidebar.button("🔄 Επαναφορά Αρχικών Κήπων"):
    st.session_state.my_gardens = get_default_gardens()
    st.session_state.extra_events = []
    st.session_state.leaves = []
    save_data()
    st.sidebar.success("Όλοι οι κήποι επαναφέρθηκαν!")
    safe_rerun()

password = st.text_input("🔑 Δώσε τον κωδικό πρόσβασης:", type="password")

if password == PASSWORD_SECRET:
    if (
        "my_gardens" not in st.session_state
        or "extra_events" not in st.session_state
        or "leaves" not in st.session_state
    ):
        saved_g, saved_e, saved_l = load_data()
        st.session_state.my_gardens = (
            saved_g if saved_g is not None else get_default_gardens()
        )
        st.session_state.extra_events = saved_e if saved_e is not None else []
        st.session_state.leaves = saved_l if saved_l is not None else []
        if saved_g is None:
            save_data()

    if "active_add_date" not in st.session_state:
        st.session_state.active_add_date = None

    view_mode = st.radio(
        "📌 **Επιλογή Προβολής:**",
        [
            "📅 Πλήρες Μηνιαίο Πρόγραμμα",
            "💰 Πληρωμές Μήνα",
            "🔄 Συχνότητα Εβδομάδων (Α,Β,Γ,Δ)",
            "➕ Προσθήκη Νέου Τακτικού Κήπου",
        ],
        horizontal=True,
    )

    # -------------------------------------------------------------
    # 1️⃣ ΠΡΟΒΟΛΗ ΜΗΝΙΑΙΟΥ ΠΡΟΓΡΑΜΜΑΤΟΣ
    # -------------------------------------------------------------
    if view_mode == "📅 Πλήρες Μηνιαίο Πρόγραμμα":

        col_m, col_y = st.columns(2)
        selected_month_num = col_m.selectbox(
            "Μήνας:",
            range(1, 13),
            index=datetime.now().month - 1,
            format_func=lambda x: MONTHS_FULL[x - 1],
        )
        selected_year = col_y.number_input(
            "Έτος:", value=datetime.now().year, step=1
        )

        holidays_dict = get_greek_holidays(selected_year)

        # 🏖️ ΔΙΑΧΕΙΡΙΣΗ ΑΔΕΙΩΝ & ΡΕΠΟ
        with st.expander("🏖️ **Διαχείριση Αδειών & Ρεπό**", expanded=False):
            tab_add_l, tab_list_l = st.tabs(
                ["➕ Προσθήκη Άδειας/Ρεπό", "📋 Ενεργές Άδειες"]
            )

            with tab_add_l:
                leave_type = st.radio(
                    "Τύπος:",
                    ["👤 Άδεια Προσωπικού", "🔴 Ρεπό / Αργία"],
                    horizontal=True,
                )

                person_name = ""
                if leave_type == "👤 Άδεια Προσωπικού":
                    person_name = st.text_input(
                        "Όνομα (π.χ. Γιάννης):", key="leave_person_input"
                    )

                col_d1, col_d2 = st.columns(2)
                start_d = col_d1.date_input(
                    "Από ημερομηνία:", date.today(), key="leave_start"
                )
                end_d = col_d2.date_input(
                    "Έως ημερομηνία:", date.today(), key="leave_end"
                )

                leave_note = st.text_input("Σημείωση (προαιρετικά):", key="leave_note")

                if st.button("✅ Αποθήκευση Άδειας / Ρεπό"):
                    if leave_type == "👤 Άδεια Προσωπικού" and not person_name.strip():
                        st.warning("Συμπλήρωσε το όνομα του ατόμου!")
                    elif start_d > end_d:
                        st.error(
                            "Η ημερομηνία 'Από' δεν μπορεί να είναι μετά την ημερομηνία 'Έως'!"
                        )
                    else:
                        new_leave = {
                            "type": (
                                "Άδεια" if leave_type == "👤 Άδεια Προσωπικού" else "Ρεπό"
                            ),
                            "person": (
                                person_name.strip()
                                if leave_type == "👤 Άδεια Προσωπικού"
                                else "Όλοι"
                            ),
                            "start_date": start_d.strftime("%Y-%m-%d"),
                            "end_date": end_d.strftime("%Y-%m-%d"),
                            "notes": leave_note.strip(),
                        }
                        st.session_state.leaves.append(new_leave)
                        save_data()
                        st.success("Καταχωρήθηκε επιτυχώς!")
                        safe_rerun()

            with tab_list_l:
                if not st.session_state.leaves:
                    st.caption("Δεν υπάρχουν καταχωρημένες άδειες ή ρεπό.")
                else:
                    for idx, l in enumerate(st.session_state.leaves):
                        c1, c2 = st.columns([0.82, 0.18])
                        range_str = (
                            f"{l['start_date']} έως {l['end_date']}"
                            if l["start_date"] != l["end_date"]
                            else l["start_date"]
                        )
                        title_str = (
                            f"🏖️ **{l['person']}** ({l['type']})"
                            if l["type"] == "Άδεια"
                            else "🔴 **ΡΕΠΟ**"
                        )
                        c1.write(
                            f"{title_str} | 📅 {range_str}"
                            + (f" _({l['notes']})_" if l["notes"] else "")
                        )
                        if c2.button("🗑️", key=f"del_leave_{idx}"):
                            st.session_state.leaves.pop(idx)
                            save_data()
                            safe_rerun()

        search_query = st.text_input(
            "🔍 Αναζήτηση Κήπου:", placeholder="Γράψε όνομα..."
        )

        if search_query.strip():
            st.subheader(f"🔎 Αποτελέσματα για: '{search_query}'")
            for idx, g in enumerate(st.session_state.my_gardens):
                if search_query.lower() in g["name"].lower():
                    weeks_str = (
                        ", ".join([w.replace("Εβδομάδα ", "") for w in g.get("weeks", [])])
                        if g.get("weeks")
                        else "Καμία"
                    )
                    st.write(
                        f"📌 **{g['name']}** | {g['day']} | **Εβδομάδες:** {weeks_str}"
                    )
                    st.caption(f"📝 Σημειώσεις: {g.get('notes', 'Καμία')}")
                    st.divider()
        else:
            num_days = calendar.monthrange(selected_year, selected_month_num)[1]

            for day_num in range(1, num_days + 1):
                day_dt = datetime(selected_year, selected_month_num, day_num)
                date_str = day_dt.strftime("%Y-%m-%d")
                greek_day_name = DAYS_GREEK[day_dt.weekday()]

                if greek_day_name == "Κυριακή":
                    continue

                week_code = get_week_name(day_num)
                month_name = MONTHS_FULL[selected_month_num - 1]

                matching_gardens = [
                    (idx, g)
                    for idx, g in enumerate(st.session_state.my_gardens)
                    if g["day"] == greek_day_name and week_code in g.get("weeks", [])
                ]

                matching_extras = [
                    (ex_idx, ev)
                    for ex_idx, ev in enumerate(st.session_state.extra_events)
                    if ev.get("date") == date_str
                ]

                matching_leaves = [
                    l
                    for l in st.session_state.leaves
                    if l["start_date"] <= date_str <= l["end_date"]
                ]

                is_official_holiday = date_str in holidays_dict

                # 📌 ΤΙΤΛΟΣ ΗΜΕΡΑΣ + ΚΟΥΜΠΙ «➕ ΕΞΤΡΑΔΑΚΙ»
                col_head1, col_head2 = st.columns([0.70, 0.30])
                with col_head1:
                    st.markdown(
                        f"### 📌 {greek_day_name} {day_num:02d} {month_name}"
                        f" <small style='color:#555;'>({week_code})</small>",
                        unsafe_allow_html=True,
                    )
                with col_head2:
                    if st.button("➕ Εξτραδάκι", key=f"btn_add_trigger_{date_str}"):
                        if st.session_state.active_add_date == date_str:
                            st.session_state.active_add_date = None
                        else:
                            st.session_state.active_add_date = date_str
                        safe_rerun()

                # 🏛️ ΕΜΦΑΝΙΣΗ ΕΠΙΣΗΜΗΣ ΑΡΓΙΑΣ
                if is_official_holiday:
                    st.error(f"🔴 **ΕΠΙΣΗΜΗ ΑΡΓΙΑ:** {holidays_dict[date_str]}")

                # 🏖️ ΕΜΦΑΝΙΣΗ ΑΔΕΙΩΝ & ΡΕΠΟ
                for l in matching_leaves:
                    if l["type"] == "Ρεπό":
                        st.error(
                            f"🔴 **ΡΕΠΟ / ΑΡΓΙΑ**"
                            + (f" - _Σημείωση: {l['notes']}_" if l["notes"] else "")
                        )
                    else:
                        st.info(
                            f"🏖️ **Άδεια:** {l['person']}"
                            + (f" - _Σημείωση: {l['notes']}_" if l["notes"] else "")
                        )

                # ⚡ ΦΟΡΜΑ ΠΡΟΣΘΗΚΗΣ ΕΞΤΡΑΔΑΚΙΟΥ
                if st.session_state.active_add_date == date_str:
                    st.info(
                        f"⚡ **Προσθήκη Εξτραδακίου για {greek_day_name}"
                        f" {day_num:02d}/{selected_month_num:02d}:**"
                    )
                    c1, c2 = st.columns([0.65, 0.35])
                    ex_name = c1.text_input(
                        "Όνομα Πελάτη:",
                        key=f"ex_name_{date_str}",
                        placeholder="π.χ. Γιώργος",
                    )
                    ex_time = c2.text_input(
                        "⏰ Ώρα:", key=f"ex_time_{date_str}", placeholder="π.χ. 10:30"
                    )
                    ex_title = st.text_input(
                        "Περιγραφή Εργασίας:",
                        key=f"ex_title_{date_str}",
                        placeholder="π.χ. Κλάδεμα / Ράντισμα",
                    )
                    ex_note = st.text_input(
                        "Σημείωση (προαιρετικά):", key=f"ex_note_{date_str}"
                    )

                    col_btn1, col_btn2 = st.columns(2)
                    if col_btn1.button("✅ Αποθήκευση", key=f"save_ex_{date_str}"):
                        if ex_name.strip() or ex_title.strip():
                            new_extra = {
                                "name": (
                                    ex_name.strip() if ex_name.strip() else "Εξτραδάκι"
                                ),
                                "time": ex_time.strip(),
                                "date": date_str,
                                "title": (
                                    ex_title.strip()
                                    if ex_title.strip()
                                    else "Έκτακτη εργασία"
                                ),
                                "notes": ex_note.strip(),
                            }
                            st.session_state.extra_events.append(new_extra)
                            save_data()
                            st.session_state.active_add_date = None
                            safe_rerun()
                        else:
                            st.warning("Συμπλήρωσε τουλάχιστον Όνομα ή Εργασία!")

                    if col_btn2.button("❌ Ακύρωση", key=f"cancel_ex_{date_str}"):
                        st.session_state.active_add_date = None
                        safe_rerun()

                # 🚨 ΕΜΦΑΝΙΣΗ ΕΞΤΡΑΔΑΚΙΩΝ
                if matching_extras:
                    for real_ex_idx, ex in matching_extras:
                        col_ex1, col_ex2 = st.columns([0.84, 0.16])
                        with col_ex1:
                            time_str = f" ⏰ {ex['time']}" if ex.get("time") else ""
                            st.warning(
                                f"⚡ **[{ex.get('name', 'Εξτραδάκι')}]**{time_str} -"
                                f" **{ex.get('title', '')}**"
                                + (
                                    f" <br>_Σημείωση: {ex['notes']}_"
                                    if ex.get("notes")
                                    else ""
                                ),
                                icon="🚨",
                            )
                        with col_ex2:
                            if st.button("🗑️", key=f"del_ex_{date_str}_{real_ex_idx}"):
                                st.session_state.extra_events.pop(real_ex_idx)
                                save_data()
                                safe_rerun()

                # 🌿 ΕΜΦΑΝΙΣΗ ΤΑΚΤΙΚΩΝ ΚΗΠΩΝ
                if (
                    not matching_gardens
                    and not matching_extras
                    and not matching_leaves
                    and not is_official_holiday
                    and st.session_state.active_add_date != date_str
                ):
                    st.caption("_Καμία προγραμματισμένη εργασία_")
                else:
                    for idx, g in matching_gardens:
                        st.checkbox(
                            f"🌿 **{g['name']}**", key=f"chk_{date_str}_{idx}_{g['name']}"
                        )

                        # 📝 ΜΟΝΟ ΣΗΜΕΙΩΣΗ
                        with st.expander(f"📝 Σημείωση ({g['name']})", expanded=False):
                            user_note = st.text_area(
                                "Σημείωση Κήπου:",
                                value=g.get("notes", ""),
                                key=f"note_{date_str}_{idx}",
                                height=60,
                            )
                            if user_note != g.get("notes", ""):
                                st.session_state.my_gardens[idx]["notes"] = user_note
                                save_data()

                st.markdown("---")

    # -------------------------------------------------------------
    # 2️⃣ ΚΑΡΤΕΛΑ ΠΛΗΡΩΜΩΝ ΜΗΝΑ
    # -------------------------------------------------------------
    elif view_mode == "💰 Πληρωμές Μήνα":
        st.subheader("💰 Διαχείριση Πληρωμών Μήνα")

        pay_month = st.selectbox(
            "Επίλεξε Μήνα για έλεγχο πληρωμών:",
            MONTHS_SHORT,
            index=datetime.now().month - 1,
            format_func=lambda x: MONTHS_FULL[MONTHS_SHORT.index(x)],
        )

        paid_count = 0
        total_gardens = len(st.session_state.my_gardens)

        st.divider()

        for idx, g in enumerate(st.session_state.my_gardens):
            pm = g.get("paid_months", {})
            is_paid = pm.get(pay_month, False)

            if is_paid:
                paid_count += 1

            c_check, c_name, c_day = st.columns([0.15, 0.55, 0.30])

            new_val = c_check.checkbox(
                "Πληρώθηκε", value=is_paid, key=f"pay_page_{pay_month}_{idx}"
            )
            c_name.markdown(f"**{g['name']}**")
            c_day.caption(f"🗓️ {g['day']}")

            if new_val != is_paid:
                if "paid_months" not in st.session_state.my_gardens[idx]:
                    st.session_state.my_gardens[idx]["paid_months"] = {m: False for m in MONTHS_SHORT}
                st.session_state.my_gardens[idx]["paid_months"][pay_month] = new_val
                save_data()
                safe_rerun()

        st.divider()
        st.info(f"📊 **Συνολικές Πληρωμές για {MONTHS_FULL[MONTHS_SHORT.index(pay_month)]}:** {paid_count} από {total_gardens} κήπους")

    # -------------------------------------------------------------
    # 3️⃣ ΚΑΡΤΕΛΑ ΣΥΧΝΟΤΗΤΑΣ ΕΒΔΟΜΑΔΩΝ
    # -------------------------------------------------------------
    elif view_mode == "🔄 Συχνότητα Εβδομάδων (Α,Β,Γ,Δ)":
        st.subheader("🔄 Διαχείριση Συχνότητας Εβδομάδων Κήπων")
        st.caption("Επίλεξε ποιες εβδομάδες του μήνα επισκέπτεσαι τον κάθε κήπο.")

        for idx, g in enumerate(st.session_state.my_gardens):
            with st.expander(f"🌿 {g['name']} ({g['day']})", expanded=False):
                current_weeks = g.get("weeks", ALL_WEEKS.copy())
                
                selected_weeks = []
                col_w1, col_w2 = st.columns(2)
                
                with col_w1:
                    if st.checkbox("Εβδομάδα Α", value="Εβδομάδα Α" in current_weeks, key=f"week_A_{idx}"):
                        selected_weeks.append("Εβδομάδα Α")
                    if st.checkbox("Εβδομάδα Β", value="Εβδομάδα Β" in current_weeks, key=f"week_B_{idx}"):
                        selected_weeks.append("Εβδομάδα Β")
                with col_w2:
                    if st.checkbox("Εβδομάδα Γ", value="Εβδομάδα Γ" in current_weeks, key=f"week_C_{idx}"):
                        selected_weeks.append("Εβδομάδα Γ")
                    if st.checkbox("Εβδομάδα Δ", value="Εβδομάδα Δ" in current_weeks, key=f"week_D_{idx}"):
                        selected_weeks.append("Εβδομάδα Δ")

                if selected_weeks != current_weeks:
                    st.session_state.my_gardens[idx]["weeks"] = selected_weeks
                    save_data()
                    safe_rerun()

    # -------------------------------------------------------------
    # 4️⃣ ΠΡΟΣΘΗΚΗ ΝΕΟΥ ΤΑΚΤΙΚΟΥ ΚΗΠΟΥ
    # -------------------------------------------------------------
    elif view_mode == "➕ Προσθήκη Νέου Τακτικού Κήπου":
        st.subheader("➕ Προσθήκη Νέου Τακτικού Κήπου")

        new_garden_name = st.text_input("Όνομα Νέου Κήπου:")
        new_garden_day = st.selectbox("Ημέρα Επίσκεψης:", DAYS_GREEK[:6]) # Εκτός Κυριακής
        
        st.write("**Επιλογή Εβδομάδων:**")
        nc1, nc2 = st.columns(2)
        n_wA = nc1.checkbox("Εβδομάδα Α", value=True, key="new_wA")
        n_wB = nc1.checkbox("Εβδομάδα Β", value=True, key="new_wB")
        n_wC = nc2.checkbox("Εβδομάδα Γ", value=True, key="new_wC")
        n_wD = nc2.checkbox("Εβδομάδα Δ", value=True, key="new_wD")

        new_garden_notes = st.text_area("Αρχικές Σημειώσεις (προαιρετικά):")

        if st.button("💾 Αποθήκευση Νέου Κήπου"):
            if not new_garden_name.strip():
                st.warning("Παρακαλώ συμπληρώστε όνομα κήπου!")
            else:
                chosen_weeks = []
                if n_wA: chosen_weeks.append("Εβδομάδα Α")
                if n_wB: chosen_weeks.append("Εβδομάδα Β")
                if n_wC: chosen_weeks.append("Εβδομάδα Γ")
                if n_wD: chosen_weeks.append("Εβδομάδα Δ")

                default_paid = {m: False for m in MONTHS_SHORT}
                new_entry = {
                    "name": new_garden_name.strip(),
                    "day": new_garden_day,
                    "weeks": chosen_weeks,
                    "notes": new_garden_notes.strip(),
                    "paid_months": default_paid.copy(),
                }
                st.session_state.my_gardens.append(new_entry)
                save_data()
                st.success(f"Ο κήπος '{new_garden_name.strip()}' προστέθηκε επιτυχώς!")
                safe_rerun()

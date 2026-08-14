
import calendar
from datetime import datetime
import json
import os
import streamlit as st

st.set_page_config(
    page_title="Πρόγραμμα Κήπων", page_icon="🌿", layout="centered"
)

# CSS για σφιχτή & καθαρή εμφάνιση σε κινητά
st.markdown(
    """
<style>
    .block-container { padding-top: 0.8rem; padding-bottom: 1.5rem; padding-left: 0.5rem; padding-right: 0.5rem; }
    div[data-testid="stVerticalBlock"] > div { gap: 0.2rem; }
    h3 { margin-top: 0.8rem !important; margin-bottom: 0.3rem !important; font-size: 1.15rem !important; color: #2e7d32; }
    hr { margin-top: 0.4rem !important; margin-bottom: 0.4rem !important; }
    .stCheckbox { margin-bottom: 0px; }
    .streamlit-expanderHeader { font-size: 0.92rem !important; font-weight: 600; padding: 4px 8px !important; }
</style>
""",
    unsafe_allow_html=True,
)

DATA_FILE = "gardens_data.json"
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


def save_data():
  data = {
      "my_gardens": st.session_state.my_gardens,
      "extra_events": st.session_state.extra_events,
  }
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


def load_data():
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = json.load(f)
        if isinstance(content, list):
          return content, []
        return content.get("my_gardens", []), content.get("extra_events", [])
    except:
      return None, None
  return None, None


st.title("🌿 Πρόγραμμα Κήπων")

if st.sidebar.button("🔄 Επαναφορά Αρχικών Κήπων"):
  st.session_state.my_gardens = get_default_gardens()
  st.session_state.extra_events = []
  save_data()
  st.sidebar.success("Όλοι οι κήποι επαναφέρθηκαν!")
  st.rerun()

password = st.text_input("🔑 Δώσε τον κωδικό πρόσβασης:", type="password")

if password == PASSWORD_SECRET:
  if (
      "my_gardens" not in st.session_state
      or "extra_events" not in st.session_state
  ):
    saved_g, saved_e = load_data()
    st.session_state.my_gardens = (
        saved_g if saved_g is not None else get_default_gardens()
    )
    st.session_state.extra_events = saved_e if saved_e is not None else []
    save_data()

  view_mode = st.radio(
      "📌 **Επιλογή Προβολής:**",
      [
          "📅 Πλήρες Μηνιαίο Πρόγραμμα",
          "🔄 Συχνότητα Εβδομάδων (Α,Β,Γ,Δ)",
          "➕ Προσθήκη / Εξτραδάκια / Διαγραφή",
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

    search_query = st.text_input(
        "🔍 Αναζήτηση Κήπου:", placeholder="Γράψε όνομα..."
    )

    def render_month_picker(garden_idx, key_prefix):
      g = st.session_state.my_gardens[garden_idx]
      pm = g.get("paid_months", {})
      paid_list = [m for m in MONTHS_SHORT if pm.get(m, False)]
      status_text = "🟢 " + ", ".join(paid_list) if paid_list else "🔴 Καμία"

      st.caption(f"**Πληρωμένοι Μήνες:** {status_text}")

      for row in range(0, 12, 4):
        cols = st.columns(4)
        for col_idx in range(4):
          m_idx = row + col_idx
          if m_idx < 12:
            m = MONTHS_SHORT[m_idx]
            is_checked = pm.get(m, False)
            new_val = cols[col_idx].checkbox(
                m, value=is_checked, key=f"{key_prefix}_{m}_{garden_idx}"
            )
            if new_val != is_checked:
              st.session_state.my_gardens[garden_idx]["paid_months"][
                  m
              ] = new_val
              save_data()
              st.rerun()

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
          render_month_picker(idx, "search")
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
            if ev["date"] == date_str
        ]

        st.markdown(
            f"### 📌 {greek_day_name} {day_num:02d} {month_name}"
            f" <small style='color:#555;'>({week_code})</small>",
            unsafe_allow_html=True,
        )

        # ⚡ ΕΜΦΑΝΙΣΗ ΕΞΤΡΑΔΑΚΙΩΝ ΜΕ ΚΟΥΜΠΙ ΔΙΑΓΡΑΦΗΣ
        if matching_extras:
          for ex_idx, ex in matching_extras:
            col_ex1, col_ex2 = st.columns([0.82, 0.18])
            with col_ex1:
              name_part = f"**[{ex.get('name', 'Εξτραδάκι')}]** "
              time_part = f"({ex['time']}) " if ex.get("time") else ""
              st.warning(
                  f"⚡ {name_part}{time_part}**{ex['title']}**"
                  + (
                      f" <br>_Σημείωση: {ex['notes']}_"
                      if ex.get("notes")
                      else ""
                  ),
                  icon="🚨",
              )
            with col_ex2:
              if st.button("🗑️", key=f"del_ex_main_{date_str}_{ex_idx}"):
                st.session_state.extra_events.pop(ex_idx)
                save_data()
                st.rerun()

        # Τακτικοί κήποι
        if not matching_gardens and not matching_extras:
          st.caption("_Καμία προγραμματισμένη εργασία_")
        else:
          for idx, g in matching_gardens:
            st.checkbox(
                f"🌿 **{g['name']}**", key=f"chk_{date_str}_{idx}_{g['name']}"
            )

            with st.expander(
                f"📝 Σημειώσεις & Πληρωμές ({g['name']})", expanded=False
            ):
              render_month_picker(idx, f"main_{date_str}")
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
  # 2️⃣ ΚΑΡΤΕΛΑ ΡΥΘΜΙΣΗΣ ΕΒΔΟΜΑΔΩΝ (Α, Β, Γ, Δ)
  # -------------------------------------------------------------
  elif view_mode == "🔄 Συχνότητα Εβδομάδων (Α,Β,Γ,Δ)":
    st.subheader("⚙️ Ρύθμιση Εβδομάδων ανά Κήπο")

    for day in DAYS_GREEK[:6]:
      day_gardens = [
          (idx, g)
          for idx, g in enumerate(st.session_state.my_gardens)
          if g["day"] == day
      ]
      if day_gardens:
        st.markdown(f"### 🗓️ {day}")
        for idx, g in day_gardens:
          st.write(f"🌿 **{g['name']}**")
          cols = st.columns(4)
          current_weeks = g.get("weeks", [])
          new_weeks = []

          for w_idx, w_code in enumerate(ALL_WEEKS):
            is_selected = w_code in current_weeks
            label = w_code.replace("Εβδομάδα ", "Εβδ. ")
            if cols[w_idx].checkbox(
                label, value=is_selected, key=f"week_set_{idx}_{w_code}"
            ):
              new_weeks.append(w_code)

          if set(new_weeks) != set(current_weeks):
            st.session_state.my_gardens[idx]["weeks"] = new_weeks
            save_data()
            st.rerun()

        st.divider()

  # -------------------------------------------------------------
  # 3️⃣ ΠΡΟΣΘΗΚΗ / ΕΞΤΡΑΔΑΚΙΑ / ΔΙΑΓΡΑΦΗ
  # -------------------------------------------------------------
  else:
    tab1, tab2, tab3 = st.tabs([
        "⚡ Προσθήκη Έκτακτου (Εξτραδάκι)",
        "➕ Προσθήκη Νέου Κήπου",
        "🗑️ Διαγραφή Κήπου / Εξτραδακίου",
    ])

    with tab1:
      st.subheader("⚡ Προσθήκη Έκτακτης Εργασίας / Εξτραδάκι")
      ex_name = st.text_input(
          "Όνομα Πελάτη / Κήπου:", placeholder="π.χ. Γιώργος / Βίλα Παπαδόπουλου"
      )
      ex_date = st.date_input("Ημερομηνία:", datetime.now())
      ex_time = st.time_input(
          "Ώρα (προαιρετικά):", datetime.strptime("09:00", "%H:%M").time()
      )
      ex_title = st.text_input(
          "Περιγραφή Εργασίας:", placeholder="π.χ. Κλάδεμα δέντρου / Ράντισμα"
      )
      ex_note = st.text_area("Σημείωση / Λεπτομέρειες:", height=60)

      if st.button("✅ Αποθήκευση & Εισαγωγή στο Πρόγραμμα"):
        if ex_title.strip():
          new_event = {
              "name": (
                  ex_name.strip() if ex_name.strip() else "Έκτακτος Πελάτης"
              ),
              "date": ex_date.strftime("%Y-%m-%d"),
              "time": ex_time.strftime("%H:%M"),
              "title": ex_title,
              "notes": ex_note,
          }
          st.session_state.extra_events.append(new_event)
          save_data()
          st.success("Το εξτραδάκι μπήκε κατευθείαν στο πρόγραμμα!")
          st.rerun()
        else:
          st.warning("Παρακαλώ συμπλήρωσε την περιγραφή εργασίας.")

    with tab2:
      st.subheader("➕ Προσθήκη Νέου Τακτικού Κήπου")
      new_name = st.text_input("Όνομα Κήπου / Πελάτη:")
      new_day = st.selectbox("Ημέρα Εβδομάδας:", DAYS_GREEK[:6])

      st.write("Εβδομάδες που πηγαίνεις:")
      w_a = st.checkbox("Εβδομάδα Α (1η-7η)", value=True)
      w_b = st.checkbox("Εβδομάδα Β (8η-14η)", value=True)
      w_c = st.checkbox("Εβδομάδα Γ (15η-21η)", value=True)
      w_d = st.checkbox("Εβδομάδα Δ (22η-31η)", value=True)

      selected_weeks = []
      if w_a:
        selected_weeks.append("Εβδομάδα Α")
      if w_b:
        selected_weeks.append("Εβδομάδα Β")
      if w_c:
        selected_weeks.append("Εβδομάδα Γ")
      if w_d:
        selected_weeks.append("Εβδομάδα Δ")

      if st.button("✅ Προσθήκη Κήπου"):
        if new_name.strip():
          default_paid = {m: False for m in MONTHS_SHORT}
          st.session_state.my_gardens.append({
              "name": new_name,
              "day": new_day,
              "weeks": selected_weeks,
              "notes": "",
              "paid_months": default_paid,
          })
          save_data()
          st.success(f"Ο κήπος '{new_name}' προστέθηκε!")
          st.rerun()

    with tab3:
      st.subheader("🗑️ Διαγραφή Εξτραδακίων")
      if st.session_state.extra_events:
        for ex_idx, ex in enumerate(st.session_state.extra_events):
          col_del1, col_del2 = st.columns([0.8, 0.2])
          col_del1.write(
              f"⚡ **[{ex.get('name', 'Εξτραδάκι')}]** {ex['date']} -"
              f" {ex['title']}"
          )
          if col_del2.button("🗑️ Διαγραφή", key=f"tab_del_ex_{ex_idx}"):
            st.session_state.extra_events.pop(ex_idx)
            save_data()
            st.success("Το εξτραδάκι διαγράφηκε!")
            st.rerun()
      else:
        st.info("Δεν υπάρχουν καταχωρημένα εξτραδάκια.")

      st.divider()

      st.subheader("🗑️ Διαγραφή Τακτικού Κήπου")
      garden_names = [g["name"] for g in st.session_state.my_gardens]
      if garden_names:
        to_delete = st.selectbox("Επίλεξε κήπο για διαγραφή:", garden_names)
        if st.button("🗑️ Διαγραφή Κήπου"):
          st.session_state.my_gardens = [
              g for g in st.session_state.my_gardens if g["name"] != to_delete
          ]
          save_data()
          st.success(f"Ο κήπος '{to_delete}' διαγράφηκε!")
          st.rerun()

elif password != "":
  st.error("❌ Λάθος κωδικός πρόσβασης!")

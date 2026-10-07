"""MediBot - hospital virtual assistant (Python + Streamlit).

Run:  streamlit run app.py
"""
import csv
import hashlib
import io
import datetime as dt

import pandas as pd
import streamlit as st

import engine
import geo
import storage as db
import voice
from i18n import LANGS, TTS_CODES, VOICE_CODES, t

st.set_page_config(page_title="MediBot", page_icon="🏥", layout="wide")
db.init()

# ---------------------------------------------------------------- session ---
st.session_state.setdefault("lang", "en")
st.session_state.setdefault("chat", [])
st.session_state.setdefault("alert", None)
st.session_state.setdefault("notified", set())
st.session_state.setdefault("tip_offset", 0)

# ---------------------------------------------------------------- sidebar ---
with st.sidebar:
    st.selectbox(t("lang_label", "en"), list(LANGS), format_func=LANGS.get, key="lang")
lang = st.session_state.lang


def T(key):
    return t(key, lang)


if lang == "ur":  # right-to-left layout for Urdu
    st.markdown("<style>.stApp{direction:rtl;text-align:right;}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.subheader(T("emg_numbers"))
    for label, number in engine.EMERGENCY_NUMBERS.items():
        st.markdown(f"**{label}:** `{number}`")
    st.caption(T("emg_note"))

# --------------------------------------------------- disclaimer (must accept) ---
st.title(T("title"))
st.caption(T("subtitle"))

if not st.session_state.get("agreed"):
    st.warning(f"**{T('disclaimer_title')}**\n\n{T('disclaimer_body')}")
    if st.button(T("agree_btn"), type="primary"):
        st.session_state.agreed = True
        st.rerun()
    st.stop()

with st.expander(T("disclaimer_title")):
    st.markdown(T("disclaimer_body"))

# ---------------------------------------------------------- patient profile ---
with st.sidebar:
    st.divider()
    st.subheader(T("profile_header"))
    st.text_input(T("p_name"), key="p_name")
    st.number_input(T("p_age"), 0, 120, 0, key="p_age")
    st.selectbox(T("p_gender"), ["", T("g_male"), T("g_female"), T("g_other"), T("g_na")], key="p_gender")
    st.text_input(T("p_allergies"), key="p_allergies")
    st.text_area(T("p_conditions"), key="p_conditions", height=70)
    st.caption(T("profile_note"))
    st.divider()
    st.checkbox(T("voice_reply"), key="speak")
    st.caption(T("ai_on") if engine.ai_available() else T("ai_off"))


def profile():
    return {
        "name": st.session_state.get("p_name", ""),
        "age": st.session_state.get("p_age", 0) or "",
        "gender": st.session_state.get("p_gender", ""),
        "allergies": st.session_state.get("p_allergies", ""),
        "conditions": st.session_state.get("p_conditions", ""),
    }


# ------------------------------------------------------------ chat handling ---
def handle(text):
    text = text.strip()
    if not text:
        return
    st.session_state.chat.append(("user", text))
    db.log_message("user", text, lang)
    kind = engine.detect_emergency(text)
    if kind:
        reply = T("emergency_msg" if kind == "medical" else "crisis_msg")
        st.session_state.alert = kind
    else:
        with st.spinner("…"):
            reply = engine.ai_reply(st.session_state.chat, lang, profile())
    st.session_state.chat.append(("assistant", reply))
    db.log_message("assistant", reply, lang)
    st.session_state.speak_text = reply


def show_alert():
    kind = st.session_state.get("alert")
    if not kind:
        return
    numbers = " • ".join(f"**{k}: {v}**" for k, v in engine.EMERGENCY_NUMBERS.items())
    st.error(f"### {T('emergency_title')}\n\n{numbers}")
    if st.button(T("dismiss"), key="dismiss_alert"):
        st.session_state.alert = None
        st.rerun()


# ------------------------------------------------------- reminder watcher ---
@st.fragment(run_every=30)
def reminder_watcher():
    """Re-checks every 30 s while the app is open."""
    for r in db.due_reminders():
        key = (r["id"], dt.date.today().isoformat())
        if key not in st.session_state.notified:
            st.session_state.notified.add(key)
            st.toast(f"💊 {r['medicine']} — {r['dose'] or ''}", icon="⏰")
        c1, c2 = st.columns([4, 1])
        c1.warning(f"⏰ **{T('rm_due')}:** {r['medicine']} {r['dose'] or ''} ({r['time']})")
        if c2.button(T("rm_taken"), key=f"taken_{r['id']}"):
            db.mark_taken(r["id"], dt.date.today().isoformat())
            st.rerun()


reminder_watcher()
show_alert()

tabs = st.tabs([T("tab_chat"), T("tab_symptom"), T("tab_doctors"),
                T("tab_reminders"), T("tab_tips"), T("tab_appts"), T("tab_history")])

# ================================================================ 1. CHAT ===
with tabs[0]:
    audio = st.audio_input(T("voice_label"))
    st.caption(T("voice_hint"))
    if audio is not None:
        data = audio.getvalue()
        h = hashlib.md5(data).hexdigest()
        if h != st.session_state.get("last_audio"):
            st.session_state.last_audio = h
            text, err = voice.transcribe(data, VOICE_CODES[lang])
            if text:
                handle(text)
            elif err == "unclear":
                st.warning(T("voice_fail"))
            else:
                st.warning(T("voice_net") + str(err))

    typed = st.chat_input(T("chat_placeholder"))
    if typed:
        handle(typed)

    if st.button(T("clear_chat")):
        st.session_state.chat = []
        st.session_state.alert = None
        st.rerun()

    with st.chat_message("assistant"):
        st.markdown(T("chat_welcome"))
    for role, msg in st.session_state.chat:
        with st.chat_message(role):
            st.markdown(msg)

    spoken = st.session_state.pop("speak_text", None)
    if spoken and st.session_state.get("speak"):
        mp3 = voice.speak(spoken, TTS_CODES[lang])
        if mp3:
            st.audio(mp3, format="audio/mp3", autoplay=True)

# ====================================================== 2. SYMPTOM CHECKER ===
with tabs[1]:
    st.markdown(T("sc_intro"))
    chosen = st.multiselect(T("sc_select"), list(engine.SYMPTOMS),
                            format_func=lambda k: engine.symptom_label(k, lang))
    c1, c2 = st.columns(2)
    severity = c1.slider(T("sc_severity"), 1, 10, 4)
    days = c2.number_input(T("sc_days"), 0, 60, 1)
    if st.button(T("sc_run"), type="primary"):
        if not chosen:
            st.warning(T("sc_pick_one"))
        else:
            age = int(st.session_state.get("p_age") or 0)
            res = engine.assess(chosen, severity, days, age)
            i = 1 if lang == "ur" else 0
            level = res["level"]
            box = {"emergency": st.error, "urgent": st.warning,
                   "soon": st.info, "home": st.success}[level]
            box(f"**{T('sc_urgency')}:** {engine.URGENCY[level][i]}")
            if level == "emergency":
                st.error(" • ".join(f"**{k}: {v}**" for k, v in engine.EMERGENCY_NUMBERS.items()))
            st.subheader(T("sc_possible"))
            if not res["ranked"]:
                st.write("—")
            for key, score in res["ranked"]:
                c = engine.CONDITIONS[key]
                st.markdown(f"**{c['name'][i]}** — {int(score * 100)}% {T('sc_match')}")
                st.progress(score)
                st.write(c["advice"][i])
                st.caption(f"{T('sc_specialty')}: {c['spec']}")
            st.caption(T("sc_note"))

# ========================================================= 3. FIND DOCTOR ===
with tabs[2]:
    st.markdown(T("dr_intro"))
    mode = st.radio(T("dr_mode"), ["sample", "live"], horizontal=True,
                    format_func=lambda m: T("dr_mode_sample") if m == "sample" else T("dr_mode_live"))
    c1, c2, c3 = st.columns(3)
    area = c1.text_input(T("dr_area"), "Karachi, Pakistan")
    radius = c2.slider(T("dr_radius"), 1, 30, 10)
    spec = c3.selectbox(T("dr_specialty"), [T("dr_all")] + geo.SPECIALTIES)
    if st.button(T("dr_search"), type="primary"):
        st.session_state.pop("doc_results", None)
        try:
            try:
                center = geo.geocode(area)
            except Exception:
                center = geo.DEFAULT_CENTER if mode == "sample" else None
                if mode == "live":
                    raise
            if center is None:
                st.warning(T("dr_geo_fail"))
            else:
                if mode == "live":
                    results = geo.live_search(center[0], center[1], radius)
                else:
                    results = geo.sample_search(center[0], center[1], radius,
                                                None if spec == T("dr_all") else spec)
                st.session_state.doc_results = (mode, results)
        except Exception as e:
            st.error(T("dr_net_err") + str(e))

    if "doc_results" in st.session_state:
        used_mode, results = st.session_state.doc_results
        if not results:
            st.info(T("dr_none"))
        else:
            st.map(pd.DataFrame(results)[["lat", "lon"]])
            for r in results:
                a, b = st.columns([4, 1])
                a.markdown(f"**{r['name']}** {('· ' + r['area']) if r['area'] else ''}  \n"
                           f"{r['km']} {T('dr_distance')}")
                b.link_button(T("dr_directions"),
                              f"https://www.google.com/maps/search/?api=1&query={r['lat']},{r['lon']}")
        if used_mode == "sample":
            st.caption(T("dr_sample_note"))

# ========================================================== 4. REMINDERS ===
with tabs[3]:
    st.subheader(T("rm_add"))
    with st.form("rm_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        med = c1.text_input(T("rm_medicine"))
        dose = c2.text_input(T("rm_dose"))
        when = c3.time_input(T("rm_time"), dt.time(9, 0))
        if st.form_submit_button(T("rm_save")) and med.strip():
            db.add_reminder(med.strip(), dose.strip(), when.strftime("%H:%M"))
            st.rerun()
    rows = db.reminders()
    if not rows:
        st.info(T("rm_empty"))
    today = dt.date.today().isoformat()
    for r in rows:
        c1, c2, c3 = st.columns([4, 1, 1])
        done = f" ✅ {T('rm_taken_today')}" if r["last_taken"] == today else ""
        c1.markdown(f"**{r['time']}** — {r['medicine']} {r['dose'] or ''}{done}")
        on = c2.checkbox(T("rm_active"), bool(r["active"]), key=f"act_{r['id']}")
        if on != bool(r["active"]):
            db.set_reminder_active(r["id"], on)
        if c3.button(T("rm_delete"), key=f"del_{r['id']}"):
            db.delete_reminder(r["id"])
            st.rerun()
    st.caption(T("rm_note"))

# =========================================================== 5. HEALTH TIPS ===
with tabs[4]:
    i = 1 if lang == "ur" else 0
    cat, en_tip, ur_tip = engine.tip_of_the_day(st.session_state.tip_offset)
    st.subheader(T("tp_today"))
    st.success(f"🌿 **{engine.TIP_CATEGORIES[cat][i]}** — {(ur_tip if i else en_tip)}")
    if st.button(T("tp_new")):
        st.session_state.tip_offset += 1
        st.rerun()
    st.divider()
    st.subheader(T("tp_all"))
    pick = st.selectbox(T("tp_cat"), [""] + list(engine.TIP_CATEGORIES),
                        format_func=lambda k: T("dr_all") if k == "" else engine.TIP_CATEGORIES[k][i])
    for c, e, u in engine.TIPS:
        if pick in ("", c):
            st.markdown(f"- **{engine.TIP_CATEGORIES[c][i]}:** {u if i else e}")

# ========================================================= 6. APPOINTMENTS ===
with tabs[5]:
    st.subheader(T("ap_new"))
    with st.form("ap_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        patient = c1.text_input(T("ap_patient"), st.session_state.get("p_name", ""))
        phone = c2.text_input(T("ap_phone"))
        facility = c1.selectbox(T("ap_facility"), [f["name"] for f in geo.FACILITIES])
        aspec = c2.selectbox(T("ap_specialty"), geo.SPECIALTIES)
        adate = c1.date_input(T("ap_date"), dt.date.today() + dt.timedelta(days=1))
        atime = c2.time_input(T("ap_time"), dt.time(10, 0))
        reason = st.text_area(T("ap_reason"), height=80)
        if st.form_submit_button(T("ap_submit")):
            if patient.strip() and phone.strip():
                db.add_appointment(patient.strip(), phone.strip(), facility, aspec,
                                   adate.isoformat(), atime.strftime("%H:%M"), reason.strip())
                st.success(T("ap_saved"))
            else:
                st.warning(T("ap_note"))
    st.subheader(T("ap_list"))
    for a in db.appointments():
        c1, c2 = st.columns([5, 1])
        c1.markdown(f"**{a['date']} {a['time']}** — {a['patient']} · {a['facility']} · {a['specialty']}  \n"
                    f"{T('ap_status')}: `{a['status']}` {('— ' + a['reason']) if a['reason'] else ''}")
        if a["status"] != "cancelled" and c2.button(T("ap_cancel"), key=f"cx_{a['id']}"):
            db.cancel_appointment(a["id"])
            st.rerun()

# ============================================================== 7. HISTORY ===
with tabs[6]:
    st.subheader(T("hs_title"))
    st.caption(T("hs_privacy"))
    msgs = db.messages()
    if not msgs:
        st.info(T("hs_empty"))
    else:
        st.dataframe(pd.DataFrame(msgs), use_container_width=True, hide_index=True)
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=["ts", "role", "lang", "content"])
        w.writeheader()
        w.writerows(msgs)
        st.download_button(T("hs_download"), buf.getvalue().encode("utf-8-sig"),
                           "medibot_history.csv", "text/csv")
        if st.button(T("hs_clear")):
            db.clear_messages()
            st.rerun()

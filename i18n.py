"""UI text for every supported language.

To add a language: add it to LANGS, VOICE_CODES, then add a new dict to TEXT
with the same keys (missing keys fall back to English automatically).
"""

LANGS = {"en": "English", "ur": "اردو (Urdu)"}

# Language codes used by speech recognition (Google) and text-to-speech (gTTS)
VOICE_CODES = {"en": "en-US", "ur": "ur-PK"}
TTS_CODES = {"en": "en", "ur": "ur"}

TEXT = {
    "en": {
        "title": "🏥 MediBot – Hospital Virtual Assistant",
        "subtitle": "Symptom checker • Emergency alerts • Nearby doctors • Reminders • Health tips • Voice input",
        "lang_label": "Language / زبان",
        "disclaimer_title": "⚠️ Medical Disclaimer",
        "disclaimer_body": (
            "MediBot gives **general health information only**. It is **not a doctor**, does not "
            "diagnose, and cannot replace professional medical advice, diagnosis or treatment. "
            "Never ignore or delay seeking medical help because of something you read here. "
            "**In an emergency, call an ambulance or go to the nearest emergency room immediately.**"
        ),
        "agree_btn": "I understand and agree",
        "profile_header": "👤 Patient details (optional)",
        "p_name": "Name",
        "p_age": "Age (years)",
        "p_gender": "Gender",
        "p_allergies": "Known allergies",
        "p_conditions": "Existing conditions / medicines",
        "g_male": "Male",
        "g_female": "Female",
        "g_other": "Other",
        "g_na": "Prefer not to say",
        "profile_note": "Details stay in this browser session only and help personalise answers.",
        "emg_numbers": "🚑 Emergency numbers",
        "emg_note": "Please verify these numbers for your city.",
        "tab_chat": "💬 Chat",
        "tab_symptom": "🩺 Symptom checker",
        "tab_doctors": "📍 Find doctor",
        "tab_reminders": "💊 Reminders",
        "tab_tips": "🌿 Health tips",
        "tab_appts": "📅 Appointments",
        "tab_history": "🗂️ History",
        "chat_welcome": (
            "Hello! I'm MediBot. Tell me your symptoms or ask a health question — type it or use the "
            "microphone. I give general information only and will flag anything that looks urgent."
        ),
        "chat_placeholder": "Type your health question…",
        "voice_label": "🎤 Voice input — record, then stop",
        "voice_hint": "Speak your question; it will be transcribed and sent automatically.",
        "voice_fail": "Could not understand the audio. Please try again.",
        "voice_net": "Voice recognition needs an internet connection or the speech package is missing: ",
        "voice_reply": "🔊 Read replies aloud",
        "clear_chat": "Clear chat",
        "ai_on": "AI mode: ON (Claude)",
        "ai_off": "AI mode: OFF – using built-in symptom engine. Set ANTHROPIC_API_KEY to enable full AI.",
        "emergency_title": "🚨 POSSIBLE EMERGENCY",
        "emergency_msg": (
            "🚨 **What you describe may be a medical emergency.**\n\n"
            "**Call an ambulance now or go to the nearest emergency room.** Do not drive yourself. "
            "Stay with someone if you can.\n\nEmergency numbers are shown in the sidebar and above."
        ),
        "crisis_msg": (
            "💙 I'm really sorry you're going through this. You are not alone, and help is available.\n\n"
            "**Please contact a mental-health helpline or emergency services right now, or go to the nearest "
            "hospital.** If you can, tell a trusted family member or friend and stay with them.\n\n"
            "If you are in immediate danger, call your local emergency number."
        ),
        "dismiss": "Dismiss alert",
        "sc_intro": "Pick everything you are experiencing. This gives a *general* idea only — it is not a diagnosis.",
        "sc_select": "Your symptoms",
        "sc_severity": "How severe is it? (1 = mild, 10 = worst)",
        "sc_days": "For how many days? (0 = just started)",
        "sc_run": "Check symptoms",
        "sc_pick_one": "Please select at least one symptom.",
        "sc_result": "Result",
        "sc_urgency": "Urgency",
        "sc_possible": "Possible causes (ranked by symptom match)",
        "sc_match": "symptom match",
        "sc_specialty": "Suggested specialist",
        "sc_note": "These are possibilities, not a diagnosis. A doctor can examine you and run tests.",
        "dr_intro": "Find hospitals, clinics and doctors near you.",
        "dr_mode": "Search source",
        "dr_mode_sample": "Built-in hospital list (works offline)",
        "dr_mode_live": "Live search (OpenStreetMap, needs internet)",
        "dr_area": "Your area / city",
        "dr_radius": "Search radius (km)",
        "dr_specialty": "Specialty",
        "dr_all": "Any",
        "dr_search": "Search",
        "dr_none": "Nothing found. Try a bigger radius or a different area.",
        "dr_distance": "km away",
        "dr_directions": "Open in Maps",
        "dr_net_err": "Could not reach the map service: ",
        "dr_sample_note": "Sample data with approximate coordinates — always call ahead and verify. Edit geo.py to add your hospital's real doctors.",
        "dr_geo_fail": "Could not find that area. Try another name.",
        "rm_add": "Add a medicine reminder",
        "rm_medicine": "Medicine name",
        "rm_dose": "Dose / notes",
        "rm_time": "Time",
        "rm_save": "Save reminder",
        "rm_empty": "No reminders yet.",
        "rm_due": "Due now",
        "rm_taken": "Mark taken",
        "rm_delete": "Delete",
        "rm_active": "Active",
        "rm_note": "Reminders alert you while this app is open in your browser. Follow your doctor's prescription.",
        "rm_taken_today": "taken today",
        "tp_today": "Tip of the day",
        "tp_new": "Another tip",
        "tp_all": "All tips",
        "tp_cat": "Category",
        "ap_new": "Request an appointment",
        "ap_patient": "Patient name",
        "ap_phone": "Phone number",
        "ap_facility": "Hospital / clinic",
        "ap_specialty": "Specialty",
        "ap_date": "Preferred date",
        "ap_time": "Preferred time",
        "ap_reason": "Reason for visit",
        "ap_submit": "Send request",
        "ap_saved": "Request saved. The hospital desk will confirm by phone.",
        "ap_list": "Your requests",
        "ap_cancel": "Cancel",
        "ap_status": "Status",
        "ap_note": "Name and phone are required.",
        "hs_title": "Saved conversation log",
        "hs_download": "Download CSV",
        "hs_clear": "Delete all saved history",
        "hs_empty": "No saved messages.",
        "hs_privacy": "Chats are logged on this computer (medibot.db). On shared hospital kiosks, clear history after use.",
    },
    "ur": {
        "title": "🏥 میڈی بوٹ – ہسپتال کا ورچوئل اسسٹنٹ",
        "subtitle": "علامات چیک • ایمرجنسی الرٹ • قریبی ڈاکٹر • دوا کی یاد دہانی • صحت کے مشورے • آواز سے سوال",
        "lang_label": "Language / زبان",
        "disclaimer_title": "⚠️ طبی انتباہ",
        "disclaimer_body": (
            "میڈی بوٹ صرف **عمومی صحت کی معلومات** دیتا ہے۔ یہ **ڈاکٹر نہیں ہے**، تشخیص نہیں کرتا اور "
            "ڈاکٹر کے مشورے، تشخیص یا علاج کا متبادل نہیں ہو سکتا۔ یہاں پڑھی کسی بات کی وجہ سے علاج میں "
            "تاخیر نہ کریں۔ **ایمرجنسی میں فوراً ایمبولینس بلائیں یا قریبی ایمرجنسی روم جائیں۔**"
        ),
        "agree_btn": "میں سمجھتا/سمجھتی ہوں اور متفق ہوں",
        "profile_header": "👤 مریض کی تفصیلات (اختیاری)",
        "p_name": "نام",
        "p_age": "عمر (سال)",
        "p_gender": "جنس",
        "p_allergies": "معلوم الرجی",
        "p_conditions": "موجودہ بیماریاں / ادویات",
        "g_male": "مرد",
        "g_female": "عورت",
        "g_other": "دیگر",
        "g_na": "بتانا نہیں چاہتا/چاہتی",
        "profile_note": "تفصیلات صرف اسی براؤزر سیشن میں رہتی ہیں اور جوابات بہتر بنانے میں مدد دیتی ہیں۔",
        "emg_numbers": "🚑 ایمرجنسی نمبرز",
        "emg_note": "براہ کرم اپنے شہر کے لیے ان نمبروں کی تصدیق کریں۔",
        "tab_chat": "💬 چیٹ",
        "tab_symptom": "🩺 علامات چیک",
        "tab_doctors": "📍 ڈاکٹر تلاش کریں",
        "tab_reminders": "💊 یاد دہانی",
        "tab_tips": "🌿 صحت کے مشورے",
        "tab_appts": "📅 اپائنٹمنٹ",
        "tab_history": "🗂️ ہسٹری",
        "chat_welcome": (
            "السلام علیکم! میں میڈی بوٹ ہوں۔ اپنی علامات بتائیں یا صحت سے متعلق سوال پوچھیں — لکھ کر یا "
            "مائیکروفون سے۔ میں صرف عمومی معلومات دیتا ہوں اور کوئی خطرناک بات ہو تو فوراً خبردار کروں گا۔"
        ),
        "chat_placeholder": "اپنا صحت کا سوال لکھیں…",
        "voice_label": "🎤 آواز سے سوال — ریکارڈ کریں، پھر روکیں",
        "voice_hint": "اپنا سوال بولیں؛ وہ خود بخود لکھ کر بھیج دیا جائے گا۔",
        "voice_fail": "آواز سمجھ نہیں آئی۔ دوبارہ کوشش کریں۔",
        "voice_net": "آواز کی شناخت کے لیے انٹرنیٹ چاہیے یا اسپیچ پیکیج انسٹال نہیں: ",
        "voice_reply": "🔊 جوابات بول کر سنائیں",
        "clear_chat": "چیٹ صاف کریں",
        "ai_on": "AI موڈ: آن (Claude)",
        "ai_off": "AI موڈ: بند – بلٹ اِن سمپٹم انجن استعمال ہو رہا ہے۔ مکمل AI کے لیے ANTHROPIC_API_KEY سیٹ کریں۔",
        "emergency_title": "🚨 ممکنہ ایمرجنسی",
        "emergency_msg": (
            "🚨 **آپ جو بتا رہے ہیں وہ طبی ایمرجنسی ہو سکتی ہے۔**\n\n"
            "**ابھی ایمبولینس بلائیں یا قریبی ایمرجنسی روم جائیں۔** خود گاڑی نہ چلائیں۔ "
            "ممکن ہو تو کسی کو ساتھ رکھیں۔\n\nایمرجنسی نمبرز سائیڈ بار اور اوپر دکھائے گئے ہیں۔"
        ),
        "crisis_msg": (
            "💙 مجھے افسوس ہے کہ آپ اس مشکل سے گزر رہے ہیں۔ آپ اکیلے نہیں ہیں، مدد دستیاب ہے۔\n\n"
            "**براہ کرم ابھی کسی ذہنی صحت ہیلپ لائن یا ایمرجنسی سروس سے رابطہ کریں، یا قریبی ہسپتال جائیں۔** "
            "ممکن ہو تو کسی قابلِ اعتماد گھر والے یا دوست کو بتائیں اور ان کے ساتھ رہیں۔\n\n"
            "اگر فوری خطرہ ہو تو اپنے علاقے کا ایمرجنسی نمبر ملائیں۔"
        ),
        "dismiss": "الرٹ بند کریں",
        "sc_intro": "جو علامات آپ کو ہیں وہ سب منتخب کریں۔ یہ صرف *عمومی* اندازہ ہے — تشخیص نہیں۔",
        "sc_select": "آپ کی علامات",
        "sc_severity": "شدت کتنی ہے؟ (1 = ہلکی، 10 = بہت زیادہ)",
        "sc_days": "کتنے دن سے؟ (0 = ابھی شروع ہوئی)",
        "sc_run": "علامات چیک کریں",
        "sc_pick_one": "براہ کرم کم از کم ایک علامت منتخب کریں۔",
        "sc_result": "نتیجہ",
        "sc_urgency": "فوریت",
        "sc_possible": "ممکنہ وجوہات (علامات کے مطابق ترتیب)",
        "sc_match": "علامات کی مطابقت",
        "sc_specialty": "تجویز کردہ ماہر",
        "sc_note": "یہ صرف امکانات ہیں، تشخیص نہیں۔ ڈاکٹر معائنہ اور ٹیسٹ کر سکتا ہے۔",
        "dr_intro": "اپنے قریب ہسپتال، کلینک اور ڈاکٹر تلاش کریں۔",
        "dr_mode": "تلاش کا ذریعہ",
        "dr_mode_sample": "بلٹ اِن ہسپتال لسٹ (آف لائن چلتی ہے)",
        "dr_mode_live": "لائیو تلاش (OpenStreetMap، انٹرنیٹ چاہیے)",
        "dr_area": "آپ کا علاقہ / شہر",
        "dr_radius": "تلاش کا دائرہ (کلومیٹر)",
        "dr_specialty": "شعبہ",
        "dr_all": "کوئی بھی",
        "dr_search": "تلاش کریں",
        "dr_none": "کچھ نہیں ملا۔ بڑا دائرہ یا دوسرا علاقہ آزمائیں۔",
        "dr_distance": "کلومیٹر دور",
        "dr_directions": "میپ میں کھولیں",
        "dr_net_err": "میپ سروس سے رابطہ نہیں ہو سکا: ",
        "dr_sample_note": "یہ نمونہ ڈیٹا ہے جس کے کوآرڈینیٹس تقریباً درست ہیں — جانے سے پہلے فون کر کے تصدیق کریں۔ اپنے ہسپتال کے اصل ڈاکٹر شامل کرنے کے لیے geo.py میں ترمیم کریں۔",
        "dr_geo_fail": "یہ علاقہ نہیں ملا۔ کوئی اور نام آزمائیں۔",
        "rm_add": "دوا کی یاد دہانی شامل کریں",
        "rm_medicine": "دوا کا نام",
        "rm_dose": "خوراک / نوٹس",
        "rm_time": "وقت",
        "rm_save": "یاد دہانی محفوظ کریں",
        "rm_empty": "ابھی کوئی یاد دہانی نہیں۔",
        "rm_due": "ابھی وقت ہو گیا",
        "rm_taken": "لے لی",
        "rm_delete": "حذف کریں",
        "rm_active": "فعال",
        "rm_note": "یاد دہانی تب بجتی ہے جب یہ ایپ براؤزر میں کھلی ہو۔ ڈاکٹر کے نسخے پر عمل کریں۔",
        "rm_taken_today": "آج لے لی",
        "tp_today": "آج کا مشورہ",
        "tp_new": "ایک اور مشورہ",
        "tp_all": "تمام مشورے",
        "tp_cat": "زمرہ",
        "ap_new": "اپائنٹمنٹ کی درخواست",
        "ap_patient": "مریض کا نام",
        "ap_phone": "فون نمبر",
        "ap_facility": "ہسپتال / کلینک",
        "ap_specialty": "شعبہ",
        "ap_date": "پسندیدہ تاریخ",
        "ap_time": "پسندیدہ وقت",
        "ap_reason": "آنے کی وجہ",
        "ap_submit": "درخواست بھیجیں",
        "ap_saved": "درخواست محفوظ ہو گئی۔ ہسپتال ڈیسک فون پر تصدیق کرے گا۔",
        "ap_list": "آپ کی درخواستیں",
        "ap_cancel": "منسوخ کریں",
        "ap_status": "حالت",
        "ap_note": "نام اور فون نمبر ضروری ہیں۔",
        "hs_title": "محفوظ شدہ گفتگو کا لاگ",
        "hs_download": "CSV ڈاؤنلوڈ کریں",
        "hs_clear": "تمام محفوظ ہسٹری حذف کریں",
        "hs_empty": "کوئی محفوظ پیغام نہیں۔",
        "hs_privacy": "چیٹس اس کمپیوٹر (medibot.db) میں لاگ ہوتی ہیں۔ مشترکہ ہسپتال کیوسک پر استعمال کے بعد ہسٹری صاف کریں۔",
    },
}


def t(key: str, lang: str = "en") -> str:
    """Translate a UI key, falling back to English, then to the key itself."""
    return TEXT.get(lang, {}).get(key) or TEXT["en"].get(key) or key

"""Medical logic: emergency detection, symptom checker, health tips, AI replies.

Everything here is plain Python and works offline except `ai_reply`'s optional
Claude call. NOTHING here is a diagnosis — always keep the disclaimer visible.
"""
import os
import re
import datetime as dt

# --------------------------------------------------------------------------
# Emergency numbers (VERIFY for your city / hospital before deployment)
# --------------------------------------------------------------------------
EMERGENCY_NUMBERS = {
    "Edhi Ambulance": "115",
    "Chhipa Ambulance": "1020",
    "Rescue": "1122",
}

# --------------------------------------------------------------------------
# Emergency keyword detection (English, Roman Urdu, Urdu script)
# Safety-first: it may over-trigger (e.g. "no chest pain") — that is deliberate.
# --------------------------------------------------------------------------
MEDICAL_EMERGENCY = [
    "chest pain", "chest tightness", "heart attack", "can't breathe", "cant breathe",
    "cannot breathe", "difficulty breathing", "not breathing", "unconscious",
    "passed out", "seizure", "convulsion", "stroke", "face drooping", "slurred speech",
    "severe bleeding", "heavy bleeding", "bleeding a lot", "vomiting blood",
    "coughing blood", "overdose", "poison", "snake bite", "choking", "anaphylaxis",
    "swollen tongue", "severe burn",
    "seene mein dard", "seene me dard", "saans nahi", "saans lene mein dikkat",
    "behosh", "dora pad", "khoon bahut", "zeher", "saanp ne kaat",
    "سینے میں درد", "سانس نہیں", "سانس لینے میں", "بے ہوش", "بیہوش", "دورہ",
    "زہر", "خون بہہ", "بہت خون", "فالج",
]
CRISIS = [
    "suicide", "kill myself", "want to die", "end my life", "hurt myself", "self harm",
    "khudkushi", "marna chahta", "marna chahti", "jaan dena",
    "خودکشی", "مرنا چاہتا", "مرنا چاہتی", "جان دینا",
]


def detect_emergency(text: str):
    """Return 'crisis', 'medical' or None."""
    low = text.lower().replace("’", "'")
    if any(k in low for k in CRISIS):
        return "crisis"
    if any(k in low for k in MEDICAL_EMERGENCY):
        return "medical"
    return None


# --------------------------------------------------------------------------
# Symptom knowledge base
# key: (English, Urdu, [keywords for free-text detection])
# --------------------------------------------------------------------------
SYMPTOMS = {
    "fever": ("Fever", "بخار", ["fever", "temperature", "bukhar", "bukhaar", "بخار"]),
    "cough": ("Cough", "کھانسی", ["cough", "khansi", "کھانسی"]),
    "sore_throat": ("Sore throat", "گلے میں درد", ["sore throat", "throat pain", "gala kharab", "gale mein dard", "گلے"]),
    "runny_nose": ("Runny / blocked nose", "ناک بہنا / بند ناک", ["runny nose", "blocked nose", "stuffy nose", "nazla", "zukam", "زکام", "نزلہ"]),
    "headache": ("Headache", "سر درد", ["headache", "head ache", "sar dard", "sir dard", "سر درد"]),
    "body_ache": ("Body aches", "جسم میں درد", ["body ache", "body pain", "badan dard", "jism mein dard", "جسم"]),
    "nausea": ("Nausea", "متلی", ["nausea", "nauseous", "matli", "متلی"]),
    "vomiting": ("Vomiting", "الٹی", ["vomit", "throwing up", "ulti", "الٹی"]),
    "diarrhea": ("Diarrhea", "دست", ["diarrhea", "diarrhoea", "loose motion", "loose stool", "dast", "دست"]),
    "abdominal_pain": ("Stomach pain", "پیٹ میں درد", ["stomach pain", "stomach ache", "abdominal", "belly pain", "pait dard", "pet dard", "پیٹ"]),
    "chest_pain": ("Chest pain / tightness", "سینے میں درد", ["chest pain", "chest tight", "seene", "سینے"]),
    "short_breath": ("Shortness of breath", "سانس پھولنا", ["short of breath", "shortness of breath", "breathless", "saans phoolna", "سانس"]),
    "dizziness": ("Dizziness", "چکر آنا", ["dizzy", "dizziness", "chakkar", "چکر"]),
    "fatigue": ("Tiredness / weakness", "تھکاوٹ / کمزوری", ["tired", "fatigue", "weakness", "weak", "kamzori", "thakan", "کمزوری", "تھکاوٹ"]),
    "rash": ("Skin rash", "جلد پر دانے", ["rash", "skin spots", "daane", "dane", "دانے"]),
    "burning_urine": ("Burning urination", "پیشاب میں جلن", ["burning urination", "burning while urinating", "peshab mein jalan", "پیشاب میں جلن"]),
    "thirst_urination": ("Excess thirst / urination", "زیادہ پیاس / پیشاب", ["excessive thirst", "very thirsty", "frequent urination", "pyaas", "پیاس"]),
    "joint_pain": ("Joint pain", "جوڑوں میں درد", ["joint pain", "joints hurt", "jodon", "جوڑ"]),
    "blurred_vision": ("Blurred vision", "دھندلا نظر آنا", ["blurred vision", "blurry vision", "dhundla", "دھندلا"]),
}

# condition: names, symptom weights, specialist, advice
CONDITIONS = {
    "cold": {
        "name": ("Common cold", "عام نزلہ زکام"),
        "w": {"runny_nose": 3, "sore_throat": 2, "cough": 2, "headache": 1, "fever": 1},
        "spec": "General Physician",
        "advice": ("Rest, drink plenty of fluids and warm drinks. Usually settles in 7–10 days.",
                   "آرام کریں، مائعات اور گرم مشروبات زیادہ لیں۔ عموماً 7 سے 10 دن میں ٹھیک ہو جاتا ہے۔"),
    },
    "flu": {
        "name": ("Influenza / viral fever", "فلو / وائرل بخار"),
        "w": {"fever": 3, "body_ache": 3, "cough": 2, "fatigue": 2, "headache": 2, "sore_throat": 1},
        "spec": "General Physician",
        "advice": ("Rest, fluids, and fever control as advised by a doctor/pharmacist. See a doctor if fever lasts over 3 days.",
                   "آرام کریں، مائعات لیں اور بخار کنٹرول ڈاکٹر/فارماسسٹ کے مشورے سے کریں۔ بخار 3 دن سے زیادہ رہے تو ڈاکٹر کو دکھائیں۔"),
    },
    "gastro": {
        "name": ("Gastroenteritis (stomach infection)", "معدے کا انفیکشن"),
        "w": {"diarrhea": 3, "vomiting": 3, "nausea": 2, "abdominal_pain": 2, "fever": 1},
        "spec": "General Physician",
        "advice": ("Take ORS in small frequent sips. See a doctor urgently if there is blood in stool, you cannot keep fluids down, or it lasts over 2 days.",
                   "او آر ایس تھوڑا تھوڑا کر کے بار بار پئیں۔ پاخانے میں خون ہو، سیال نہ ٹھہریں یا 2 دن سے زیادہ ہو تو فوراً ڈاکٹر کو دکھائیں۔"),
    },
    "migraine": {
        "name": ("Migraine / tension headache", "مائیگرین / تناؤ کا سر درد"),
        "w": {"headache": 4, "nausea": 2, "blurred_vision": 2, "dizziness": 1},
        "spec": "Neurologist",
        "advice": ("Rest in a dark quiet room and stay hydrated. A sudden 'worst headache of life' needs emergency care.",
                   "اندھیرے پرسکون کمرے میں آرام کریں اور پانی پئیں۔ اچانک زندگی کا بدترین سر درد ہو تو ایمرجنسی جائیں۔"),
    },
    "uti": {
        "name": ("Urinary tract infection", "پیشاب کی نالی کا انفیکشن"),
        "w": {"burning_urine": 4, "abdominal_pain": 2, "fever": 1, "fatigue": 1},
        "spec": "General Physician",
        "advice": ("Drink water and see a doctor for a urine test — antibiotics need a prescription.",
                   "پانی زیادہ پئیں اور پیشاب ٹیسٹ کے لیے ڈاکٹر کو دکھائیں — اینٹی بائیوٹک نسخے پر ملتی ہے۔"),
    },
    "dengue": {
        "name": ("Dengue-like illness", "ڈینگی جیسی بیماری"),
        "w": {"fever": 3, "headache": 2, "body_ache": 2, "joint_pain": 2, "rash": 2, "nausea": 1, "fatigue": 1},
        "spec": "General Physician",
        "advice": ("Common in monsoon season. Get a blood test (CBC/NS1) soon, drink fluids, and avoid aspirin/ibuprofen unless a doctor says so.",
                   "برسات میں عام ہے۔ جلد خون کا ٹیسٹ (CBC/NS1) کروائیں، مائعات لیں اور ڈاکٹر کے کہے بغیر اسپرین/آئبوپروفین نہ لیں۔"),
    },
    "typhoid": {
        "name": ("Typhoid (enteric fever)", "ٹائیفائیڈ"),
        "w": {"fever": 3, "abdominal_pain": 2, "fatigue": 2, "diarrhea": 1, "headache": 1},
        "spec": "General Physician",
        "advice": ("Prolonged fever with stomach symptoms needs a blood test and a doctor's treatment. Drink only safe water.",
                   "طویل بخار کے ساتھ پیٹ کی علامات ہوں تو خون کا ٹیسٹ اور ڈاکٹر کا علاج ضروری ہے۔ صرف صاف پانی پئیں۔"),
    },
    "diabetes": {
        "name": ("High blood sugar (diabetes warning signs)", "بلند بلڈ شوگر (ذیابیطس کی علامات)"),
        "w": {"thirst_urination": 4, "fatigue": 2, "blurred_vision": 2},
        "spec": "Endocrinologist",
        "advice": ("Get a blood sugar test (fasting / HbA1c) and see a doctor.",
                   "بلڈ شوگر ٹیسٹ (فاسٹنگ / HbA1c) کروائیں اور ڈاکٹر کو دکھائیں۔"),
    },
    "hypertension": {
        "name": ("High blood pressure", "ہائی بلڈ پریشر"),
        "w": {"headache": 2, "dizziness": 2, "blurred_vision": 2, "chest_pain": 1},
        "spec": "Cardiologist",
        "advice": ("Have your blood pressure measured. Reduce salt and see a doctor for regular monitoring.",
                   "بلڈ پریشر ناپیں۔ نمک کم کریں اور باقاعدہ نگرانی کے لیے ڈاکٹر کو دکھائیں۔"),
    },
    "asthma": {
        "name": ("Asthma / airway irritation", "دمہ / سانس کی نالیوں کی جلن"),
        "w": {"short_breath": 3, "cough": 3, "chest_pain": 1},
        "spec": "Pulmonologist",
        "advice": ("Avoid dust and smoke. If you have an inhaler, use it as prescribed. Seek care if breathing worsens.",
                   "گرد اور دھوئیں سے بچیں۔ انہیلر ہو تو نسخے کے مطابق استعمال کریں۔ سانس بگڑے تو فوراً علاج لیں۔"),
    },
    "cardiac": {
        "name": ("Possible heart-related problem", "دل سے متعلق ممکنہ مسئلہ"),
        "w": {"chest_pain": 4, "short_breath": 3, "dizziness": 2, "nausea": 1, "fatigue": 1},
        "spec": "Cardiologist",
        "advice": ("Chest pain or breathlessness can be serious. Get checked by a doctor today.",
                   "سینے کا درد یا سانس پھولنا سنگین ہو سکتا ہے۔ آج ہی ڈاکٹر سے معائنہ کروائیں۔"),
    },
}

URGENCY = {
    "emergency": ("🚨 EMERGENCY – call an ambulance / go to the ER now",
                  "🚨 ایمرجنسی – ابھی ایمبولینس بلائیں / ایمرجنسی روم جائیں"),
    "urgent": ("🟠 URGENT – see a doctor today",
               "🟠 فوری – آج ہی ڈاکٹر کو دکھائیں"),
    "soon": ("🟡 SOON – book a doctor visit in the next 1–2 days",
             "🟡 جلد – اگلے 1 سے 2 دن میں ڈاکٹر سے ملیں"),
    "home": ("🟢 LOW – home care is reasonable; watch for worsening",
             "🟢 کم – گھریلو دیکھ بھال مناسب ہے؛ حالت بگڑے تو ڈاکٹر کو دکھائیں"),
}
_ORDER = ["home", "soon", "urgent", "emergency"]


def _idx(lang):
    return 1 if lang == "ur" else 0


def symptom_label(key, lang):
    return SYMPTOMS[key][_idx(lang)]


def detect_symptoms(text):
    """Find symptom keys mentioned in free text."""
    low = text.lower()
    return [k for k, (_, _, kws) in SYMPTOMS.items() if any(w in low for w in kws)]


def assess(selected, severity=3, days=0, age=0):
    """Rank possible conditions and decide how urgent it is."""
    sel = set(selected)
    ranked = []
    for key, c in CONDITIONS.items():
        total = sum(c["w"].values())
        matched = [s for s in c["w"] if s in sel]
        got = sum(c["w"][s] for s in matched)
        # coverage of the condition x how many of YOUR symptoms it explains
        score = (got / total) * (len(matched) / len(sel)) if sel else 0
        if got and score >= 0.25:
            ranked.append((key, score))
    ranked.sort(key=lambda x: x[1], reverse=True)

    level = "home"
    if days >= 3 or severity >= 5:
        level = "soon"
    if severity >= 8 or (age and (age < 2 or age >= 65) and "fever" in sel):
        level = "urgent"
    if sel & {"chest_pain", "short_breath"}:
        level = "urgent"
    if {"chest_pain", "short_breath"} <= sel or ("chest_pain" in sel and severity >= 7):
        level = "emergency"
    return {"level": level, "ranked": ranked[:3]}


def format_assessment(res, selected, lang):
    i = _idx(lang)
    names = ", ".join(symptom_label(s, lang) for s in selected)
    lines = [f"**{URGENCY[res['level']][i]}**", ""]
    lines.append(("Symptoms noted: " if i == 0 else "نوٹ کی گئی علامات: ") + names)
    for key, score in res["ranked"]:
        c = CONDITIONS[key]
        lines.append(f"- **{c['name'][i]}** ({int(score * 100)}%) — {c['advice'][i]}")
    lines.append("")
    lines.append("Use the *Symptom checker* tab for a more detailed check, and see a doctor for a real diagnosis."
                 if i == 0 else
                 "زیادہ تفصیلی جانچ کے لیے *علامات چیک* ٹیب استعمال کریں اور اصل تشخیص کے لیے ڈاکٹر کو دکھائیں۔")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Health tips
# --------------------------------------------------------------------------
TIP_CATEGORIES = {
    "hydration": ("Hydration", "پانی"),
    "heat": ("Heat & summer", "گرمی"),
    "sleep": ("Sleep", "نیند"),
    "nutrition": ("Nutrition", "غذا"),
    "activity": ("Activity", "ورزش"),
    "hygiene": ("Hygiene", "صفائی"),
    "mental": ("Mental health", "ذہنی صحت"),
    "heart": ("Heart", "دل"),
    "mosquito": ("Dengue prevention", "ڈینگی سے بچاؤ"),
    "diabetes": ("Diabetes", "ذیابیطس"),
}

TIPS = [
    ("hydration", "Sip water through the day. Pale-yellow urine usually means you are drinking enough.",
     "دن بھر تھوڑا تھوڑا پانی پئیں۔ ہلکے زرد رنگ کا پیشاب عموماً کافی پانی کی نشانی ہے۔"),
    ("heat", "In hot weather avoid going out at midday, wear light clothes, and drink fluids — heatstroke is an emergency.",
     "گرمی میں دوپہر کو باہر جانے سے بچیں، ہلکے کپڑے پہنیں اور مائعات لیں — ہیٹ اسٹروک ایمرجنسی ہے۔"),
    ("sleep", "Adults generally need 7–9 hours of sleep. Keep a regular sleep time and avoid screens before bed.",
     "بالغوں کو عموماً 7 سے 9 گھنٹے نیند چاہیے۔ سونے کا وقت مقرر رکھیں اور سونے سے پہلے اسکرین سے بچیں۔"),
    ("nutrition", "Fill half your plate with vegetables and fruit; limit fried food, sugary drinks and extra salt.",
     "آدھی پلیٹ سبزیوں اور پھلوں سے بھریں؛ تلی ہوئی چیزیں، میٹھے مشروبات اور زیادہ نمک کم کریں۔"),
    ("activity", "Aim for about 30 minutes of brisk walking on most days. Even short walks help.",
     "زیادہ تر دن تقریباً 30 منٹ تیز چہل قدمی کریں۔ مختصر چہل قدمی بھی فائدہ دیتی ہے۔"),
    ("hygiene", "Wash hands with soap for 20 seconds before eating and after using the toilet.",
     "کھانے سے پہلے اور بیت الخلا کے بعد 20 سیکنڈ تک صابن سے ہاتھ دھوئیں۔"),
    ("mental", "Feeling low or anxious for weeks? Talk to someone you trust or a mental-health professional — it is a health issue like any other.",
     "کئی ہفتوں سے اداسی یا گھبراہٹ ہے؟ کسی قابلِ اعتماد شخص یا ماہرِ نفسیات سے بات کریں — یہ بھی دوسری بیماریوں کی طرح صحت کا مسئلہ ہے۔"),
    ("heart", "Do not ignore chest pain, especially with sweating or breathlessness. Get a regular blood pressure check after age 30.",
     "سینے کے درد کو نظر انداز نہ کریں، خاص طور پر پسینے یا سانس پھولنے کے ساتھ۔ 30 سال کے بعد بلڈ پریشر باقاعدگی سے چیک کروائیں۔"),
    ("mosquito", "Remove standing water from coolers, tyres and pots weekly, and use repellent and nets during dengue season.",
     "کولر، ٹائر اور گملوں میں کھڑا پانی ہر ہفتے نکالیں اور ڈینگی کے موسم میں ریپیلنٹ اور جالی استعمال کریں۔"),
    ("diabetes", "Family history of diabetes? Get a blood sugar test yearly and limit sugary drinks and sweets.",
     "خاندان میں ذیابیطس ہے؟ ہر سال شوگر ٹیسٹ کروائیں اور میٹھے مشروبات اور مٹھائی کم کریں۔"),
    ("nutrition", "Do not skip breakfast; include protein such as eggs, lentils or yoghurt to stay full longer.",
     "ناشتہ نہ چھوڑیں؛ انڈے، دال یا دہی جیسی پروٹین شامل کریں تاکہ دیر تک پیٹ بھرا رہے۔"),
    ("hydration", "Illness with diarrhea or vomiting? Use ORS rather than plain water alone, and take it in small sips.",
     "دست یا الٹی ہو تو صرف پانی کے بجائے او آر ایس لیں اور تھوڑا تھوڑا کر کے پئیں۔"),
]


def tip_of_the_day(offset=0):
    idx = (dt.date.today().toordinal() + offset) % len(TIPS)
    return TIPS[idx]


# --------------------------------------------------------------------------
# AI replies (Claude when ANTHROPIC_API_KEY is set, built-in engine otherwise)
# --------------------------------------------------------------------------
MODEL = os.environ.get("MEDIBOT_MODEL", "claude-sonnet-5-5")

SYSTEM_PROMPT = """You are MediBot, a virtual health assistant for a hospital.
Rules:
- Give general health information only. Never claim to diagnose. Never prescribe prescription-only medicines or give specific doses.
- Ask one or two short clarifying questions when symptoms are vague (duration, severity, age, other symptoms).
- If anything suggests a possible emergency (chest pain, trouble breathing, stroke signs, severe bleeding, unconsciousness, poisoning, suicidal thoughts) tell the person to call emergency services / go to the ER immediately.
- For self-harm or suicidal thoughts: respond with warmth, encourage contacting a helpline, emergency services or a trusted person. Never give methods.
- Consider the patient details provided (age, allergies, conditions) when relevant.
- Be warm, concise (under 180 words), and use simple language. Use short bullet points when helpful.
- Always recommend seeing a doctor for persistent, worsening, or severe symptoms.
- Reply in the same language the user selected: {lang_name}.
"""


def ai_available():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return False
    try:
        import anthropic  # noqa: F401
        return True
    except ImportError:
        return False


def _profile_text(profile):
    parts = []
    for k, label in [("name", "Name"), ("age", "Age"), ("gender", "Gender"),
                     ("allergies", "Allergies"), ("conditions", "Existing conditions/medicines")]:
        v = profile.get(k)
        if v:
            parts.append(f"{label}: {v}")
    return "; ".join(parts)


def fallback_reply(text, lang, profile):
    found = detect_symptoms(text)
    if not found:
        return ("I can help best if you tell me your symptoms (for example: fever, cough, headache, stomach pain). "
                "You can also use the **Symptom checker** tab. I give general information only — please see a doctor for a diagnosis."
                if lang == "en" else
                "اپنی علامات بتائیں تو میں بہتر مدد کر سکوں گا (مثلاً بخار، کھانسی، سر درد، پیٹ درد)۔ "
                "آپ **علامات چیک** ٹیب بھی استعمال کر سکتے ہیں۔ میں صرف عمومی معلومات دیتا ہوں — تشخیص کے لیے ڈاکٹر کو دکھائیں۔")
    try:
        age = int(profile.get("age") or 0)
    except (TypeError, ValueError):
        age = 0
    return format_assessment(assess(found, severity=3, days=0, age=age), found, lang)


def ai_reply(history, lang, profile):
    """history: list of (role, text) ending with the latest user message."""
    if not ai_available():
        return fallback_reply(history[-1][1], lang, profile)
    try:
        import anthropic
        client = anthropic.Anthropic()
        msgs = [{"role": r, "content": m} for r, m in history[-12:]]
        while msgs and msgs[0]["role"] != "user":
            msgs.pop(0)
        system = SYSTEM_PROMPT.format(lang_name="Urdu (اردو)" if lang == "ur" else "English")
        ptxt = _profile_text(profile)
        if ptxt:
            system += f"\nPatient details: {ptxt}"
        resp = client.messages.create(model=MODEL, max_tokens=600, system=system, messages=msgs)
        return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
    except Exception as e:  # network, key, quota ...
        return fallback_reply(history[-1][1], lang, profile) + f"\n\n_(AI service unavailable: {type(e).__name__})_"

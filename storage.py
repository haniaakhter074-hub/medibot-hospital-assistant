"""SQLite storage (single file: medibot.db next to this script)."""
import sqlite3
import datetime as dt
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).with_name("medibot.db")

SCHEMA = [
    """CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, role TEXT, lang TEXT, content TEXT)""",
    """CREATE TABLE IF NOT EXISTS reminders(
        id INTEGER PRIMARY KEY AUTOINCREMENT, medicine TEXT, dose TEXT,
        time TEXT, active INTEGER DEFAULT 1, last_taken TEXT)""",
    """CREATE TABLE IF NOT EXISTS appointments(
        id INTEGER PRIMARY KEY AUTOINCREMENT, created TEXT, patient TEXT, phone TEXT,
        facility TEXT, specialty TEXT, date TEXT, time TEXT, reason TEXT,
        status TEXT DEFAULT 'requested')""",
]


def _run(sql, args=(), fetch=False):
    with closing(sqlite3.connect(DB_PATH)) as con:
        con.row_factory = sqlite3.Row
        cur = con.execute(sql, args)
        rows = [dict(r) for r in cur.fetchall()] if fetch else None
        con.commit()
        return rows


def init():
    for sql in SCHEMA:
        _run(sql)


# ---- chat log -------------------------------------------------------------
def log_message(role, content, lang):
    _run("INSERT INTO messages(ts, role, lang, content) VALUES(?,?,?,?)",
         (dt.datetime.now().isoformat(timespec="seconds"), role, lang, content))


def messages():
    return _run("SELECT ts, role, lang, content FROM messages ORDER BY id", fetch=True)


def clear_messages():
    _run("DELETE FROM messages")


# ---- reminders ------------------------------------------------------------
def add_reminder(medicine, dose, hhmm):
    _run("INSERT INTO reminders(medicine, dose, time) VALUES(?,?,?)", (medicine, dose, hhmm))


def reminders():
    return _run("SELECT * FROM reminders ORDER BY time", fetch=True)


def set_reminder_active(rid, active):
    _run("UPDATE reminders SET active=? WHERE id=?", (int(active), rid))


def mark_taken(rid, day_iso):
    _run("UPDATE reminders SET last_taken=? WHERE id=?", (day_iso, rid))


def delete_reminder(rid):
    _run("DELETE FROM reminders WHERE id=?", (rid,))


def due_reminders(now=None):
    """Active reminders whose time has passed today and are not yet taken today."""
    now = now or dt.datetime.now()
    today = now.date().isoformat()
    due = []
    for r in reminders():
        if not r["active"] or r["last_taken"] == today:
            continue
        h, m = map(int, r["time"].split(":"))
        if now >= now.replace(hour=h, minute=m, second=0, microsecond=0):
            due.append(r)
    return due


# ---- appointments ---------------------------------------------------------
def add_appointment(patient, phone, facility, specialty, date, time, reason):
    _run("""INSERT INTO appointments(created, patient, phone, facility, specialty, date, time, reason)
            VALUES(?,?,?,?,?,?,?,?)""",
         (dt.datetime.now().isoformat(timespec="seconds"), patient, phone, facility,
          specialty, date, time, reason))


def appointments():
    return _run("SELECT * FROM appointments ORDER BY date, time", fetch=True)


def cancel_appointment(aid):
    _run("UPDATE appointments SET status='cancelled' WHERE id=?", (aid,))

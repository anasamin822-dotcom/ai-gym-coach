import sqlite3
import streamlit as st
from pathlib import Path
from datetime import datetime, timedelta

_DB_PATH = str(Path(__file__).parent.parent.parent / "data.db")


@st.cache_resource
def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = _get_connection()

    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                username   TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS exercises (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER NOT NULL REFERENCES users(id),
                exercise_name TEXT    NOT NULL,
                reps          INTEGER NOT NULL DEFAULT 0,
                sets          INTEGER NOT NULL DEFAULT 0,
                time          INTEGER NOT NULL DEFAULT 0,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS payments (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id      INTEGER NOT NULL REFERENCES users(id),
                phone_number TEXT,
                plan_name    TEXT NOT NULL,
                amount       REAL NOT NULL,
                utr_number   TEXT UNIQUE NOT NULL,
                status       TEXT DEFAULT 'VERIFIED',
                created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Robust schema migrations for existing SQLite databases
        existing_cols = [row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()]
        
        if "phone_number" not in existing_cols:
            try:
                conn.execute("ALTER TABLE users ADD COLUMN phone_number TEXT")
            except sqlite3.OperationalError:
                pass

        if "trial_start" not in existing_cols:
            try:
                conn.execute("ALTER TABLE users ADD COLUMN trial_start TIMESTAMP")
            except sqlite3.OperationalError:
                pass

        if "is_pro" not in existing_cols:
            try:
                conn.execute("ALTER TABLE users ADD COLUMN is_pro INTEGER DEFAULT 0")
            except sqlite3.OperationalError:
                pass

        if "pro_expiry" not in existing_cols:
            try:
                conn.execute("ALTER TABLE users ADD COLUMN pro_expiry TIMESTAMP")
            except sqlite3.OperationalError:
                pass

        if "last_payment_ref" not in existing_cols:
            try:
                conn.execute("ALTER TABLE users ADD COLUMN last_payment_ref TEXT")
            except sqlite3.OperationalError:
                pass


def get_user(username: str) -> sqlite3.Row:
    conn = _get_connection()
    return conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()


def get_user_by_phone(phone_number: str) -> sqlite3.Row:
    conn = _get_connection()
    clean_phone = "".join(filter(str.isdigit, str(phone_number)))
    return conn.execute("SELECT * FROM users WHERE phone_number = ?", (clean_phone,)).fetchone()


def create_user_with_phone(phone_number: str, username: str = None) -> sqlite3.Row:
    conn = _get_connection()
    clean_phone = "".join(filter(str.isdigit, str(phone_number)))
    if not username:
        username = f"Athlete_{clean_phone[-4:]}"

    now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with conn:
        conn.execute(
            """
            INSERT INTO users (username, phone_number, trial_start, is_pro)
            VALUES (?, ?, ?, 0)
            """,
            (username, clean_phone, now_iso)
        )
    return get_user_by_phone(clean_phone)


def get_or_create_user_by_phone(phone_number: str) -> sqlite3.Row:
    user = get_user_by_phone(phone_number)
    if user is None:
        user = create_user_with_phone(phone_number)
    return user


def calculate_subscription_status(user_id: int) -> dict:
    """
    Computes 7-Day Free Trial remaining days, Pro subscription status, and access rights.
    """
    conn = _get_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        return {
            "is_pro": False,
            "is_trial_active": False,
            "trial_days_left": 0,
            "can_access": False,
            "badge_text": "Guest",
            "badge_color": "gray"
        }

    # Check Pro status
    is_pro = bool(user["is_pro"])
    pro_expiry = user["pro_expiry"]
    now = datetime.now()

    if is_pro and pro_expiry:
        try:
            exp_date = datetime.strptime(str(pro_expiry)[:19], "%Y-%m-%d %H:%M:%S")
            if exp_date < now:
                is_pro = False
        except Exception:
            pass

    if is_pro:
        return {
            "is_pro": True,
            "is_trial_active": False,
            "trial_days_left": 0,
            "can_access": True,
            "badge_text": "👑 PRO ATHLETE",
            "badge_color": "#00F59B"
        }

    # Check 7-Day Free Trial
    trial_start_str = user["trial_start"] if "trial_start" in user.keys() and user["trial_start"] else user["created_at"]
    trial_days_left = 7
    if trial_start_str:
        try:
            start_date = datetime.strptime(str(trial_start_str)[:19], "%Y-%m-%d %H:%M:%S")
            elapsed = (now - start_date).total_seconds() / (24 * 3600)
            trial_days_left = max(0, 7 - int(elapsed))
        except Exception:
            trial_days_left = 7

    is_trial_active = trial_days_left > 0
    can_access = is_pro or is_trial_active

    if is_trial_active:
        badge_text = f"🟢 7-Day Trial: {trial_days_left} Days Left"
        badge_color = "#38BDF8"
    else:
        badge_text = "⚠️ Free Trial Expired"
        badge_color = "#EF4444"

    return {
        "is_pro": is_pro,
        "is_trial_active": is_trial_active,
        "trial_days_left": trial_days_left,
        "can_access": can_access,
        "badge_text": badge_text,
        "badge_color": badge_color
    }


def activate_pro_subscription(user_id: int, plan_name: str, days: int, amount: float, utr_number: str) -> bool:
    conn = _get_connection()
    now = datetime.now()
    expiry_date = (now + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    clean_utr = str(utr_number).strip().upper()

    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    phone = user["phone_number"] if user and "phone_number" in user.keys() else ""

    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO payments (user_id, phone_number, plan_name, amount, utr_number, status)
            VALUES (?, ?, ?, ?, ?, 'VERIFIED')
            """,
            (user_id, phone, plan_name, amount, clean_utr)
        )
        conn.execute(
            """
            UPDATE users
            SET is_pro = 1, pro_expiry = ?, last_payment_ref = ?
            WHERE id = ?
            """,
            (expiry_date, clean_utr, user_id)
        )
    return True


def get_user_payments(user_id: int):
    conn = _get_connection()
    return conn.execute("SELECT * FROM payments WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()


def add_exercise(user_id, exercise_name, reps, sets, time):
    conn = _get_connection()
    with conn:
        existing = conn.execute("""
            SELECT * FROM exercises 
            WHERE user_id = ? AND exercise_name = ? AND Date('created_at') = Date('now')
        """, (user_id, exercise_name)).fetchone()

        if existing:
            conn.execute("""
                UPDATE exercises 
                SET reps = reps + ?, sets = sets + ?, time = time + ?
                WHERE id = ?
            """, (reps, sets, time, existing['id']))
        else:
            conn.execute("""
                INSERT INTO exercises (user_id, exercise_name, sets, reps, time)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, exercise_name, sets, reps, time))


def get_users_exercises(user_id):
    conn = _get_connection()
    return conn.execute("""
        SELECT * FROM exercises 
        WHERE user_id = ?
    """, (user_id,)).fetchall()

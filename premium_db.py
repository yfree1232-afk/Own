import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("premium.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS premium_users (
    user_id INTEGER PRIMARY KEY,
    expiry_date TEXT
)
""")
conn.commit()


def add_user(user_id: int, days: int):
    expiry = datetime.now() + timedelta(days=days)
    cursor.execute(
        "REPLACE INTO premium_users (user_id, expiry_date) VALUES (?, ?)",
        (user_id, expiry.strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    return expiry


def remove_user(user_id: int):
    cursor.execute("DELETE FROM premium_users WHERE user_id = ?", (user_id,))
    conn.commit()


def is_premium(user_id: int):
    cursor.execute("SELECT expiry_date FROM premium_users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()

    if not data:
        return False

    expiry = datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S")

    if expiry < datetime.now():
        remove_user(user_id)
        return False

    return True


def get_expiry(user_id: int):
    cursor.execute("SELECT expiry_date FROM premium_users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    if data:
        return datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S")
    return None

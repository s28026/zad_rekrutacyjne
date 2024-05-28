import time
from .db import get_db


def add_message(title, content):
    db = get_db()
    db.execute("INSERT INTO messages (title, content) VALUES (?, ?)", (title, content))
    db.commit()


def get_messages():
    db = get_db()
    return db.execute("SELECT * FROM messages").fetchall()

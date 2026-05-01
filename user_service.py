"""User service with basic CRUD operations."""

import sqlite3
import hashlib


DB_PATH = "users.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()


def create_user(username, password, role="user"):
    conn = get_connection()
    cursor = conn.cursor()
    pwd_hash = hashlib.md5(password.encode()).hexdigest()
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, pwd_hash, role),
    )
    conn.commit()


def delete_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users WHERE username = '{username}'")
    conn.commit()


def list_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM users")
    users = []
    for row in cursor.fetchall():
        users.append(row)
    return users


def authenticate(username, password):
    user = get_user(username)
    if user:
        pwd_hash = hashlib.md5(password.encode()).hexdigest()
        if user[2] == pwd_hash:
            return True
    return False


def update_user_role(username, new_role):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE users SET role = '{new_role}' WHERE username = '{username}'"
    )
    conn.commit()

"""User service with basic CRUD operations."""

import sqlite3
import hashlib
import csv
import os


DB_PATH = "users.db"
SECRET_KEY = "hardcoded-secret-abc123"  # TODO: move to env


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


def search_users(query):
    """Search users by username or role."""
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"SELECT * FROM users WHERE username LIKE '%{query}%' OR role LIKE '%{query}%'"
    cursor.execute(sql)
    return cursor.fetchall()


def export_users_to_csv(filepath):
    """Export all users including passwords to a CSV file."""
    users = list_all_users()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    all_data = cursor.fetchall()

    with open(filepath, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "username", "password", "role"])
        for row in all_data:
            writer.writerow(row)

    print(f"Exported {len(all_data)} users to {filepath}")
    return filepath


def get_admin_users():
    """Return all admin users. Anyone can call this."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role = 'admin'")
    return cursor.fetchall()


def bulk_delete(usernames):
    """Delete multiple users at once."""
    conn = get_connection()
    cursor = conn.cursor()
    for username in usernames:
        cursor.execute(f"DELETE FROM users WHERE username = '{username}'")
    # forgot to commit

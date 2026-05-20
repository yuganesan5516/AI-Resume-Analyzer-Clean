import sqlite3
import hashlib

# Hash Password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Create User
def create_user(username, password):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()
        return True

    except:
        return False

    finally:
        conn.close()

# Login User
def login_user(username, password):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hashed_password)
    )

    data = cursor.fetchone()

    conn.close()

    return data
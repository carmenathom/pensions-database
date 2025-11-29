from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(username, email, password, role, name):
    existing = find_user_by_username(username)
    if existing:
        raise ValueError("Username already exists")

    conn = get_db()
    cur = conn.cursor()
    hashed = generate_password_hash(password)

    try:
        cur.execute("""
            INSERT INTO Users (username, email, password_hash, role, name)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING user_id;
        """, (username, email, hashed, role, name))

        uid = cur.fetchone()['user_id']  
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
    return uid



def find_user_by_username(username):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT user_id, username, password_hash, role 
        FROM Users 
        WHERE username = %s
    """, (username,))
    
    user = cur.fetchone() 
    cur.close()
    conn.close()
    return user



def validate_login(username, password):
    user = find_user_by_username(username)
    if user and check_password_hash(user['password_hash'], password):  
        return user
    return None
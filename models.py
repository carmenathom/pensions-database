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


def get_all_users():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, username, email, role, name, created_at
        FROM Users
        ORDER BY user_id;
    """)
    users = cur.fetchall()

    cur.close()
    conn.close()
    return users


def get_user_by_id(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, username, email, role, name
        FROM Users
        WHERE user_id = %s;
    """, (user_id,))

    user = cur.fetchone()

    cur.close()
    conn.close()
    return user

def update_user(user_id, username, email, role, name):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Users
        SET username = %s, email = %s, role = %s, name = %s
        WHERE user_id = %s;
    """, (username, email, role, name, user_id))

    conn.commit()
    cur.close()
    conn.close()

def insert_document(title, doc_type, source, added_by, filename):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Document (title, doc_type, source, added_by, processed)
        VALUES (%s, %s, %s, %s, FALSE)
        RETURNING document_id;
    """, (title, doc_type, source, added_by))

    doc_id = cur.fetchone()['document_id']
    conn.commit()

    cur.close()
    conn.close()

    return doc_id

def mark_document_processed(doc_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Document
        SET processed = TRUE
        WHERE document_id = %s;
    """, (doc_id,))

    conn.commit()
    cur.close()
    conn.close()

def get_documents_by_user(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT document_id, title, doc_type, source, processed, added_at, added_by
        FROM Document
        WHERE added_by = %s
        ORDER BY added_at DESC;
    """, (user_id,))

    docs = cur.fetchall()
    cur.close()
    conn.close()
    return docs


def get_document_by_id(doc_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT document_id, title, doc_type, source, processed, added_at, added_by
        FROM Document
        WHERE document_id = %s;
    """, (doc_id,))

    doc = cur.fetchone()
    cur.close()
    conn.close()
    return doc


def update_document(doc_id, title, doc_type, source):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Document
        SET title = %s, doc_type = %s, source = %s
        WHERE document_id = %s;
    """, (title, doc_type, source, doc_id))

    conn.commit()
    cur.close()
    conn.close()

def delete_document_db(doc_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM Document WHERE document_id = %s;", (doc_id,))

    conn.commit()
    cur.close()
    conn.close()

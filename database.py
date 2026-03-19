import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DB_URL, sslmode='require')

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    # Create Tables
    cur.execute('''CREATE TABLE IF NOT EXISTS scammers 
                   (bgmi_id TEXT PRIMARY KEY, reason TEXT, proof TEXT, added_by TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS sellers 
                   (user_id TEXT PRIMARY KEY, name TEXT, vouches INTEGER DEFAULT 0)''')
    conn.commit()
    cur.close()
    conn.close()

def search_scammer(query_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM scammers WHERE bgmi_id = %s", (query_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def add_scammer(bgmi_id, reason, proof, admin_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO scammers VALUES (%s, %s, %s, %s)", (bgmi_id, reason, proof, admin_id))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except:
        return False

import os
import pymysql
from pymysql.cursors import DictCursor
from threading import Lock
from dotenv import load_dotenv

load_dotenv() 

_lock = Lock()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "sepehran_flights")
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        charset=DB_CHARSET,
        cursorclass=DictCursor,
        autocommit=False
    )

def execute(query: str, params: tuple = (), commit: bool = False) -> int:
    with _lock:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(query, params)
            if commit:
                conn.commit()
            return cur.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()

def fetchall(query: str, params: tuple = ()):
    with _lock:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(query, params)
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

def fetchone(query: str, params: tuple = ()):
    with _lock:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(query, params)
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()

import sqlite3
from exceptions import auth_exceptions

conn = sqlite3.connect('./database.db', check_same_thread=False)

def init():
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        uid INTEGER PRIMARY KEY AUTOINCREMENT,
        id TEXT UNIQUE,
        password TEXT,
        name TEXT
    ); ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS posts(
        postid INTEGER PRIMARY KEY AUTOINCREMENT,
        ownerid INTEGER,
        ownername TEXT,
        content TEXT
    ); ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS chat_rooms(
        chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_name TEXT,
        room_type TEXT CHECK(room_type IN ('private', 'group')) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by INTEGER,
        FOREIGN KEY (created_by) REFERENCES users(uid)
    ); ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS chat_members(
        chat_id INTEGER,
        user_id INTEGER,
        PRIMARY KEY (chat_id, user_id),
        FOREIGN KEY (chat_id) REFERENCES chat_rooms(chat_id),
        FOREIGN KEY (user_id) REFERENCES users(uid)
    ); ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS chat_messages (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER,
        sender_id INTEGER,
        content TEXT NOT NULL,
        FOREIGN KEY (room_id) REFERENCES chat_rooms(chat_id),
        FOREIGN KEY (sender_id) REFERENCES users(uid)
    ); ''')
    conn.commit()

def insert_user(name, id, password):
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO users (name, id, password) VALUES (?, ?, ?);', (name, id, password))
        conn.commit()
    except:
        conn.rollback()
        raise RegisterFailed(message='Database insert failed.')

def select_user(id, password):
    # TODO: try except handle
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = ? AND password = ?;', (id, password))
    return cur.fetchone()

def list_post():
    # TODO: try except handle
    cur = conn.cursor()
    cur.execute('SELECT * FROM posts;')
    return cur.fetchall()

def insert_post(ownerid, ownername, content):
    # TODO: try except handle
    cur = conn.cursor()
    cur.execute("INSERT INTO posts (ownerid, ownername, content) VALUES (?, ?, ?);", (ownerid, ownername, content))
    conn.commit()

def post_chat(chat_id: int):
    # TODO
    return 1


init()
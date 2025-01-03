import sqlite3
from for_server.exceptions import db_exceptions

conn = sqlite3.connect('./database.db', check_same_thread=False)

def insert_user(name, id, password):
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO users (name, id, password) VALUES (?, ?, ?);', (name, id, password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        raise db_exceptions.RegisterFailed("Already exists")
    except sqlite3.Error:
        conn.rollback()
        raise db_exceptions.RegisterFailed("Database error")


def login(id, password):
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE id = ? AND password = ?;', (id, password))
        user = cur.fetchone()
        if user is None:
            raise db_exceptions.LoginFailed("ID or password is incorrect")
        return user
    except sqlite3.Error:
        raise db_exceptions.LoginFailed("Database error")


def list_post():
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM posts;')
        return cur.fetchall()
    except sqlite3.Error as e:
        raise db_exceptions.ChatBaseException(f"failed to list posts: {str(e)}")


def insert_post(ownerid, ownername, content):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO posts (ownerid, ownername, content) VALUES (?, ?, ?);",
                    (ownerid, ownername, content))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise db_exceptions.ChatBaseException(f"failed to insert post: {str(e)}")


def get_chat(chat_id: int, uid):
    try:
        cur = conn.cursor()
        # 채팅방 존재 여부 확인
        cur.execute('SELECT * FROM chat_rooms WHERE chat_id = ?;', (chat_id,))
        if cur.fetchone() is None:
            raise db_exceptions.ChatRoomNotFound()

        # 사용자가 채팅방 멤버인지 확인
        cur.execute('SELECT * FROM chat_members WHERE chat_id = ? AND user_id = ?;',
                    (chat_id, uid))
        if cur.fetchone() is None:
            raise db_exceptions.NotParticipant()

        # 채팅방 정보 가져오기
        cur.execute('''
            SELECT chat_rooms.*, users.name as creator_name 
            FROM chat_rooms 
            LEFT JOIN users ON chat_rooms.created_by = users.uid 
            WHERE chat_id = ?
        ''', (chat_id,))
        chat_info = cur.fetchone()

        # 메시지 목록 가져오기
        cur.execute('''
            SELECT chat_messages.*, users.name as sender_name 
            FROM chat_messages 
            LEFT JOIN users ON chat_messages.sender_id = users.uid 
            WHERE room_id = ? 
            ORDER BY message_id ASC
        ''', (chat_id,))
        messages = cur.fetchall()

        return {
            "chat_info": chat_info,
            "messages": messages
        }
    except (db_exceptions.ChatRoomNotFound, db_exceptions.NotParticipant):
        raise
    except sqlite3.Error as e:
        raise db_exceptions.ChatBaseException(f"failed to get chat: {str(e)}")


def post_chat(chat_id: int, sender_id: int, content: str):
    try:
        cur = conn.cursor()
        # 채팅방 존재 여부 확인
        cur.execute('SELECT * FROM chat_rooms WHERE chat_id = ?;', (chat_id,))
        if cur.fetchone() is None:
            raise db_exceptions.ChatRoomNotFound()

        # 발신자가 채팅방 멤버인지 확인
        cur.execute('SELECT * FROM chat_members WHERE chat_id = ? AND user_id = ?;',
                    (chat_id, sender_id))
        if cur.fetchone() is None:
            raise db_exceptions.NotParticipant()

        # 메시지 저장
        cur.execute('''
            INSERT INTO chat_messages (room_id, sender_id, content) 
            VALUES (?, ?, ?)
        ''', (chat_id, sender_id, content))
        conn.commit()
        return cur.lastrowid
    except (db_exceptions.ChatRoomNotFound, db_exceptions.NotParticipant):
        raise
    except sqlite3.Error as e:
        conn.rollback()
        raise db_exceptions.MessagePostFailed()

def create_chat_room(room_name: str, room_type: str, creator_id: int, members: list[int]):
    try:
        cur = conn.cursor()
        # 채팅방 생성
        cur.execute('''
            INSERT INTO chat_rooms (room_name, room_type, created_by) 
            VALUES (?, ?, ?)
        ''', (room_name, room_type, creator_id))

        chat_id = cur.lastrowid

        # 생성자 추가
        cur.execute('''
            INSERT INTO chat_members (chat_id, user_id)
            VALUES (?, ?)
        ''', (chat_id, creator_id))

        # 다른 멤버들 추가
        for member_id in members:
            if member_id != creator_id:  # 생성자가 멤버 목록에 있어도 중복 추가되지 않도록
                cur.execute('''
                    INSERT INTO chat_members (chat_id, user_id)
                    VALUES (?, ?)
                ''', (chat_id, member_id))

        cur.execute('INSERT INTO chat_members (chat_id, user_id) VALUES (?, ?);', (chat_id, 0))
        conn.commit()
        return chat_id
    except sqlite3.Error as e:
        conn.rollback()
        raise db_exceptions.ChatBaseException(f"채팅방 생성 실패: {str(e)}")

def get_user_chats(user_id: int):
    try:
        cur = conn.cursor()
        # 사용자가 참여중인 모든 채팅방 정보를 가져옴
        cur.execute('''
            SELECT 
                cr.chat_id,
                cr.room_name,
                cr.room_type,
                u.name as creator_name,
                (
                    SELECT COUNT(*)
                    FROM chat_members cm2
                    WHERE cm2.chat_id = cr.chat_id
                ) as member_count
            FROM chat_rooms cr
            JOIN chat_members cm ON cr.chat_id = cm.chat_id
            LEFT JOIN users u ON cr.created_by = u.uid
            WHERE cm.user_id = ?
            ORDER BY cr.chat_id DESC
        ''', (user_id,))

        return cur.fetchall()
    except sqlite3.Error as e:
        raise db_exceptions.ChatBaseException(f"failed to get user chats: {str(e)}")

def init():
    try:
        cur = conn.cursor()
        with open('./dao/init.sql', 'r') as sql_file:
            sql_script = sql_file.read()
        cur.executescript(sql_script)
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise db_exceptions.ChatBaseException(f"failed to initialize database: {str(e)}")

init()
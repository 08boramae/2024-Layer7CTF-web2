CREATE TABLE IF NOT EXISTS users (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    id TEXT,
    password TEXT,
    name TEXT
);

CREATE TABLE IF NOT EXISTS posts (
    postid INTEGER PRIMARY KEY,
    ownerid INTEGER,
    ownername TEXT,
    content TEXT
);

CREATE TABLE IF NOT EXISTS chat_rooms (
    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT,
    room_type TEXT CHECK(room_type IN ('private', 'group')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    FOREIGN KEY (created_by) REFERENCES users(uid)
);

CREATE TABLE IF NOT EXISTS chat_members (
    chat_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY (chat_id, user_id),
    FOREIGN KEY (chat_id) REFERENCES chat_rooms(chat_id),
    FOREIGN KEY (user_id) REFERENCES users(uid)
);

CREATE TABLE IF NOT EXISTS chat_messages (
    message_id INTEGER PRIMARY KEY,
    room_id INTEGER,
    sender_id INTEGER,
    content TEXT NOT NULL,
    FOREIGN KEY (room_id) REFERENCES chat_rooms(chat_id),
    FOREIGN KEY (sender_id) REFERENCES users(uid)
);

INSERT INTO users (uid, id, password, name) VALUES (0, 'bot', 'opqypdktv87129g51rv2aa7lxbvdc6zs', 'bot');
INSERT INTO users (id, password, name) VALUES ('admin', 'u11jq93fdbfysp5n1nytqufu8dhg68zz', 'admin');
INSERT INTO users (id, password, name) VALUES ('johndoe', 'l9okbbz2biimwvmavf535z48sjd00sp0', 'John Doe');

INSERT INTO chat_rooms (room_name, room_type, created_by) VALUES ('FLAG', 'private', 0);
INSERT INTO chat_members (chat_id, user_id) VALUES (1, 0);
INSERT INTO chat_messages (room_id, sender_id, content) VALUES (1, 0, 'Layer7{smooth_like_jelly_ya_x5emyeje0dfwbc0y7boramae0247js2sc4f60c}');
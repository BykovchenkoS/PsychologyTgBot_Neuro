import sqlite3

with sqlite3.connect('../DataBases/database.db', check_same_thread=False) as db:
    cursor = db.cursor()
    query_users = """
    CREATE TABLE IF NOT EXISTS users (
      user_id INTEGER PRIMARY KEY,
      have_friends BOOLEAN,
      user_name VARCHAR(50)
    );
    """
    query_friends = """CREATE TABLE IF NOT EXISTS users_friends (
      user_friend TEXT PRIMARY KEY,
      user_id INTEGER NOT NULL,
      FOREIGN KEY(user_id) REFERENCES users(user_id)
    );
    """
    cursor.execute(query_users)
    cursor.execute(query_friends)
    pass

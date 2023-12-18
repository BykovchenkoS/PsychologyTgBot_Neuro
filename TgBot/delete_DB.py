import DB_connection as db

db.cursor.execute('DELETE from users;')
db.cursor.execute('DELETE from users_friends;')
db.cursor.connection.commit()
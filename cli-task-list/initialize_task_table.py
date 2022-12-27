import sqlite3

conn = sqlite3.connect('tasks.db')
c = conn.cursor()
c.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, description TEXT, deadline DATE, completed BOOLEAN DEFAULT 0, group_id TEXT)")
conn.commit()
conn.close()

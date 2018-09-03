import sqlite3
conn = sqlite3.connect("testing.db")
c = conn.cursor()
c.execute('''create table user(id INTEGER primary key  autoincrement,
             name char(10))''')
rs = c.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'")
for ex in rs:
    print(ex)
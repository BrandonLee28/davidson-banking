import sqlite3
conn = sqlite3.connect('.\sql_db\Demo_table.db')
cur = conn.cursor()

# create table in database
username = "test@yaboo.com"
password = 1

#query = "Insert Into user ('email','password') Values(?,?);"
#cur.execute(query,(username,password))
#conn.commit()
#conn.commit()
#query = "UPDATE user SET money = money + ? WHERE user_id = ?"
#cur.execute(query,(100,28))
print(cur.execute("SELECT * FROM user").fetchall())

# Add the new 'money' column to the 'users' table

# Commit the changes
conn.commit()

# commit and save changes to database
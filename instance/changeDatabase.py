import sqlite3

conn = sqlite3.connect("instance\\warehouse.db")
cur = conn.cursor()


cur.execute("INSERT INTO user_model (username,password,role) VALUES (?,?,?)",("zahra","zahra123","admin"))
#cur.execute("INSERT INTO product (code,dateOfLoad,sold) VALUES (?,?,?)",("12","12","12"))

conn.commit()


#read csv file 
# import sqlite3

# conn = sqlite3.connect("emaildb.sqlite")
# cur = conn.cursor()

# cur.execute("DROP TABLE IF EXISTS Counts")
# cur.execute("CREATE TABLE Counts (email TEXT,count INTEGER)")

# fh = open("mbox.txt")
# for line in fh :
#     if not line.startswith("From: "):continue
#     pieces = line.split()
#     email = pieces[1]
#     cur.execute('SELECT count FROM Counts WHERE email=? ',(email,))
#     row = cur.fetchone()
#     if row is None:
#         cur.execute("INSERT INTO Counts (email,count) VALUES (?,1)",(email,))
#     else:
#         cur.execute("UPDATE Counts SET count=count +1 WHERE email=?",(email,))
#     conn.commit()
# cur.close()

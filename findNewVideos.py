import subprocess
import sqlite3
from sqlite3 import Error

videoDate = "2017-10-08"

try:
    connection = sqlite3.connect("C:/Users/yulia/PycharmProjects/youtubescraper/youtubeDB.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM video WHERE date=?", (videoDate,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
except Error as e:
    print(e)
finally:
    connection.close()

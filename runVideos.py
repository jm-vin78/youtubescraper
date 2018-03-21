# -*- coding: utf-8 -*-
import subprocess
import sqlite3
from sqlite3 import Error
from scrapy.crawler import CrawlerProcess
import scrapy
from youtubescraper.spiders.channelSpider import ChannelspiderSpider


try:
    connection = sqlite3.connect("C:/Users/yulia/PycharmProjects/youtubescraper/youtubeDB.db")
    cur = connection.cursor()
    cur.execute(''' DELETE FROM video  ''')
    cur.execute(''' DELETE FROM sqlite_sequence WHERE name="video" ''')  # reset ids from 1
    cur.execute(''' DELETE FROM channel  ''')
    connection.commit()
    cur.execute("SELECT name, idSubTopic FROM subtopic")
    rows = cur.fetchall()
    for row in rows:
        print(row)
        theme = row[0].replace(" ", "+")
        print(theme)
        idSubTopic = row[1]
        print(idSubTopic)
        command = 'scrapy crawl --nolog youTubeSpider -a theme=%s -a idSubTopic=%i' % (theme, idSubTopic)
        subprocess.call(command)
except Error as e:
    print(e)
finally:
    print()
    connection.close()


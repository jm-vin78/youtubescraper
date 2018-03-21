# -*- coding: utf-8 -*-
import subprocess
import sqlite3
from sqlite3 import Error
from scrapy.crawler import CrawlerProcess
import scrapy
from youtubescraper.spiders.channelSpider import ChannelspiderSpider


try:
    #connection = sqlite3.connect("C:/Users/yulia/PycharmProjects/youtubescraper/youtubeDB.db")
    #cur = connection.cursor()
    #cur.execute(''' DELETE FROM channel  ''')
    #connection.commit()
    command = 'scrapy crawl --nolog channelSpider'
    subprocess.call(command)

except Error as e:
    print(e)
finally:
    print()
    # connection.close()


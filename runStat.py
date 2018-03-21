# -*- coding: utf-8 -*-
import subprocess
import sqlite3
from sqlite3 import Error
from scrapy.crawler import CrawlerProcess
import scrapy
from youtubescraper.spiders.channelSpider import ChannelspiderSpider


try:
    commandStat = 'scrapy crawl --nolog statSpider'
    subprocess.call(commandStat)
except Error as e:
    print(e)
finally:
    print()

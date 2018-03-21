# -*- coding: utf-8 -*-
import scrapy
from string import digits
import sqlite3
from sqlite3 import Error
import re
import sys
from datetime import datetime

class StatSpider(scrapy.Spider):
    name = 'statSpider'
    base_url = ''

    def __init__(self, *args, **kwargs):
        super(StatSpider, self).__init__(*args, **kwargs)
        print("Initializing spider.")
        try:
            connection = sqlite3.connect("C:/Users/yulia/PycharmProjects/youtubescraper/youtubeDB.db")
            cur = connection.cursor()
            cur.execute("SELECT url FROM statVideo")
            results = cur.fetchall()
            for result in results:
                self.start_urls.append(self.base_url+result[0])
        except Error as e:
            print(e)
        finally:
            connection.close()
            print(self.start_urls)

    def parse(self, response):
        try:
            # url = response.xpath('//*[@id="video-title"]').extract_first()
            #
            # date = response.xpath('//*[@id="watch-uploader-info"]/strong/text()').extract_first()
            # date_only = re.search('Published on (\w+\W\d+)\W(\W\d+)', date)
            # date_only = date_only.group(1) + date_only.group(2)
            # date_edited = datetime.strptime(date_only, '%b %d %Y').date()
            # date = date_edited

            print("Parsing video. Url: %s" % response.url)
            url = response.url
            number_of_views = ''.join(c for c in response.xpath('//*[@id="watch7-views-info"]/div[1]/text()').extract_first() if c in digits)
            connection = sqlite3.connect("C:/Users/yulia/PycharmProjects/youtubescraper/youtubeDB.db")
            cur = connection.cursor()
            sql = ''' UPDATE statVideo SET 
                            numberOfViews=? 
                      WHERE url=? '''
            cur.execute(sql, (number_of_views, url))
            connection.commit()
        except:
            e = sys.exc_info()[0]
            print(e)
        finally:
            connection.close()

# -*- coding: utf-8 -*-
import scrapy
from string import digits
import sqlite3
from sqlite3 import Error
import re
import sys
from datetime import datetime

class ChannelspiderSpider(scrapy.Spider):
    name = 'channelSpider'
    base_url = 'https://www.youtube.com'

    def __init__(self, *args, **kwargs):
        super(ChannelspiderSpider, self).__init__(*args, **kwargs)
        print("Initializing spider.")
        try:
            connection = sqlite3.connect("C:/Users/yulia/PycharmProjects/youtubescraper/youtubeDB.db")
            cur = connection.cursor()
            cur.execute("SELECT url FROM channel")
            results = cur.fetchall()
            for result in results:
                self.start_urls.append(self.base_url+result[0]+"/videos")
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

            print("Parsing channel. Url: %s" % response.url)
            number_of_views_last = response.xpath('//*[@id="channels-browse-content-grid"]/li[1]/div/div[1]/div[2]/div/ul/li[1]/text()').extract_first()
            number_of_views2 = []
            number_of_views = response.xpath('//*[@id="channels-browse-content-grid"]/li/div/div[1]/div[2]/div/ul/li[1]/text()').extract()
            for elem in number_of_views:
                elem = ''.join(c for c in elem if c in digits)
                number_of_views2.append(elem)
            number_of_views2 = [0 if x == '' else int(x) for x in number_of_views2]
            mean_views = round(sum(number_of_views2)/len(number_of_views2), 2)

            m = re.search("https://www.youtube.com(.+)/videos", response.url)
            url = m.group(1)
            connection = sqlite3.connect("C:/Users/yulia/PycharmProjects/youtubescraper/youtubeDB.db")
            cur = connection.cursor()
            sql = ''' UPDATE channel SET 
                            averageViewsAllVideos=?
                      WHERE url=? '''
            cur.execute(sql, (mean_views, url))
            connection.commit()
        except:
            e = sys.exc_info()[0]
            print(e)
        finally:
            connection.close()

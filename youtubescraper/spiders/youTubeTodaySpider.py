# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from string import digits
from scrapy.linkextractors import LinkExtractor
import sqlite3
from sqlite3 import Error
import re
from datetime import datetime

class YoutubetodayspiderSpider(CrawlSpider):
    name = 'youTubeTodaySpider'
    base_url = 'https://www.youtube.com/results?sp=EgIIAg%253D%253D&search_query=' # find videos posted today

    rules = [
        Rule(LinkExtractor(allow=r"/watch\?v=.+$"), callback='parse_videos'),
        # Rule(LinkExtractor(allow=r"/channel/.*", process_value=process_value), callback='parse_channels'),
        # Rule(LinkExtractor(allow=r"/user/.+$", process_value=process_value), callback='parse_channels')
    ]

    def __init__(self, theme='', idSubTopic='', *args, **kwargs):
        super(YoutubetodayspiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = [self.base_url + theme]
        self.theme = theme
        self.idSubTopic = idSubTopic

    def parse_videos(self, response):
        print("Parsing today's video. Theme: %s" % self.theme)
        print("Subtopic id: %s" % self.idSubTopic)
        text = response.xpath('//*[@id="eow-title"]/@title').extract_first()
        channel = response.xpath('//*[@id="watch7-user-header"]/div/a/text()').extract_first()
        channel_link = response.xpath('//*[@id="watch7-user-header"]/div/a/@href').extract_first()
        number_of_views = ''.join(c for c in response.xpath('//*[@id="watch7-views-info"]/div[1]/text()').extract_first() if c in digits)

        date = response.xpath('//*[@id="watch-uploader-info"]/strong/text()').extract_first()
        date_only = re.search('Published on (\w+\W\d+)\W(\W\d+)', date)
        date_only = date_only.group(1) + date_only.group(2)
        date_edited = datetime.strptime(date_only, '%b %d %Y').date()
        date = date_edited

        description = response.xpath('//*[@id="eow-description"]/text()').extract_first()
        category = response.xpath('//*[@id="watch-description-extras"]/ul/li[1]/ul/li/a/text()').extract_first()
        url = response.url

        number_of_subscribers = response.xpath('//*[@id="watch7-subscription-container"]/span/span[2]/text()').extract_first()
        if "K" in number_of_subscribers:
            number_of_subscribers = float(number_of_subscribers.replace("K", "")) * 1000
        elif "M" in number_of_subscribers:
            number_of_subscribers = float(number_of_subscribers.replace("M", "")) * 1000000
        number_of_subscribers = int(number_of_subscribers)

        likes = response.xpath('//*[@id="watch8-sentiment-actions"]/span/span[1]/button/span/text()').extract_first()
        dislikes = response.xpath('//*[@id="watch8-sentiment-actions"]/span/span[3]/button/span/text()').extract_first()

        try:
            connection = sqlite3.connect("C:/Users/yulia/PycharmProjects/youtubescraper/youtubeDB.db")
            cur = connection.cursor()

            # cur.execute("SELECT * FROM channel WHERE url=?", (channel_link,))
            # if cur.fetchone() is None:
            #     print("No such channel.")
            #     sql = ''' INSERT INTO
            #                 channel(name, url, numberOfSubscribers)
            #                 VALUES(?,?,?) '''
            #     cur.execute(sql, (channel, channel_link, number_of_subscribers))

            sql = ''' INSERT INTO 
                todayVideo(name, url, numberOfViews, date, likes, dislikes, description, channelUrl, category, idSubTopic) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
            print((text, url, number_of_views, date, likes, dislikes, description, channel_link, category, self.idSubTopic))
            cur.execute(sql, (text, url, number_of_views, date, likes, dislikes, description, channel_link, category, self.idSubTopic))
            connection.commit()
        except Error as e:
            print(e)
        finally:
            connection.close()


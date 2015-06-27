#!/usr/bin/env python

import sys
import os
import feedparser
import time
from goose import Goose
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir_path)
print parent_dir_path
from DbScripts.mongo_db_basketball import BasketFeedMongo
from Links_Basketball import NBA
class Basketball:
    """
    This function gets the links 
    of all the news articles on the
    Rss Feed and stores them in list_of_links.
    """
    def rss_feeds(self,NBA):
        list_of_links = list()
        self.list_of_links = list_of_links
        self.d = feedparser.parse(NBA)
        self.details = self.d.entries
        for entry in self.details:
            self.list_of_links.append(entry['link'])
            
        print self.list_of_links
    
    """
    This function gets the full text from all 
    the links in the list_of_links, only after checking
    for redundancy
    """

    def full_news(self):
        goose_instance = Goose()
        for val in self.list_of_links:
            article = goose_instance.extract(val)
            full_text = article.cleaned_text.format()
            title = article.title
            _dict = {"website":"NBA", "news_id":val, "news":full_text, "title":title, "time_of_storing":time.mktime(time.localtime())}
            BasketFeedMongo.insert_news(_dict)
    
    """
    This function checks for duplicate news_ids.
    If a duplicate is found function full_news doesn't run
    """
    
    def checking(self):
        for val in self.list_of_links:
            if not BasketFeedMongo.check_basket(val):
                self.full_news()


if __name__ == '__main__':
    obj = Basketball()
    obj.rss_feeds(NBA)
    obj.checking()
    #obj.full_news()







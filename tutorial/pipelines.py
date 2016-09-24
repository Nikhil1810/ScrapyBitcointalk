# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.exceptions import DropItem
import json
import datetime
 
class TutorialPipeline(object):
    def __init__(self):
        self.addresses = {}
        self.file = open('output.json', 'wb')
        self.backupfile = open('backup-output.json', 'wb', 1)
        self.max_users = -1
        self.cur_users = 0
        

    def process_item(self, item, spider):
      
        
        if item["membername"] in self.addresses:
            
              
            for i in self.addresses.values():
                 
                 if item["address"] not in i:
                      self.addresses[item["membername"]].add(item["address"])
            
            
        else:
            
            self.addresses.setdefault(item["membername"],set())
            self.addresses[item["membername"]].add(item["address"])
            
            self.backupfile.write("%s " % json.dumps({item["membername"]:(item["address"])}))
            self.backupfile.write(" %s \n" % json.dumps(item["date"]))
            date_handler = lambda obj: (
                obj.isoformat()
                if isinstance(obj, datetime.datetime)
                or isinstance(obj, datetime.date)
                else None 
            )    
            self.backupfile.write("%s \n" % json.dumps(datetime.datetime.now(), default=date_handler))                 
            self.cur_users += 1
        if self.cur_users == self.max_users:
            raise CloseSpider('count reached')
        else:
            return item

    
    
    def close_spider(self, spider):
        def set_default(obj):
          if isinstance(obj, set):
             return list(obj)
        
          raise TypeError
        
        
        
        self.addresses.update((key,(value)) for key,value in self.addresses.items())
        self.file.write(json.dumps(self.addresses,default=set_default))
       
        self.file.close()







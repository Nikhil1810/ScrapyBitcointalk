from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.item import Item
from scrapy.linkextractors.sgml import SgmlLinkExtractor

import bc_validator as bcv
from tutorial.items import TutorialItem

class BitcointalkSpider(CrawlSpider):
    name = "bitcoin"
    allowed_domains = ["bitcointalk.org"]
    
    start_urls = ['https://bitcointalk.org/index.php?topic=1128521.1000']

    rules = (
       Rule(SgmlLinkExtractor(deny=[
            'https://bitcointalk\.org/index\.php\?action=ignore',
            'https://bitcointalk\.org/index\.php\?action=profile',
            ], 
            allow_domains='bitcointalk.org'), callback='parse_item', follow=True),
    )
    
    def parse_item(self, response):
        #print (type(response))
        items =[]
	
        
        posts =  response.xpath("//a[contains(@name,'msg')]/following-sibling::table[1]")
        for post in posts: 
         item = TutorialItem()
         author = ''.join(post.xpath('.//td[@class="poster_info"]/.//b/a/.//text()').extract())
         date =''.join(post.xpath('.//div[@class="subject"]/following-sibling::div/.//text()').extract())
         bitcoinkey = ''.join(post.xpath('.//div[contains(@class, "signature")]/text()').re(r'(1[1-9A-HJ-NP-Za-km-z]{26,33})'))
         if bitcoinkey:
             item['membername']= author
             if(bcv.check_bc(bitcoinkey)):
                 item["address"] = bitcoinkey                         
                 item["date"]= date
                 items.append(item)
             
         

        return items
        

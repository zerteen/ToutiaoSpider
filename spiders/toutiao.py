# encoding: utf-8
import sys
sys.path.append("C:\\Users\\xiongz\Desktop\\toutiaoScrppy\\toutiao\\toutiao");
import codecs 
import scrapy
from items import ToutiaoItem
import json
import urllib2
import re
reload(sys)
sys.setdefaultencoding('UTF-8')

class Toutiao(scrapy.Spider):
	"""头条爬虫类"""
	
	name = "toutiao"
	allowed_domain = ["toutiao.com"]
	start_time = 1513611635 # 2017-12-19
	end_time = 1493611635 # 2017-05-01
	start_urls = ["https://www.toutiao.com/api/pc/feed/?category=news_hot&_signature=NwfhqgAAbTjWrXQAnwT7aDcH4b"]
	base_class_url = "http://toutiao.com"
	categories = ["news_society","news_hot","news_tech","news_society","news_entertainment","news_game","news_sports","news_car","news_finance"]
	count = 0

	def parse(self, response):
		page = json.loads(response.body)
		# print page.keys()
		
		# print page["data"][0]
		# print len(page["data"])

		if page["data"]:
			for i in page["data"]:
				if not i.has_key("article_genre"):
					continue
				if i["article_genre"] != 'article':
					continue
				# print i["group_id"]
				# print i["Title"].encode("GBK", "ignore")
				# print i["chinese_tag"]
				# print i["abstract"].encode("GBK", "ignore")
				# print i["label"]
				print "Get url> https://www.toutiao/a"+i["group_id"]
				yield scrapy.Request(url="https://www.toutiao.com/a"+str(i["group_id"]), callback=self.artical_parse, priority=100)
		# 		self.count += 1
		# print self.count 
		self.start_time -= 2100
		if self.start_time > self.end_time:
			for category in self.categories:
				url = "https://www.toutiao.com/api/pc/feed/?category="+category+"&max_behot_time="+str(self.start_time)+"&_signature=NwfhqgAAbTjWrXQAnwT7aDcH4b"
				yield scrapy.Request(url,self.parse)

	def artical_parse(self, response):
		item = ToutiaoItem()
		page = response.body
		url = response.url
		comments = []
		search_title_article = re.search("articleInfo: {\n      title: '(.*?)',\n      content: '(.*?)'", page)
		search_source_time = re.search("source: '(.*?)',\n        time: '(.*?)'\n      },",page)
		search_tags = re.findall('{"name":"(.*?)"}', page)
		page_id = re.search("/a(.*?)$",response.url)
		print "1"
		comment_url = "https://www.toutiao.com/api/comment/list/?group_id="+page_id.group(1)+"&item_id="+page_id.group(1)
		request  = urllib2.Request(comment_url)  
		request.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")  
		print "2"
		
		try:
			response = urllib2.urlopen(request,timeout=15)
			page = response.read()
			comment_page = page.decode("utf-8","ignore") # 指定超时秒数，在规定时间内不返回结果，直接raise timeout
			comments = re.findall('"text": "(.*?)",',comment_page)   
		except urllib2.URLError as e:
			print e


		print "3"
		#>>> content = urllib2.urlopen('https://www.toutiao.com/api/comment/list/?group_id=6492177752957911565&item_id=6492177752957911565')
		# >>> text = content.read()
		# >>> re.findall('"text": "(.*?)",',text)

		if search_title_article and search_source_time and search_tags:
			item['Title'] = search_title_article.group(1).decode("utf-8", "ignore")
			# item['Article'] = search_title_article.group(2).decode("utf-8", "ignore")
			# result, number  =  re .subn(regex, newstring, subject)  &lt;/div&gt;
			item["Article"], num = re.subn("&lt;(.*?)&gt;","",search_title_article.group(2))
			item['URL'] = url
			item['Sources'] = search_source_time.group(1).decode('utf-8', "ignore")
			item['PublishTime'] = search_source_time.group(2).decode("utf-8","ignore")
			item['KeyWords'] = ','.join(search_tags)
			item['Comments'] = '\t'.join([i.decode('unicode_escape') for i in comments])
		print "4"
		yield item
		
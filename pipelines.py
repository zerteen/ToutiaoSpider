# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import threading
import json
import sys
import codecs
reload(sys)
sys.path.append("..")
class ToutiaoPipeline(object):
	# lock = threading.Lock()
	count = 0
	# file = open("test.json","a")


	def process_item(self, item, spider):
		ToutiaoPipeline.count += 1
		# file = open(str(self.count)+".json","w+")
		file = codecs.open(str(self.count)+".json",'w','utf-8')
		lines = json.dumps(dict(item), indent=4, separators=(',', ': '), ensure_ascii=False)
		# print lines
		try:
			# ToutiaoPipeline.lock.acquire()
			file.write(lines)
			
			print "write success!\n\n\n\n"
		except:
			print "pipeline wrong!!!"
		finally:
			# ToutiaoPipeline.lock.release()
			file.close()
			return item
	def close_spider(self, spider):
		pass

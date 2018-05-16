# coidng: utf-8
import json
import os
import sys
reload(sys)  
sys.setdefaultencoding('utf8') 

if __name__ == '__main__':
	folder = "data"
	target_folder = 'data_2'
	files = os.listdir(folder)
	if not os.path.exists(target_folder):
		os.mkdir(target_folder)
	for file in files:
		print "processing file:"+ file
		f = open(folder+'\\'+file,"r")
		text = ''.join(f.readlines())
		if text == "{}":
			continue
		j = json.loads(text)
		f.close()

		reply = 0
		total = 0

		comments = j["Comments"]

		title = j["Title"]
		url = j["URL"]
		source = j["Sources"]
		key = j["KeyWords"]
		article = j["Article"]
		time = j["PublishTime"]

		content = comments.split("\t")
		total = len(content)
		reply = 0
		content = ' '.join(content)
		link = url
		j = json.dumps({"KeyWords": key, "PublishTime": time, "Reply":reply, "Total": total, "Comment": content, "CLink": link,"Article": article, "URL": url, "Title": title, "Sources": source}, separators=(',', ': '),encoding="ascii",indent =4, sort_keys=False)


		f = open(target_folder +"\\"+file,"wb")
		f.write(j.decode('raw_unicode_escape'))
		f.close()
	print "done!"




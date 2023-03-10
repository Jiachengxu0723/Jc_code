import os
import json
import requests

from queue import Queue
from threading import Thread

from config import down_path
from utils import format_headers, get_baidu_obj_url

header = """
Host: image.baidu.com
Connection: keep-alive
sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"
Accept: text/plain, */*; q=0.01
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
"""
headers = format_headers(header)
#headers = header全路径

def get_image(url):

	# 获取接口的图片列表信息res
	res = requests.get(url, headers=headers)
	''' 
	json.loads #将文本res.txt通过json.loads转为字典
	strict=False #字符串中允许使用控制字符
	.get('data',[]) #获取字典里data对应的value,没有则返回[]
	'''
	data_list = json.loads(res.text, strict=False).get('data', [])
	# 遍历图片信息列表
	for data in data_list:
		obj_url = data.get('objURL')
		if obj_url:
			# 获取解密后的图片URL
			image_url = get_baidu_obj_url(obj_url)
			print(image_url)
			# todo 保存的名字(1.png)应为不重复的，比如自增字段;时间戳
			if not os.path.exists(down_path):
				os.makedirs(down_path)
			with open(os.path.join(down_path,'1.png'), 'wb') as w:
				connent = requests.get(image_url).content
				w.write(connent)



if __name__ == '__main__':
	# 要爬取的关键字
	keyword = '梅西'
	url_video = 'https://www.baidu.com/sf/vsearch?pd=video&wd=replace%28%29&tn=vsearch&lid=f1dcb307000ba693queryWord={keyword}&ie=utf-8&word={keyword}rsv_spt=7&rsv_bp=1&f=8'

	url = f'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&queryWord={keyword}&ie=utf-8&oe=utf-8&word={keyword}'
	# 拼凑页数参数 获取图片列表页URL
	search_url = url + f'&pn=0&rn=50'
	get_image(search_url)

	#多线程 提升效率
	# q = Queue()
	# for i in range(0, 31, 30):
	# 	search_url = url + f'&pn={i}&rn=30'
	# 	q.put(search_url)
	# while not q.empty():
	# 	thread_list = [Thread(target=get_image, args=(q.get(),)) for i in range(1) if not q.empty()]
	# 	[i.start() for i in thread_list]
	# 	[i.join() for i in thread_list]

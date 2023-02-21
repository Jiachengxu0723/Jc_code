import traceback

def get_baidu_obj_url(obj_url):
	"""
	解密百度图片，返回真实URL
	:param obj_url:
	:return:

	"""
	try:
		single_map = {"w": "a", "k": "b", "v": "c", "1": "d", "j": "e", "u": "f", "2": "g", "i": "h", "t": "i",
					  "3": "j", "h": "k", "s": "l", "4": "m", "g": "n", "5": "o", "r": "p", "q": "q", "6": "r",
					  "f": "s", "p": "t", "7": "u", "e": "v", "o": "w", "8": "1", "d": "2", "n": "3", "9": "4",
					  "c": "5", "m": "6", "0": "7", "b": "8", "l": "9", "a": "0"}

		multiple_map = {"_z2C$q": ":", "_z&e3B": ".", "AzdH3F": "/"}

		for k, v in multiple_map.items():
			#dict.items(key,value)返回可遍历的（键，值）元组数
			obj_url = obj_url.replace(k, v)
			#将obj_url中的k替换成v

		url = ""
		for i, str_ in enumerate(obj_url):
			if single_map.get(str_):
				url += single_map.get(str_)
			else:
				url += str_
		return url
	except Exception:
		traceback.print_exc()


def format_headers(string) -> dict:
	"""
	将在Chrome上复制下来的浏览器UA格式化成字典，以\n为切割点
	:param string: 使用三引号的字符串
	:return:
	"""
	string = string.strip().replace(' ', '').split('\n')
	#strip()去掉首位指定的字符，默认为空格
	#replace（'old','new',n）将字符串中old替换为new，替换不超过n次
	#dict.update（dict1）将dict1里的字典更新到dict字典里，如果key相同则覆盖
	new_headers = {}
	for key_value in string:
		key_value_list = key_value.split(':')
		if len(key_value_list) > 2:
			new_headers.update({key_value_list[0]: ':'.join(key_value_list[1::])})
		else:
			new_headers.update({key_value_list[0]: key_value_list[1]})
	return new_headers


if __name__ == '__main__':
	obj_url = "ipprf_z2C$qAzdH3FAzdH3F2t42d_z&e3Bkwt17_z&e3Bv54AzdH3Ft4w2j_fjw6viAzdH3Ff6v=ippr%nA%dF%dFckalbbjclcddc_z&e3Bv1g_z&e3Bf5i7vf_z&e3Bv54%dFt4w2jf%dFdadaadan%dFu9admdc08vj99ncmwbwv9cml8bu9wk9j_z&e3B3rj2&6juj6=ippr%nA%dF%dFckalbbjclcddc_z&e3Bv1g_z&e3Bf5i7vf_z&e3Bv54&wrr=daad&ftzj=ullll,8aaaa&q=wba&g=a&2=ag&u4p=3rj2?fjv=8m8bnbblb8&p=jc8kwu0j1wdd9c8dnk8ual89jwwlvl8b"
	print(get_baidu_obj_url(obj_url))

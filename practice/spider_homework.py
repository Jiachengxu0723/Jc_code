
import json,requests

keyword = '戴口罩'
url = f'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&queryWord={keyword}&ie=utf-8&oe=utf-8&word={keyword}'

res = requests.get(url)
print(res.text)
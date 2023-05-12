# -*-coding:utf-8-*-
import re
import requests
import os

def dowmloadPic(html,keyword,count):
    pic_url = re.findall('"objURL":"(.*?)",',html,re.S)
    i = 0
    dir = 'picture/' + keyword + '/'
    if not os.path.exists(dir):
        os.makedirs(dir)
    print ('找到关键词:'+keyword+'的图片，现在开始下载图片...')
    for each in pic_url:
        print ('正在下载第'+str(i+1)+'张图片，图片地址:'+str(each))
        try:
            pic= requests.get(each, timeout=3)
        except requests.exceptions.ConnectionError:
            print ('【错误】当前图片无法下载')
            continue
        #保存路径
        string = dir + keyword+'_'+str(i) + '.jpg'
        #解决编码问题，确保中文名称可以存储
        fp = open(string.encode('utf-8'),'wb')
        fp.write(pic.content)
        fp.close()
        i += 1
        if str(i) == str(count):
            print ('下载完毕')
            return

def main():
    word = input("请输入你要下载的图（中文）: ")
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&ct=201326592&v=flip'
    count_picture = input('请输入你要下载的数量（张）：')
    result = requests.get(url)
    dowmloadPic(result.text, word, count_picture)

if __name__ == '__main__':
    main()

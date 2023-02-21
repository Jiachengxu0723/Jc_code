# -*- coding:utf-8 -*-
#! python3
from PIL import Image

img = Image.open("/home/mrx/Downloads/1/t.png")#读取系统的内照片

width = img.size[0]#长度
height = img.size[1]#宽度
print(width)
print(height)

for a in range(1,width):#遍历所有长度的点
  for b in range(1,height):#遍历所有宽度的点

    data = (img.getpixel((a,b)))#打印该图片的所有点
    #打印每个像素点的颜色RGBA的值(r,g,b,alpha)

    if (data[0]>=170 and data[1]>=170 and data[2]>=170):#RGBA的r值大于170，并且g值大于170,并且b值大于170
      img.putpixel((a,b),(234,53,57,255))#则这些像素点的颜色改成大红色

img = img.convert("RGB")#把图片强制转成RGB
img.save("/home/mrx/Downloads/1/t.png")#保存修改像素点后的图片



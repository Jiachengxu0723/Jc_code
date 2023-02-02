# -*-coding:utf-8-*-
from PIL import Image

# 白色背景图片背景透明化
def transPNG(srcImageName):
    img = Image.open(srcImageName)
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = list()
    for item in datas:
        if item[0] > 220 and item[1] > 220 and item[2] > 220:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    return img

# 图片融合
def mix(file,mark,coordinator=(570, 640)):
    #new : 这个函数创建一幅给定模式（mode）和尺寸（size）的图片。如果省略 color 参数，则创建的图片被黑色填充满，如果 color 参数是 None 值，则图片还没初始化。
    layer = Image.new('RGBA', file.size, (0, 0, 0, 0))
    #粘贴新图片至图片中，box 参数可以为 2-元组（upper, left）或是 4-元组（left, upper, right, lower），或者是 None（0, 0）。2). 功能同上。不过是将指定位置填充为某种颜色。
    layer.paste(mark, coordinator)
    #composite : 使用两幅给出的图片和一个与 alpha 参数相似用法的 mask 参数，其值可为："1", "L", "RGBA" 。两幅图片的 size 必须相同。
    out = Image.composite(layer, file, layer)
    out.show()
    out.save('mix.jpg')

def main():
    file = Image.open('background.jpeg')
    verse = ('cup.jpeg')
    verse = transPNG(verse)
    file = mix(file, verse)

if __name__ == '__main__':
    main()


from PIL import Image

def read_img(file_path):
    img = Image.open(file_path)  # 读取系统的内照片
    img = img.convert("RGB")  # 把图片强制转成RGB
    width = img.size[0]  # 长度
    height = img.size[1]  # 宽度
    # print (img.size)打印图片大小
    #print (img.getpixel((4,4)))#返回（4，4）点的RGB
    return img,width,height

def JPicture_channel_type(img,width,height):
    color_list = []
    for i in range(0, width):  # 遍历所有长度的点
        for j in range(0, height):  # 遍历所有宽度的点
            pic_color = (img.getpixel((i, j)))  # 打印该图片的所有点
            if pic_color not in color_list:
                color_list.append(pic_color)
    print(color_list)
    return color_list

def Modify_picture_channel(img,color_list,width,height,file_path):
    for x in range(0, width):  # 遍历所有长度的点
        for y in range(0, height):
                if img.getpixel((x,y)) != color_list[5]:
                    img.putpixel((x, y), (255,165,79))

    img.show()
    #img.save(file_path)

if __name__ == '__main__':
    file_path = ("/home/mrx/Downloads/t3.png")
    img,width,height = read_img(file_path)
    color_list = JPicture_channel_type(img,width,height)
    Modify_picture_channel(img,color_list,width,height,file_path)



import matplotlib.pyplot as plt
import numpy as np
import random

def Guessing_game():
    print('猜谜游戏，您有10次机会')
    answer = random.randint(1,100)
    a = 0
    b = 100
    count = 0
    while count<10:
        try:
            num = input('请输入一个0-100的整数:')
            num = eval(num)

            if type(num)in [float]:
                print('请输入一个整数')

            elif num == answer:
                print('恭喜你，答对了')
                break

            elif num < answer:
                print('猜小了')

            elif num >b or num <a:
                print('请输入范围内的值')

            else:
                print('猜大了')

            count = count + 1
            if count == 9:
                print('还有最后一次机会')

            elif count == 10:
                print('&游戏失败&Eng')
                break

        except NameError:
            print('您输入的不是数字，请再次尝试输入！')

    print('———————————————————————————————————————————')

def Calculate_BMI():
    print('BMI计算')
    height = float(input('请输入你的身高cm:'))/100
    weight = float(input('请输入你的体重kg:'))
    BMI = float(weight/height**2)

    if BMI >18 and BMI <24.5:
        print('恭喜，您的体重在正常范围内：BIM=',BMI)

    elif BMI <18:
        print('您的体重过轻：BMI=',BMI)

    elif BMI >24 and BMI<=28:
        print('您的体重偏重：BMI=',BMI)

    else:
        print('您属于肥胖，BMI=',BMI)
    my_dpi = 96
    # 设置图的尺寸(480x480)
    plt.figure(figsize=(960 / my_dpi, 960 / my_dpi), dpi=my_dpi)

    # 设置柱子的高度
    height = [BMI, 18, 24]

    # 对每个柱子命名
    bars = ('your_BMI', 'healthy_Min', 'healthy_Max')
    y_pos = np.arange(len(bars))

    # 建立柱形图并设置颜色
    plt.bar(y_pos, height, color=(0.2, 0.4, 0.6, 0.6))
    plt.xticks(y_pos, bars)

    # 保存图片
    # plt.savefig('#3_control_color_barplot1.png')

    # 展示图片
    plt.show()


    print('———————————————————————————————————————————')

def read_txt():
    reviews = []

    with open('/home/mrx/Downloads/reviews.txt', 'r') as file:
        for msg in file:
            reviews.append(msg)

    print(len(reviews))
    thirtyth = reviews[29]
    isword = True
    checklist = 'abcdefghijklmnopqrstuvwxyz-'
    count = 0

    print(f"check list长这样{checklist}")
    for char in thirtyth:
        if isword:
            if not char.lower() in checklist:
                count += 1
                isword = False
            else:
                pass
        else:
            if char in checklist:
                isword = True
    print(count)

def write_txt():
    data = [i for i in range(20)]
    file_path = ('/home/mrx/下载/code/test.txt')

    with open(file_path, 'w') as file:
        for num in data:
            file.write(str(num) + '\n')
        print('write success')

if __name__ == '__main__':
    #write_txt()
    Guessing_game()
    #Calculate_BMI()
    #read_txt()




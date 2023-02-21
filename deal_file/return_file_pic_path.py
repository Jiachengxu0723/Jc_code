import os

def judge_picture(path):
    pic_list = os.listdir(path)
    for i in range(len(pic_list)):
        if pic_list[i].split('.')[-1] in ['jpg','png','jpge','bmw']:
            pic_path = os.path.join(path,pic_list[i])
            print(pic_path)
            return pic_path

if __name__ == '__main__':
    path = ('/home/synsense/桌面/picture')
    judge_picture(path)
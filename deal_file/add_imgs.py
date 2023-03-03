# -*-coding:utf-8-*-
import os
import shutil
import zipfile


def get_file(path, types='.png'):
    file_list = []
    for roots, dirs, files in os.walk(path):
        for file in files:
            filename, suffix = os.path.splitext(file)
            if types == suffix:
                file_list.append(os.path.join(roots, file))
    return sorted(file_list)


def parse_dir_path(path):
    info, _ = os.path.splitext(path)
    condition, person, light, basename = info.split('/')[-4:]

    return condition, person, light, basename


def zip_dir(dirname):
    z = zipfile.ZipFile(dirname, 'w', zipfile.ZIP_DEFLATED)
    for roots, dirs, files in os.walk(dirname):
        fpath = roots.replace(dirname, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''
        for file in files:
            z.write(os.path.join(roots, file), fpath + file)
    z.close()


def main():
    path = './test/'
    imgs_path = './raw_data/'

    files = sorted(os.listdir(path))
    count = 0
    for file in files:
        filename = file.split('.')[0]
        condition, person, light = filename.split('_')[0:3]
        basename = '_'.join(filename.split('_')[-2:])
        img_path = imgs_path + os.path.join(condition, person, light, basename)
        new_path = path + file + '/images'
        if not os.path.exists(new_path):
            shutil.copytree(img_path, new_path)
        count += 1
        print(f'{file} 已合并')
    print(f'共 {count} 个文件合并完成')

    pngs = get_file(path)
    for png in pngs:
        png_name = png.split('/')[-1]
        png_name = str(png_name)
        number = png_name.split('.')[0]
        new_number = number.zfill(6)
        new_name = 'frame_' + new_number + '.PNG'
        new_png = png.replace(png_name, new_name)
        if not os.path.exists(new_png):
            os.rename(png, new_png)

    count = 0
    for file in files:
        dirname = path + file + '.zip'
        zip_dir(dirname)
        count += 1
        print(f'{file} 已压缩')
    print(f'共 {count} 个文件压缩完成')

if __name__ == "__main__":
    main()
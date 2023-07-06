import os
import shutil
from tqdm import tqdm
from time import sleep
import sys


def get_file(path, types=['.dat', '.csv', '.mp4']):
    file_list = []

    for roots, dirs, files in os.walk(path):
        for file in files:
            suffix = os.path.splitext(file)[-1]
            if suffix in types:
                file_list.append(os.path.join(roots, file))

    return sorted(file_list)


def prase_file(file):
    file_name, suffix = os.path.basename(file).split('.')
    if suffix in ['csv', 'dat']:
        time_stamp, tag, device = file_name.split('_')[0:3]
    else:
        time_stamp, device = file_name.split('_')
        tag = None

    return time_stamp, tag, device


def video_convert(path):
    h264_file = get_file(path, types=['.h264'])
    for file in h264_file:
        mp4_file = file.replace('.h264', '.mp4')
        if not os.path.exists(mp4_file):
            os.system(f'MP4Box -add {file} {mp4_file}')


def convert_to_csv(path, TIMESTAMP_ORIGIN=1658246400000):
    dat_file = get_file(path, types=['.dat'])
    for file in dat_file:
        csv_file = file.replace('.dat', '.csv')
        if not os.path.exists(csv_file):
            with open(csv_file, 'w') as outputFile:
                with open(file, 'rb') as inputFile:
                    while True:
                        line = inputFile.read(16)  # 读取.dat文件的一行(dat文件每行为16字节)
                        if line:
                            id = int.from_bytes(line[2:6], byteorder='big', signed=False)
                            accXDec = round(int.from_bytes(line[10:12], byteorder='big', signed=True) * 0.00024414, 8)
                            accYDec = round(int.from_bytes(line[12:14], byteorder='big', signed=True) * 0.00024414, 8)
                            accZDec = round(int.from_bytes(line[14:], byteorder='big', signed=True) * 0.00024414, 8)
                            timestamp = int.from_bytes(line[6:10], byteorder='big', signed=False) + TIMESTAMP_ORIGIN
                            outputFile.write(f"{id},{accXDec},{accYDec},{accZDec},{timestamp}\n")
                        else:
                            break
            print(f'{file} convert successful!')


def get_dataset(path):
    csv_file = get_file(path, types=['.csv', '.mp4'])
    for file in csv_file:
        time_stamp, tag, device = prase_file(file)
        dir_path = os.path.join('./dataset', device, time_stamp)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        try:
            shutil.copy(file, dir_path)
        except:
            pass


def get_lossrate_bandwith(path):
    dst_file = get_file(path, types=['.csv'])
    for file in dst_file:
        with open(file, 'rb') as f:
            first_row = f.readline()
            for count, _ in enumerate(f, 2):
                pass
            total_row = count
            offset = -80
            f.seek(offset, 2)
            last_row = f.readlines()

        first_serial = int(first_row.decode().split(',')[0])
        startTime = int(first_row.decode().split(',')[-1])
        last_serial = int(last_row[-1].decode().split(',')[0])
        endTime = int(last_row[-1].decode().split(',')[-1])
        serial_Dvaule = last_serial - first_serial + 1
        Time_Dvalue = endTime - startTime

        bandwidth = serial_Dvaule / (Time_Dvalue / 1000)
        loss_rate = (serial_Dvaule - total_row) / serial_Dvaule

        if loss_rate > 0.1 or bandwidth - 200 > 50:
            loss_rate = '{:.2%}'.format(loss_rate)
            print(os.path.abspath(file) + f'   丢包率为 : {loss_rate},'
                                          f'   数据带宽为 : {bandwidth}')


def main():
    src_path = './'
    dst_path = './bulu'

    print('------------------------mp4文件转换-------------------------')
    video_convert(src_path)

    print('\n-----------------------csv文件转换------------------------')
    convert_to_csv(src_path)
    # get_dataset(src_path)

    print('\n-----------------------异常文件列表--------------------------')
    get_lossrate_bandwith(dst_path)


if __name__ == '__main__':
    main()

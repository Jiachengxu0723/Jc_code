import csv
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


continuous_classes = ['climbing_stairs', 'eating', 'walking', 'resting','jogging']
event_classes = ['fall', 'jump_vertical', 'sit_down', 'stand_up']
devices00 = ['tag39','tag41','tag44','tag02']
devices01 = ['tag40','tag42','tag45','tag03']


def get_file_list(path, types):
    '''
    遍历路径下的文件夹，找到所有文件
    '''

    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            suffix = os.path.splitext(file)[-1]         ###  os.path.splitext：分割路径，返回路径名和文件扩展名的元组。
            if suffix in types:
                file_list.append(os.path.join(root, file))

    return sorted(file_list)


def read_file(file):
    '''
    读取文件
    '''

    rows = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    rows = rows[:-1]        ###  该文件最后一行舍去

    return rows


def write_file(csv_file, rows):
    '''
    写入到文件
    '''

    with open(csv_file, 'w') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)


def updata_row(row):
    '''
    更新文件行列
    '''

    x_value = row[3]
    y_value = row[4]
    z_value = row[5]
    idx, time_stamp = row[6].split('time: ')
    new_row = [idx, x_value, y_value, z_value, time_stamp]

    return new_row


def updata_file(file):
    '''
    将更新后的行列写入新文件
    '''

    rows = read_file(file)
    new_row = []
    for row in rows:
        try:
            r = updata_row(row)
        except:
            pass            ###  文件中可能会有格式错误的行
        else:
            new_row.append(r)

    '''
    将更新后的文件存入新的文件夹
    '''
    csv_file = file + '.csv'
    if not os.path.exists(csv_file):
        write_file(csv_file, new_row)

    return csv_file


def parse_file_path(file_path):
    info, _ = os.path.splitext(file_path)
    if 'sample' in info:
        action_class, action = info.split('/')[2:4]
        person, filename = info.split('/')[-2:]
        return action_class, action, person, filename
    elif 'tag' in info:
        person = info.split('/')[-2]
        num, device = os.path.basename(info).split('_')[-2:]
        action = os.path.basename(info).split('_')[:-2]
        if len(action) == 2:
            action = '_'.join(action)
        else:
            action = action[0]
        return person, device, action, num
    else:
        person, device, action, num = info.split('/')[2:]
        return person, device, action, num


def dat_to_csv(dat_file, csv_file, TIMESTAMP_ORIGIN=1682474400000):
    with open(csv_file, 'w') as outputFile:
        with open(dat_file, 'rb') as inputFile:
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


def visualize_file(csv_file, img_file):
    '''
    对所有CSV文件进行数据可视化
    '''
    data = pd.read_csv(csv_file, header=None, names=['serial_num', 'x', 'y', 'z', 'time_stamp'])

    x = [np.float64(x) for x in data.x]
    y = [np.float64(y) for y in data.y]
    z = [np.float64(z) for z in data.z]

    plt.figure(figsize=(20, 10))
    plt.plot(range(len(x)), x, label="x", c="#ff7f0e")
    plt.plot(range(len(y)), y, label="y", c="#1f77b4")
    plt.plot(range(len(z)), z, label="z", c="#2ca02c")

    plt.legend()
    plt.savefig(img_file, format="jpg", dpi=300)
    plt.clf()
    plt.close()


def get_duration(dir_path):
    csv_file_list = get_file_list(dir_path, types=['.csv'])
    durations = []
    for csv_file in csv_file_list:
        action_class, action, person, filename = parse_file_path(csv_file)
        with open(csv_file, 'rb') as f:
            first_row = f.readline()
            for count, _ in enumerate(f, 2):
                pass
            offset = -80
            f.seek(offset, 2)
            last_row = f.readlines()

            startTime = float(first_row.decode().split(',')[-1])
            endTime = float(last_row[-1].decode().split(',')[-1])
            duration = (endTime - startTime)/1000
            durations.append([action_class, action, person, filename, duration])
    df_duration = pd.DataFrame(durations, columns=['class', 'action', 'person', 'filename', 'duration'])
    df_duration.to_csv('duration.csv', index=False)


def get_lossrate_bandwith(csv_file):
        with open(csv_file, 'rb') as f:
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

        return  bandwidth, loss_rate


def clear_data(csv_file):
    bandwidth, loss_rate = get_lossrate_bandwith(csv_file)
    if abs(bandwidth - 200) > 50:
        df = pd.read_csv(csv_file, header=None)
        df.columns = ['Serial_number', 'X', 'Y', 'Z', 'timestamp']
        df['time_diff'] = df['timestamp'].diff(periods=1)
        for i, value in list(enumerate(df['time_diff']))[1:]:
            if abs(value)>500:
                df_new = df.drop(df.head(i+1).index)
                df_new = df_new.drop(['time_diff'], axis=1)
                print(df_new)
                df_new.to_csv(csv_file, header=False, index=False)

    if loss_rate>0.05:
        if 'device00' in csv_file:
            another_csv_file = csv_file.replace('device00', 'device01')
        else:
            another_csv_file = csv_file.replace('device01', 'device00')

        action = csv_file.split('/')[-4]
        for adition_file in addition_file_list:
            if action in adition_file:
                if 'tag44' in adition_file:
                    another_adition_file = adition_file.replace('tag44', 'tag45')
                elif 'tag45' in adition_file:
                    another_adition_file = adition_file.replace('tag45', 'tag44')
                elif 'tag28' in adition_file:
                    another_adition_file = adition_file.replace('tag28', 'tag29')
                else:
                    another_adition_file = adition_file.replace('tag29', 'tag28')

                if 'device00' in csv_file:
                    dat_to_csv(adition_file, csv_file)
                    dat_to_csv(another_adition_file, csv_file)
                else:
                    dat_to_csv(another_adition_file, csv_file)
                    dat_to_csv(adition_file, another_csv_file)

                addition_file_list.remove(adition_file)
                addition_file_list.remove(another_adition_file)
                break


def get_dataset():
    file_list = get_file_list(rawdata_path, types='')
    count = 0
    for file in file_list:
        csv_file = updata_file(file)
        person, device, action, num = parse_file_path(csv_file)
        if device in devices00:
            filename = '_'.join(['sample', num, 'device00'])
        else:
            filename = '_'.join(['sample', num, 'device01'])

        if action in continuous_classes:
            new_csv_file = os.path.join(dataset_path, 'continuous_classes', action, 'data', person, filename) + '.csv'
        else:
            new_csv_file = os.path.join(dataset_path, 'event_classes', action, 'data', person, filename) + '.csv'

        csv_dir,_ = os.path.split(new_csv_file)
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        if not os.path.exists(csv_file):
            shutil.copyfile(csv_file, new_csv_file)

        img_file = new_csv_file.replace('data', 'line_chart').replace('.csv', '.jpg')
        img_dir,_ = os.path.split(img_file)
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        if not os.path.exists(img_file):
            visualize_file(csv_file, img_file)

        print(file)
        os.remove(csv_file)
        count+=1
    print(f'共处理{count}个文件')


def get_dataset_eartag():
    dat_file_list = get_file_list(rawdata_path, types='.dat')
    count = 0
    for dat_file in dat_file_list:
        person, device, action, num = parse_file_path(dat_file)
        if device in devices00:
            filename = '_'.join(['sample', num, 'device00'])
        else:
            filename = '_'.join(['sample', num, 'device01'])

        if action in continuous_classes:
            csv_file = os.path.join(dataset_path, 'continuous_classes', action, 'data', person, filename) + '.csv'
        else:
            csv_file = os.path.join(dataset_path, 'event_classes', action, 'data', person, filename) + '.csv'

        csv_dir,_ = os.path.split(csv_file)
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        if not os.path.exists(csv_file):
            dat_to_csv(dat_file, csv_file)
            # get_lossrate_bandwith(csv_file)

        # img_file = csv_file.replace('data', 'line_chart').replace('.csv', '.jpg')
        # img_dir,_ = os.path.split(img_file)
        # if not os.path.exists(img_dir):
        #     os.makedirs(img_dir)
        # if not os.path.exists(img_file):
        #     visualize_file(csv_file, img_file)

        print(csv_file)
        count+=1
    print(f'共处理{count}个文件')


if __name__ == '__main__':
    rawdata_path = '20230510/Raw_data'
    dataset_path = '20230510/Dataset'

    # get_dataset_eartag()
    # get_duration(dataset_path)

    csv_files = get_file_list(dataset_path, types='.csv')
    addition_file_list = get_file_list('20230510/Raw_data/补录丢包率', types='.dat')

    for csv_file in csv_files:
        bandwidth, loss_rate = get_lossrate_bandwith(csv_file)
        # clear_data(csv_file)
        filename = '/'.join(csv_file.split('/')[-4:])
        if loss_rate > 0.05 or abs(bandwidth - 200) > 50:
            loss_rate = '{:.2%}'.format(loss_rate)
            print(filename + f'   丢包率为 : {loss_rate},'
                         f'   数据带宽为 : {bandwidth}')




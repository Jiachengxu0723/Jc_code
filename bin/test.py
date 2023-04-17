import csv
import os
import struct

def get_file_list(directory, ftype='.bin'):
    bin_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(ftype):
                bin_files.append(os.path.join(root, file))
    return bin_files

def read_csv_file(file_name):
    data = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    data = data[1:]
    return data

def save_events_to_file(events, filename):
    fpath, _ = os.path.split(filename)
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    with open(filename, 'wb+') as f:
        for event in events:
            x, y, p, t = event
            f.write((x).to_bytes(4, byteorder = 'little'))
            f.write((y).to_bytes(4, byteorder = 'little'))
            f.write((p).to_bytes(4, byteorder = 'little'))
            f.write((t).to_bytes(4, byteorder = 'little'))
    print('writting finished')

def read_events_from_bin_file(filename):
    events = []
    with open(filename, 'rb') as f:
        while True:
            # 每个事件共有16个字节（每个属性4个字节）
            event_data = f.read(16)
            if len(event_data) == 16:
                x, y, p, t = struct.unpack('<4I', event_data)  # 使用little-endian字节序解析uint型数据
                t &= 0xffffffff
                events.append((x, y, p, t))
            else:
                break
    return events

def parse_file(filename):
    clips = []
    csv_file = filename.replace('.bin', '.csv')
    if os.path.exists(csv_file):
        rows = read_csv_file(csv_file)
        events = read_events_from_bin_file(filename)
        for row in rows:
            _, _, start_id, end_id, label = [int(v) for v in row]
            events_clip = events[start_id:end_id]
            clips.append((events_clip, label))
    return clips

if __name__ == '__main__':
    root = './1st_data'
    save_dir = './data_post'
    label_nums = {}
    file_list = get_file_list(root, '.bin')
    for file in file_list:
        clips = parse_file(file)
        for clip in clips:
            events, label = clip
            num = label_nums.get(label, 1)
            save_filename = os.path.join(save_dir, f'c{str(label).zfill(2)}/c{str(label).zfill(2)}_{str(num).zfill(4)}.bin')
            label_nums[label] = num + 1
            save_events_to_file(events, save_filename)

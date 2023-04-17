import numpy as np
import os
import cv2
import numpy as np
import socket
import struct
from typing import Tuple, List

import pandas as pd


def free_port():
    """
    Determines a free port using sockets.
    """
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind(('0.0.0.0', 0))
    free_socket.listen(5)
    port = free_socket.getsockname()[1]
    free_socket.close()
    return port

def read_events_from_bin(filename):
    """Define the data type for the binary data.

    Args:
        filename(str): The name of the binary file to be read.

    Returns:
        events: A structured NumPy array that contains the data from the binary file.
    """
    dtype = np.dtype([('x', 'i4'), ('y', 'i4'), ('p', 'i4'), ('t', 'i4')])

    # Read binary data from the file.
    data = np.fromfile(filename, dtype)

    # Convert the binary data into a structured NumPy array.
    events = make_structured_array(data['x'], data['y'], data['t'], data['p'])

    return events


def read_events_from_aedat4(filename):
    """
    Get the aer events from version 4 of .aedat file

    Args:
        in_file: str The name of the .aedat file
    Returns:
        shape (Tuple): Shape of the sensor (height, width)
        xytp:   numpy structured array of events
    """
    with AedatFile(filename) as f:
        shape = f['events'].size
        x, y, t, p = [], [], [], []
        for packet in f.numpy_packet_iterator("events"):
            x.append(packet["x"])
            y.append(packet["y"])
            t.append(packet["timestamp"])
            p.append(packet["polarity"])
    x = np.hstack(x)
    y = np.hstack(y)
    t = np.hstack(t)
    p = np.hstack(p)
    events = make_structured_array(x, y, t, p)
    return events

def read_events_from_aedat(filename):
    """
    Get the aer events from DVS with ibm gesture dataset

    Args:
        filename:   filename
    Returns:
        shape (tuple):
            (height, width) of the sensor array
        xytp: numpy structured array of events
    """
    data_version, data_start = parse_header_from_file(filename)
    all_events = get_aer_events_from_file(filename, data_version, data_start)
    all_addr = all_events["address"]
    t = all_events["timeStamp"]

    # x = (all_addr >> 17) & 0x007F
    # y = (all_addr >> 2) & 0x007F
    # p = (all_addr >> 1) & 0x1

    x = (all_addr >> 17) & 0x00001FFF
    y = (all_addr >> 2) & 0x00001FFF
    p = (all_addr >> 1) & 0x00000001

    xytp = make_structured_array(x, y, t, p)
    return xytp

def parse_header_from_file(filename):
    """
    Get the aedat file version and start index of the binary data.

    Args:

        filename (str):     The name of the .aedat file

    Returns:
        data_version (float):   The version of the .aedat file
        data_start (int):       The start index of the data
    """
    filename = os.path.expanduser(filename)
    assert os.path.isfile(filename), f"The .aedat file '{filename}' does not exist."
    f = open(filename, "rb")
    count = 1
    is_comment = "#" in str(f.read(count))

    while is_comment:
        # Read the rest of the line
        head = str(f.readline())
        if "!AER-DAT" in head:
            data_version = float(head[head.find("!AER-DAT") + 8: -5])
        is_comment = "#" in str(f.read(1))
        count += 1
    data_start = f.seek(-1, 1)
    f.close()
    return data_version, data_start

def get_aer_events_from_file(filename, data_version, data_start):
    """
    Get aer events from an aer file.

    Args:
        filename (str):         The name of the .aedat file
        data_version (float):   The version of the .aedat file
        data_start (int):       The start index of the data

    Returns:
         all_events:          Numpy structured array:
                                  ['address'] the address of a neuron which fires
                                  ['timeStamp'] the timeStamp in mus when a neuron fires
    """
    filename = os.path.expanduser(filename)
    assert os.path.isfile(filename), \
        "The .aedat file does not exist."
    f = open(filename, "rb")
    f.seek(data_start)

    if 2 <= data_version < 3:
        event_dtype = np.dtype([("address", ">u4"), ("timeStamp", ">u4")])
        all_events = np.fromfile(f, event_dtype)
    elif data_version > 3:
        event_dtype = np.dtype([("address", "<u4"), ("timeStamp", "<u4")])
        event_list = []
        while True:
            header = f.read(28)
            if not header or len(header) == 0:
                break

            # read header
            capacity = struct.unpack("I", header[16:20])[0]
            event_list.append(np.fromfile(f, event_dtype, capacity))
        all_events = np.concatenate(event_list)
    else:
        raise NotImplementedError()
    f.close()
    return all_events


def cut_events(events, start=0, end=1):
    length = events.shape[0]
    if start <= 1:
        start = int(start*length)
    if end <= 1:
        end = int(end*length)
    events = events[start:end]
    return events

def dvs_frame_to_im(frame):
    frame_p0 = frame[0]
    frame_p1 = frame[1]
    frame_total = frame[0] + frame[1]
    im = np.zeros((frame.shape[1], frame.shape[2], 3))
    im[:, :, 1] = frame_total
    im = im.astype(np.uint8)
    return im

def load_filedir(record_filename, filedir = '/home'):
    if os.path.exists(record_filename):
        with open(record_filename, 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                filename = lines[0].strip()
                filedir, _ = os.path.split(filename)
    return filedir

def save_filename_to_file(filename, record_filename='record.txt'):
    with open(record_filename, 'w') as f:
        f.write(filename+'\n')    

def slice_by_time(xytp: np.ndarray, time_window:int, overlap:int = 0, include_incomplete=False):
    """
    Return xytp split according to fixed timewindow and overlap size
    <        <overlap>        >
    |   window1      |
             |   window2      |

    Args:
        xytp: np.ndarray
            Structured array of events
        time_window: int
            Length of time for each xytp (ms)
        overlap: int
            Length of time of overlapping (ms)
        include_incomplete: bool
            include incomplete slices ie potentially the last xytp

    Returns:
        slices List[np.ndarray]: Data slices

    """
    t = xytp["t"]
    stride = time_window - overlap
    assert stride > 0

    if include_incomplete:
        n_slices = int(np.ceil(((t[-1] - t[0]) - time_window) / stride) + 1)
    else:
        n_slices = int(np.floor(((t[-1] - t[0]) - time_window) / stride) + 1)
    n_slices = max(n_slices, 1) # for strides larger than recording time

    tw_start = np.arange(n_slices)*stride + t[0]
    tw_end = tw_start + time_window
    indices_start = np.searchsorted(t, tw_start)
    indices_end = np.searchsorted(t, tw_end)
    sliced_xytp = [xytp[indices_start[i]:indices_end[i]] for i in range(n_slices)]
    return sliced_xytp


def slice_by_count(xytp: np.ndarray, spike_count: int, overlap: int = 0, include_incomplete=False):
    """
    Return xytp sliced nto equal number of events specified by spike_count

    Args:
        xytp (np.ndarray):  Structured array of events
        spike_count (int):  Number of events per xytp
        overlap: int
            No. of spikes overlapping in the following xytp(ms)
        include_incomplete: bool
            include incomplete slices ie potentially the last xytp
    Returns:
        slices (List[np.ndarray]): Data slices
    """
    n_spk = len(xytp)
    spike_count = min(spike_count, n_spk)
    stride = spike_count - overlap
    assert stride > 0

    if include_incomplete:
        n_slices = int(np.ceil((n_spk - spike_count) / stride) + 1)
    else:
        n_slices = int(np.floor((n_spk - spike_count) / stride) + 1)

    indices_start = np.arange(n_slices)*stride
    indices_end = indices_start + spike_count
    sliced_xytp = [xytp[indices_start[i]:indices_end[i]] for i in range(n_slices)]
    return sliced_xytp

def accumulate_frames(list_xytp: List[np.ndarray], bins_y, bins_x) -> np.ndarray:
    """
    Convert xytp event lists to frames

    Args:
        list_xytp (List[np.ndarray]): A *list* of xytp, where each element in the list is a structured array of events
        bins_y (ListLike):  Bins to use for creating the frame
        bins_x (ListLike):  Bins to use for creating the frame

        Note: bins_y and bins_x are typically range(0, height_of_sensor) and range(0, width_of_sensor)
    Returns:
        raster: (np.ndaray): Numpy array with dimensions [N, polarity, height, width], where N is the length of list_xytp
    """
    frames = np.empty((len(list_xytp), 2, len(bins_y) - 1, len(bins_x) - 1), dtype=np.uint16)
    for i, slice_item in enumerate(list_xytp):
        frames[i] = np.histogramdd((slice_item["p"], slice_item["y"], slice_item["x"]),
                                   bins=((-1, 0.5, 2), bins_y, bins_x))[0]
    return frames




def make_structured_array(x, y, t, p):
    events_struct = [("x", np.uint16), ("y", np.uint16), ("t", np.uint64), ("p", bool)]
    """
    Make a structured array given lists of x, y, t, p

    Args:
        x: List of x values
        y: List of y values
        t: List of times
        p: List of polarities boolean
    Returns:
        xytp: numpy structured array
    """
    return np.fromiter(zip(x, y, t, p), dtype=events_struct)

def events_to_im(events, h=128, w=128):
    frame = accumulate_frames([events],range(h+1), range(w+1))
    frame = frame.astype(np.uint8)
    frame = frame.squeeze(axis=0)
    zero_background = np.zeros((1, h, w), dtype=np.uint8)
    frame = np.concatenate([frame, zero_background], axis=0)
    frame = np.transpose(frame, (1, 2, 0))
    frame = frame[:,:,[2,1,0]]
    frame *= 1000
    frame = np.clip(frame, 0, 255)
    im = frame.astype(np.uint8)
    return im

def next_filename(filename):
    if '_' not in filename:
        return filename
    splits = filename.split('_')
    try:
        num_str = splits[-1]
        num = int(num_str)
    except:
        return filename
    num += 1
    len_num = len(num_str)
    num_str = str(num).zfill(len_num)
    splits[-1] = num_str
    filename = '_'.join(splits)
    return filename

def get_dis(pt1, pt2):
    import math
    dis = math.sqrt((pt2[0]-pt1[0])**2+(pt2[1]-pt1[1])**2)
    return dis

def draw_horizontal_lines(im, num=2, color=(255, 255, 255), thickness=1):
    x_start = 0
    x_end = im.shape[1] - 1
    gap = int(im.shape[0] / num)
    im = np.ascontiguousarray(im)
    for i in range(1, num): 
        cv2.line(im, (x_start, gap*i), (x_end, gap*i), color, thickness)
    return im


def draw_vertical_lines(im, num=2, color=(255, 255, 255), thickness=1):
    y_start = 0
    y_end = im.shape[0] - 1
    gap = int(im.shape[1] / num)
    im = np.ascontiguousarray(im)
    for i in range(1, num):  
        cv2.line(im, (gap*i, y_start), (gap*i, y_end), color, thickness)
    return im

def draw_grids(im, row_num = 1, col_num = 1):
    if row_num > 1:
        im = draw_horizontal_lines(im, row_num)
    if col_num > 1:
        im = draw_vertical_lines(im, col_num)
    return im 


def get_file_list(directory, types = ['.jpg'], is_sort = True):
    r"""
    Get the list of all file names with certain types in a directory
    Args:
        directory(string): the directory that contains all files
    Returns:
        file_list(List[str]): List of all the required files
    """
    file_list = []
    for path, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in types:
                file_list.append(os.path.join(path, file))
    if is_sort:
        file_list.sort()
    return file_list


def split_list_average_n(origin_list, n):
    for i in range(0, len(origin_list), n):
        yield origin_list[i:i + n]


def parse_bin_file(filename):
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


def events_to_file(events, file):
    filename,_ = os.path.splitext(file)
    with open(f'{filename}_{i}.bin', 'ab+') as f:
        for event in events:
            x, y, t, p = event
            f.write(int(x).to_bytes(4, byteorder='little'))
            f.write(int(y).to_bytes(4, byteorder='little'))
            f.write(int(p).to_bytes(4, byteorder='little'))
            f.write(int(t).to_bytes(4, byteorder='little'))


def read_csv(csv_file):
    head_row = pd.read_csv(csv_file, nrows=0)
    head_row_list = list(head_row)

    # 读取
    csv_result = pd.read_csv(csv_file, usecols=head_row_list)
    row_list = csv_result.values.tolist()
    labels = []
    for row in row_list:
        start = int(row[2])
        end = int(row[3])
        labels.append([start,end])

    return labels


if __name__ == "__main__":
    # bin_files = get_file_list('./', types=['.bin'])
    #
    # for bin_file in bin_files:
    #     data = read_events_from_bin(bin_file)
    #     csv_file = bin_file.replace('bin','csv')
    #     labels = read_csv(csv_file)
    #     i = 1
    #
    #     for label in labels:
    #         start, end = label
    #         slice_data = data[start: end]
    #         events_to_file(slice_data, bin_file)
    #         i+=1
    #     print(f'{bin_file}剪切完成')

        # n = int(len(data)/5)
        # slice_data = split_list_average_n(data, n)
        # i = 1
        # for each in slice_data:
        #     events_to_file(each, bin_file)
        #     i+=1

    events = parse_bin_file('sample_001.bin')





import os
import sys
import struct
from argparse import ArgumentParser
import numpy as np

def read_events_from_bin(filename: str) -> np.ndarray:
    """
    Read events from the recorded .bin file

    Args:
        filename: the bin file

    Returns:
        numpy structured array
    """
    dtype = np.dtype([("x", "u4"), ("y", "u4"), ("p", "u4"), ("t", "u4")])
    events = np.fromfile(filename, dtype)
    return events

def save_events_to_bin(events: np.ndarray, save_path: str)-> None:
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))

    # save flipped events
    if os.path.exists(save_path):
        os.remove(save_path)
    with open(save_path, mode="wb+") as f:
        for event in events:
            for item in event:
                f.write(struct.pack("I", item))

def vertical_flip(events: np.array, resolution: tuple) -> np.ndarray:
    """
    flip event data vertically

    Args:
        events:
        resolution: (width, height)

    Returns:
        vertically flipped events
    """

    height = resolution[1]

    events["y"] = (height - 1) - events["y"]
    return events

def horizonal_flip(events: np.array, resolution: tuple) -> None:
    """
    flip event data horizonally

    Args:
        events
        resolution: (width, height)

    Returns:
        horizonally flipped events
    """

    width = resolution[0]
    events["x"] = (width - 1) - events["x"]
    return events

def get_file_list(directory, types , is_sort = True) -> list:
    r"""
    Get the list of all files names with certain types in a directory
    Args:
        directory(string): the directory that contains all files
        types(List[str]):
        is_sort:
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

def main(bin_dir):
    """
        Invert the events of all bin files in the folder vertically and horizontally

        Args:
            bin_dir: Directory containing bin files

        """
    file_list = get_file_list(
        directory=bin_dir, types=['.bin'])
    if len(file_list) == 0:
        print('该目录没有.bin文件')
    else:
        for files in file_list:
            events = read_events_from_bin(files)
            events = vertical_flip(events, resolution=(128, 128))
            events = horizonal_flip(events, resolution=(128, 128))
            save_events_to_bin(events, save_path=files)
            print(f'{files}已转换成功')

if __name__ == '__main__':
    #需要翻转的bin文件目录
    bin_dir = input('请输入需要翻转的文件夹绝对路径：')
    main(bin_dir)

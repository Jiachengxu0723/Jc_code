import enum
import os
import struct
import sys
from argparse import ArgumentParser
from typing import List

import numpy as np
import pandas as pd


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


def save_events_to_bin(events: np.ndarray, save_path: str):
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))

    # save flipped events
    if os.path.exists(save_path):
        os.remove(save_path)
    with open(save_path, "ab+") as f:
        for event in events:
            for item in event:
                f.write(struct.pack("I", item))


def parse_csv_bin(csv_path: str) -> List[tuple]:
    """Parse the annotation of the .bin file from its correlated .csv file.

    :param csv_path: the csv file
    :return: a list contain the annotation, each element in this list is a 3-tuple
    (class, start_time, end_time)
    """
    csv_df = pd.read_csv(csv_path)
    annotation = []
    for _, data in csv_df.iterrows():
        cls_lb = int(data["classification"])  # class label
        start = int(data["startTime"])  # start time
        end = int(data["endTime"])  # end time
        annotation.append((cls_lb, start, end))
    return annotation


def main(bin_file):
    """
        Invert the events of all bin files in the folder vertically and horizontally

        Args:
            bin_dir: Directory containing bin files

        """  
    
    anno_file = bin_file.replace(".bin", ".csv")
    samples_info = parse_csv_bin(anno_file)
    events = read_events_from_bin(bin_file)

    for i, info in enumerate(samples_info):
        lb, start_t, end_t = info
        events_idx = np.argwhere(
            (events["t"] >= start_t) & (events["t"] <= end_t)
        )
        sliced_events = events[events_idx].squeeze(-1)
        sliced_bin_file = bin_file.replace(".bin", f"_{i}.bin")
        save_events_to_bin(sliced_events, save_path=sliced_bin_file)


if __name__ == '__main__':
    #bin文件目录
    bin_file = '/home/synsense/图片/data/normal/c01_0001.bin'
    main(bin_file)

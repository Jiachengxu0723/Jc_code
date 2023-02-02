# -*-coding:utf-8-*-
'''
一个二进制文件(.bin)， 里面存放了很多事件，每个事件由x,y,p,t这4个值构成，这4个值都是int型4个字节，在文件中依次存放，byteorder是little, 从这个文件中把这些事件读取出来，读取成一个事件列表，
使用Python的struct模块来读取二进制文件中的数据，并将读取的事件存储到列表中。
'''

import struct

def main(file):
    # 打开二进制文件，以二进制读的方式打开
    with open(file, "rb") as binary_file:
        # 定义一个事件的大小，即 4 个 int 型数据，每个数据 4 个字节，总共 16 字节
        event_size = 4 * 4

        # 定义事件列表
        events = []

        # 读取整个文件中所有的数据
        binary_data = binary_file.read()

        # 计算有多少个事件
        event_count = len(binary_data) // event_size

        # 遍历所有事件
        for i in range(event_count):
            # 定义偏移量
            offset = i * event_size

            # 使用 struct 模块从二进制数据中解析出 4 个 int 型数据
            x, y, p, t = struct.unpack("<iiii", binary_data[offset:offset + event_size])

            # 将解析出的事件加入事件列表
            events.append((x, y, p, t))

    # 输出事件列表
    print("Events:", events)
if __name__ == '__main__':
    file = '/home/synsense/下载/in&out_switch_mine/person003_96lux/unfilter_person003_96lux_switch_indoor.bin'
    main(file)
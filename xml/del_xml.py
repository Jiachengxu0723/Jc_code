import xml.etree.cElementTree as ET
import os
import tqdm

def get_file_list(directory, types , is_sort = True)->list:
    '''
        读取目录中所有非隐藏的xml文件，返回其路径列表
        Args:
            directory:目录路径
            types:需要的文件类型
    '''
    file_list = []
    for path, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in types and '.idea' not in path.split('/'):
                file_list.append(os.path.join(path, file))
    if is_sort:
        file_list.sort()
    return file_list


def del_xml_outside1(root,tree,files):
    '''
        删除xml文件里帧数单独不连续且outside="1的节点，并打印其帧数
        Args:

    '''

    tracks_info = root.findall("track")
    i=0
    for track in tracks_info:
        boxes = track.findall("box")
        list = []
        for box in boxes:
            outside = box.get("outside")
            frame = int(box.get("frame"))
            list.append(frame)
            if frame - 1 not in list and outside == "1":
                i+=1
                print(f"{files}--->第{frame}帧已删除")
                track.remove(box)

    tree.write(files)
    if i == 0:
        print('无修改操作')
    print('-----**************-----')


def connect_xml_label(root,tree,files):
    tracks_info = root.findall("track")
    list_id_frames=[]
    for track in tracks_info:
        boxes = track.findall("box")
        label = track.get("label")
        id = int(track.get("id"))

        track_first_frame = int(boxes[0].get("frame"))
        track_last_frame = int(boxes[-1].get("frame"))

        list_id_frames.append((track_first_frame,track_last_frame))
        list_id_frames.sort(key=lambda x:x[0],reverse=False)
    #print(list_id_frames)
    for number in range(len(list_id_frames)):
        dic_id_frames={number:list_id_frames[number]}
        if dic_id_frames[number][1] == dic_id_frames[number][0]:
            print(dic_id_frames[number][0])


def main():
    #读取目录中所有非隐藏的xml文件，返回其路径列表
    file_list = get_file_list(directory='/home/synsense/下载/c001_001 (1)',types=['.xml'])
    for files in file_list:
        tree = ET.parse(files)
        root = tree.getroot()
        #删除xml文件里帧数单独不连续且outside="1的节点，并打印其帧数
        del_xml_outside1(root,tree,files)
        #
        connect_xml_label(root,tree,files)


if __name__ == '__main__':
    main()
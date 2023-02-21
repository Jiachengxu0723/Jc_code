from lxml import etree
from shutil import copy
import os
from tqdm import tqdm


if __name__ == '__main__':
    for path, d, filelist in os.walk("C:\\Users\\byb\\Desktop\\2rd_face_detect_2"):
        for filename in tqdm(filelist, ascii=True, desc="遍历xml文件："):
            if filename.endswith('xml'):
                tree = etree.parse(path + '\\' + filename)
                root = tree.getroot()
                for enode in root:
                    if enode.tag == "object":
                        for obj in enode:
                            if obj.tag == "name" and obj.text == 'eye_undetemined':
                                obj.text = 'eye_undetermined'

                                save_path = 'C:\\Users\\byb\\Desktop\\2rd_face_detect_2' #+ '\\' + path.split('\\')[-1]




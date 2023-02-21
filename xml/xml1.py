import xml.etree.ElementTree as ET
from lxml import etree
import codecs
import os


class Modify:
    """
    修改xml文件中的object，包括增加和删除
    """
    def __init__(self, input_path, output_path):
        self.xmls_path = input_path
        self.save_path = output_path

    def prettify(self, elem):
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf8')
        root = etree.fromstring(rough_string)
        return etree.tostring(root, pretty_print=True, encoding='utf8').replace("  ".encode(), "\t".encode())

    # 删除object节点
    def del_obj(self, xml_root, classname='hand_fist'):
        objs = xml_root.findall('object')
        num = 0
        for obj in objs:
            name = obj.find('name').text
            if name == classname:
                num += 1


        return xml_root, num

    # 增加object节点
    def add_obj(self, filename, classname='person'):
        xml_path = os.path.join(self.xmls_path, filename)
        xml_root = ET.parse(xml_path).getroot()




    def alter_obj(self, xml_label,classname = 'eye_undetemined'):
        objs = xml_label.findall('object')
        num = 0
        for obj in objs:
            database = SubElement(obj, 'name')
            if database.text == classname:
                database.text = 'eye_undetermined'



        return xml_root

    # 保存修改后的xml文件
    def save(self, xml_root, filename):
        str_root = self.prettify(xml_root)
        file_path = os.path.join(self.save_path, filename)
        out_file = codecs.open(file_path, 'w', encoding='utf8')
        out_file.write(str_root.decode('utf8'))
        out_file.close()


if __name__ == "__main__":
    path = "C:/Users/byb/Desktop/2rd_face_detect_2/"
    save_path = "C:/Users/byb/Desktop/2rd_face_detect_2/"
    os.makedirs(save_path,exit_ok = True)
    m = Modify(path, save_path)
    xmls = os.listdir(path)
    labelnames = ['hand_fist']
    hand_fist_num = 0
    for xml in xmls:
        print("processing -------**********------- ", xml)
        xml_path = os.path.join(path, xml)
        root = ET.parse(xml_path).getroot()
        new_root, num = m.del_obj(root, labelnames[0])
        # m.save(new_root, xml)
        m.alter_obj(xml_label,classname)

        hand_fist_num += num
        print("num is ", hand_fist_num)

        # if hand_fist_num > 1000:
        #     break

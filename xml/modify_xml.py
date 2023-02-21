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
                xml_root.remove(obj)

        return xml_root, num

    # 增加object节点
    def add_obj(self, filename, classname='person'):
        xml_path = os.path.join(self.xmls_path, filename)
        xml_root = ET.parse(xml_path).getroot()

        return xml_root

    # 保存修改后的xml文件
    def save(self, xml_root, filename):
        str_root = self.prettify(xml_root)
        file_path = os.path.join(self.save_path, filename)
        out_file = codecs.open(file_path, 'w', encoding='utf8')
        out_file.write(str_root.decode('utf8'))
        out_file.close()


if __name__ == "__main__":
    path = "/home/sdb11/metro/metro_data/hand/test/xmls/"
    save_path = "/home/sdb11/metro/metro_data/hand/test/"
    m = Modify(path, save_path)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
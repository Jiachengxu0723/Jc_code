import os
import xml

path0 = 'D:\\xjc\\钢轨探伤\\201125\\804_DF150919_000'
path = os.listdir(path0)

for p in path:
    if p.find('xml'):
        xml_path = os.path.join(path0, p)
        bmp_path = os.path.join(path0, p.replace('xml', 'bmp'))
        dom = xml.dom.minidom.parse(xml_path)

print(1)
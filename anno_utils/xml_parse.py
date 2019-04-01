'''将xml格式的标注文件，转换成用于测试mAP的txt格式文件'''
from xml.dom.minidom import parse
import xml.dom.minidom
import glob
import os

file = glob.glob(r'C:\Users\cy\Desktop\download\yolo\gas_station\gas_station_img 标完的\*.xml')
for f in file:
    (filename, extension) = os.path.splitext(f)
    with open (filename+".txt",'w') as out_file_txt:
        DOMtree = xml.dom.minidom.parse(f)
        annotation=DOMtree.documentElement
        obj = annotation.getElementsByTagName("object")
        for o in obj:
            name = o.getElementsByTagName('name')[0].childNodes[0].data
            left = o.getElementsByTagName('xmin')[0].childNodes[0].data
            top = o.getElementsByTagName('ymin')[0].childNodes[0].data
            right =o.getElementsByTagName('xmax')[0].childNodes[0].data
            bottom = o.getElementsByTagName('ymax')[0].childNodes[0].data
            line = name + " "+left+" "+top+" "+right+" "+bottom +"\n"
            out_file_txt.writelines(line)

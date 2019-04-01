'''将yolo生成的标注文件转换成labelimg的xml格式'''

from xml.dom.minidom import Document
import os
import cv2
# 参数
# anno_line: 用于训练的标注文件的一行
# label_dict: 标注文件数字和类别的dict
# xml_dir: xml文件存放目录
def writeInfoToXml(anno_line, label_dict, xml_dir):
    anno = anno_line.split(" ")
    # 创建dom文档
    doc = Document()

    # 创建根节点
    annotation = doc.createElement('annotation')
    annotation.setAttribute('verified','no')
    # 根节点插入dom树
    doc.appendChild(annotation)

    floder = doc.createElement("floder")
    floder_text = doc.createTextNode("gas_station_img")
    floder.appendChild(floder_text)
    annotation.appendChild(floder)

    filename = doc.createElement("filename")
    filename_text = doc.createTextNode(anno[0].split("/")[-1].split(".")[0])
    filename.appendChild(filename_text)
    annotation.appendChild(filename)

    path = doc.createElement("path")
    path_text = doc.createTextNode(anno[0])
    path.appendChild(path_text)
    annotation.appendChild(path)

    source = doc.createElement("source")
    annotation.appendChild(source)

    database = doc.createElement("database")
    database_text = doc.createTextNode("Unknown")
    database.appendChild(database_text)
    source.appendChild(database)

    # 读取图片尺寸
    img = cv2.imread(anno[0].strip())
    w = img.shape[1]
    h = img.shape[0]
    size = doc.createElement("size")
    annotation.appendChild(size)

    width = doc.createElement("width")
    width_text = doc.createTextNode(str(w))
    width.appendChild(width_text)
    size.appendChild(width)

    height = doc.createElement("height")
    height_text = doc.createTextNode(str(h))
    height.appendChild(height_text)
    size.appendChild(height)

    depth = doc.createElement("depth")
    depth_text = doc.createTextNode("3")
    depth.appendChild(depth_text)
    size.appendChild(depth)

    segmented = doc.createElement("segmented")
    segmented_text = doc.createTextNode("0")
    segmented.appendChild(segmented_text)
    annotation.appendChild(segmented)


    # 依次将标注文件的每个物体的标注提取，创建对应节点并插入dom树
    for i in range(1,len(anno)):
        # 分离出x_min, y_min, x_max, y_max, lable
        (x_min, y_min, x_max, y_max, label) = anno[i].strip().split(",")

        # 每一组信息先创建节点<object>，然后插入到父节点<annotation>下
        object = doc.createElement('object')
        annotation.appendChild(object)

        # 将name插入<object>中
        # 创建节点<name>
        name = doc.createElement('name')
        # 创建<name>下的文本节点
        name_text = doc.createTextNode(label_dict[label])
        # 将文本节点插入到<name>下
        name.appendChild(name_text)
        # 将<name>插入到父节点<object>下
        object.appendChild(name)

        pose = doc.createElement('pose')
        pose_text = doc.createTextNode("Unspecified")
        pose.appendChild(pose_text)
        object.appendChild(pose)

        truncated = doc.createElement('truncated')
        truncated_text = doc.createTextNode("0")
        truncated.appendChild(truncated_text)
        object.appendChild(truncated)

        Difficult = doc.createElement('Difficult')
        Difficult_text = doc.createTextNode("0")
        Difficult.appendChild(Difficult_text)
        object.appendChild(Difficult)

        bndbox = doc.createElement('bndbox')
        object.appendChild(bndbox)

        xmin = doc.createElement('xmin')
        xmin_text = doc.createTextNode(x_min)
        xmin.appendChild(xmin_text)
        bndbox.appendChild(xmin)

        ymin = doc.createElement('ymin')
        ymin_text = doc.createTextNode(y_min)
        ymin.appendChild(ymin_text)
        bndbox.appendChild(ymin)

        xmax = doc.createElement('xmax')
        xmax_text = doc.createTextNode(x_max)
        xmax.appendChild(xmax_text)
        bndbox.appendChild(xmax)

        ymax = doc.createElement('ymax')
        ymax_text = doc.createTextNode(y_max)
        ymax.appendChild(ymax_text)
        bndbox.appendChild(ymax)

    # 将dom对象写入本地xml文件
    xml_name = anno[0].split("/")[-1].replace("jpg","xml")
    xml_path = os.path.join(xml_dir,xml_name)
    with open(xml_path, 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))

    return


label_dict={"0":"person", "1":"car"}
xml_dir = "/data/cy/yolo_dataset/DCjingsai/xml"
anno_file = open("/data/cy/yolo_dataset/DCjingsai/train_dc_keras.txt","r")
for line in anno_file:
    writeInfoToXml(line,label_dict,xml_dir)
'''
将多个txt标注文件汇集用于yolo模型训练的单个txt标注文件
'''
import os
import glob

# dir_path: 标注文件目录
# out_dir: 生成的标注文件存放位置
# flag：0：用于yolo模型生成的标注转换（car 0.98 160 130 269 244）
#       1：用于测试mAP的标注转换car (160 130 269 244）
def conver_anno(dir_path, out_path, flag=0):
    files = glob.glob(os.path.join(dir_path,r'*.txt'))
    out = open(out_path, "w")

    for file in files:
        with open(file) as f:
            (filename, extension) = os.path.splitext(file)
            content =filename + ".jpg"
            content = content.replace("txt","img")
            for line in f:
                class_ = line.split(" ")[0]
                if(flag==0):
                    x1 = line.split(" ")[2]
                    y1 = line.split(" ")[3]
                    x2 = line.split(" ")[4]
                    y2 = line.split(" ")[5].strip()
                elif(flag==1):
                    x1 = line.split(" ")[1]
                    y1 = line.split(" ")[2]
                    x2 = line.split(" ")[3]
                    y2 = line.split(" ")[4].strip()
                if (class_ == "car"):
                    type = 1
                elif (class_ == "person"):
                    type = 0
                content = content + " {},{},{},{},{}".format(x1, y1, x2, y2, type)
            content = content + "\n"
            out.writelines(content)
    out.close()

dir_path = r"/home/bupt/cy/yolo/gas/txt"
out_path = "/home/bupt/cy/yolo/gas/gas_labeled_1082.txt"
conver_anno(dir_path,out_path,flag=1)
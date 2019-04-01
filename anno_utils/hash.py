# -*- coding=utf-8 -*-
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import shutil
import glob


# extract feature
# lines: src_img path typr:list
def Extra_Hash_Featrue(lines, new_rows=64, new_cols=64):
    for name in lines:
        ori_img = Image.open(name.strip())
        feature_img = ori_img.resize((new_rows, new_cols))
        feature_img = feature_img.convert('L')
        mean_value = np.mean(np.mean(feature_img))
        feature = feature_img >= mean_value
        feature = np.matrix(feature, np.int8)
        if 'features' in locals():
            temp = np.reshape(feature, (1, new_cols * new_rows))
            features = np.vstack([features, temp])
        else:
            features = np.matrix(np.reshape(feature, (1, new_cols * new_rows)))

    return features


# 查找距离近的图片
# pic_feature：提取的hash感知特征
# pic_fullname_list：上面特征对应的图片绝对地址
# copy_path：发现相似度较高的图片后复制到的目录地址
# threshold：距离阈值
def find_close_img(pic_feature, pic_fullname_list, copy_path ,threshold=3):
    for i in np.arange(0, np.shape(pic_feature)[0]):
        dist = []
        src = pic_feature[i, :]
        for j in np.arange(0, np.shape(pic_feature)[0]):
            dst = pic_feature[j, :]
            temp = src != dst
            sum = np.sum(temp)
            dist.append(sum)
        # find minimum while ignoring the zeros on the diagonal
        index = np.argsort(dist)

        for i in range(1,len(index)):
            if (not os.path.exists(pic_fullname_list[index[0]])):
                break
            if(dist[index[i]] >= threshold):
                break
            elif(dist[index[i]] > 0):
                img_path = pic_fullname_list[index[i]]
                if(os.path.exists(img_path)):
                    shutil.copyfile(img_path, os.path.join(copy_path,img_path.split("\\")[-1]))
                    shutil.copyfile(img_path.replace(".jpg",".xml"), os.path.join(copy_path, img_path.split("\\")[-1]).replace(".jpg",".xml"))
                    os.remove(img_path)

        # Visualization

        # img1_path = pic_fullname_list[i]
        # img2_path = pic_fullname_list[index[1]]
        # img3_path = pic_fullname_list[index[2]]
        # img4_path = pic_fullname_list[index[3]]

        # img1 = Image.open(img1_path)
        # img2 = Image.open(img2_path)
        # img3 = Image.open(img3_path)
        # img4 = Image.open(img4_path)
        # plt.subplot(2, 2, 1)
        # plt.imshow(img1)
        # plt.title('src Image(%s)' % img1_path[img1_path.__len__() - 10:])
        # plt.axis('off')
        # plt.xlabel(img1_path[img1_path.__len__() - 10:])
        # plt.subplot(2, 2, 2)
        # plt.imshow(img2)
        # plt.title('Image1{} distence:{}'.format(img2_path[img2_path.__len__() - 10:],dist[index[1]]))
        # plt.axis('off')
        # plt.xlabel(img2_path[img2_path.__len__() - 10:])
        # plt.subplot(2, 2, 3)
        # plt.imshow(img3)
        # plt.title('Image2{} distence:{}'.format(img3_path[img3_path.__len__() - 10:], dist[index[2]]))
        # plt.axis('off')
        # plt.xlabel(img3_path[img3_path.__len__() - 10:])
        # plt.subplot(2, 2, 4)
        # plt.imshow(img4)
        # plt.title('Image3{} distence:{}'.format(img4_path[img4_path.__len__() - 10:], dist[index[3]]))
        # plt.axis('off')
        # plt.xlabel(img4_path[img4_path.__len__() - 10:])
        # plt.show()

        # set data source
pic_root_dir = r"C:\Users\cy\Desktop\download\yolo\gas_station\gas_station_img_1"
copy_path = r'C:\Users\cy\Desktop\download\yolo\gas_station\TODO'
pic_name_list = glob.glob(pic_root_dir+r"\*.jpg")

pic_fullname_list = [os.path.join(pic_root_dir,i) for i in pic_name_list]

# extract feature
set_size = 8
pic_feature = Extra_Hash_Featrue(pic_fullname_list, set_size, set_size)

# use feature to find candidate img
find_close_img(pic_feature, pic_fullname_list, copy_path, threshold=60)
